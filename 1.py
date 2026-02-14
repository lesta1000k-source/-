import json
import os
from dataclasses import dataclass
from typing import List, Optional

# Класс, представляющий сущность "Игровой компьютер"
@dataclass
class GamingComputer:
    id: int
    model: str
    processor: str
    ram: int  # ОЗУ в ГБ
    ssd: int  # SSD в ГБ
    graphics_card: str  # Видеокарта
    price: float
    is_on_sale: bool = False  # Флаг "распродажа"
    
    def __str__(self):
        """Строковое представление компьютера"""
        sale_status = " (РАСПРОДАЖА -10%)" if self.is_on_sale else ""
        return (f"[ID: {self.id}] {self.model}{sale_status}\n"
                f"  Процессор: {self.processor}, ОЗУ: {self.ram} ГБ, SSD: {self.ssd} ГБ\n"
                f"  Видеокарта: {self.graphics_card}, Цена: {self.price:,.2f} руб.\n")
    
    def to_dict(self):
        """Преобразование в словарь для сохранения в JSON"""
        return {
            'id': self.id,
            'model': self.model,
            'processor': self.processor,
            'ram': self.ram,
            'ssd': self.ssd,
            'graphics_card': self.graphics_card,
            'price': self.price,
            'is_on_sale': self.is_on_sale
        }
    
    @classmethod
    def from_dict(cls, data):
        """Создание объекта из словаря"""
        return cls(
            id=data['id'],
            model=data['model'],
            processor=data['processor'],
            ram=data['ram'],
            ssd=data['ssd'],
            graphics_card=data['graphics_card'],
            price=data['price'],
            is_on_sale=data.get('is_on_sale', False)
        )


class ComputerManager:
    """Класс для управления коллекцией компьютеров"""
    
    def __init__(self, filename='computers.json'):
        self.filename = filename
        self.computers: List[GamingComputer] = []
        self.load_data()
    
    def load_data(self):
        """Загрузка данных из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.computers = [GamingComputer.from_dict(item) for item in data]
                print(f"Загружено {len(self.computers)} компьютеров")
            except:
                print("Ошибка загрузки данных. Создан новый список.")
                self.computers = []
        else:
            self.computers = []
            self.init_sample_data()
    
    def save_data(self):
        """Сохранение данных в файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            data = [comp.to_dict() for comp in self.computers]
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def init_sample_data(self):
        """Инициализация тестовыми данными"""
        sample_computers = [
            GamingComputer(1, "GameMaster Pro", "Intel i9-13900K", 32, 1000, "NVIDIA RTX 4090", 250000),
            GamingComputer(2, "Striker Elite", "AMD Ryzen 9 7950X", 64, 2000, "NVIDIA RTX 4080", 320000),
            GamingComputer(3, "PowerPlay", "Intel i7-13700K", 16, 512, "NVIDIA RTX 4070", 150000),
            GamingComputer(4, "Budget Gamer", "AMD Ryzen 5 7600", 16, 512, "NVIDIA RTX 3060", 90000),
            GamingComputer(5, "Starter Pack", "Intel i5-13400F", 8, 256, "NVIDIA GTX 1660", 55000),
        ]
        self.computers = sample_computers
        self.save_data()
        print("Созданы тестовые данные")
    
    def search_by_criteria(self, min_ram: Optional[int] = None, max_price: Optional[float] = None,
                           min_ssd: Optional[int] = None, graphics_required: Optional[str] = None):
        """Поиск компьютеров по нескольким условиям"""
        results = self.computers
        
        if min_ram is not None:
            results = [c for c in results if c.ram >= min_ram]
        if max_price is not None:
            results = [c for c in results if c.price <= max_price]
        if min_ssd is not None:
            results = [c for c in results if c.ssd >= min_ssd]
        if graphics_required:
            results = [c for c in results if graphics_required.lower() in c.graphics_card.lower()]
        
        return results
    
    def sort_by_price(self, ascending=True):
        """Сортировка по цене"""
        return sorted(self.computers, key=lambda x: x.price, reverse=not ascending)
    
    def sort_by_ram_ssd_sum(self, ascending=True):
        """Сортировка по сумме ОЗУ + SSD"""
        return sorted(self.computers, key=lambda x: x.ram + x.ssd, reverse=not ascending)
    
    def add_computer(self, computer: GamingComputer):
        """Добавление нового компьютера с проверкой уникальности ID"""
        if any(c.id == computer.id for c in self.computers):
            raise ValueError(f"Компьютер с ID {computer.id} уже существует")
        self.computers.append(computer)
        self.save_data()
        print(f"Компьютер {computer.model} успешно добавлен")
    
    def delete_by_id(self, computer_id: int):
        """Удаление компьютера по ID"""
        initial_count = len(self.computers)
        self.computers = [c for c in self.computers if c.id != computer_id]
        if len(self.computers) < initial_count:
            self.save_data()
            print(f"Компьютер с ID {computer_id} удален")
        else:
            print(f"Компьютер с ID {computer_id} не найден")
    
    def delete_by_index(self, index: int):
        """Удаление компьютера по номеру в списке"""
        if 0 <= index < len(self.computers):
            removed = self.computers.pop(index)
            self.save_data()
            print(f"Компьютер {removed.model} удален")
        else:
            print(f"Неверный индекс. Допустимо: 0-{len(self.computers)-1}")
    
    def upgrade_ram(self, computer_id: int, additional_ram: int):
        """Увеличение объёма ОЗУ у компьютера по ID"""
        computer = next((c for c in self.computers if c.id == computer_id), None)
        if computer:
            computer.ram += additional_ram
            self.save_data()
            print(f"ОЗУ компьютера ID {computer_id} увеличено до {computer.ram} ГБ")
        else:
            print(f"Компьютер с ID {computer_id} не найден")
    
    def mark_as_sale(self, computer_id: int):
        """Пометить компьютер как 'распродажа' и уменьшить цену на 10%"""
        computer = next((c for c in self.computers if c.id == computer_id), None)
        if computer:
            if not computer.is_on_sale:
                computer.is_on_sale = True
                computer.price *= 0.9  # Уменьшаем цену на 10%
                self.save_data()
                print(f"Компьютер ID {computer_id} помечен как распродажа. Новая цена: {computer.price:,.2f} руб.")
            else:
                print(f"Компьютер ID {computer_id} уже на распродаже")
        else:
            print(f"Компьютер с ID {computer_id} не найден")
    
    def get_price_extremes(self):
        """Получить самый дорогой и самый дешевый компьютер"""
        if not self.computers:
            return None, None
        
        most_expensive = max(self.computers, key=lambda x: x.price)
        cheapest = min(self.computers, key=lambda x: x.price)
        return most_expensive, cheapest
    
    def filter_by_graphics(self, min_graphics: str):
        """Вывести компьютеры с видеокартой не слабее указанной"""
        # Простое сравнение по строке (можно усложнить по рейтингу видеокарт)
        return [c for c in self.computers if min_graphics.lower() in c.graphics_card.lower()]


def print_menu():
    """Вывод меню"""
    print("\n" + "="*50)
    print("УПРАВЛЕНИЕ ИГРОВЫМИ КОМПЬЮТЕРАМИ")
    print("="*50)
    print("1. Поиск компьютеров по условиям")
    print("2. Сортировка по цене")
    print("3. Сортировка по сумме ОЗУ + SSD")
    print("4. Добавить новый компьютер")
    print("5. Удалить компьютер по ID")
    print("6. Удалить компьютер по номеру в списке")
    print("7. Увеличить ОЗУ у компьютера по ID")
    print("8. Пометить компьютер как 'распродажа' (-10%)")
    print("9. Показать самый дорогой и дешевый компьютер")
    print("10. Показать компьютеры с видеокартой не слабее указанной")
    print("11. Показать все компьютеры")
    print("0. Выход")
    print("="*50)


def main():
    manager = ComputerManager()
    
    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()
        
        if choice == '1':
            print("\n--- ПОИСК ПО УСЛОВИЯМ ---")
            try:
                min_ram = input("Минимальный объем ОЗУ (ГБ, Enter - пропустить): ").strip()
                min_ram = int(min_ram) if min_ram else None
                
                max_price = input("Максимальная цена (руб, Enter - пропустить): ").strip()
                max_price = float(max_price) if max_price else None
                
                min_ssd = input("Минимальный объем SSD (ГБ, Enter - пропустить): ").strip()
                min_ssd = int(min_ssd) if min_ssd else None
                
                graphics = input("Модель видеокарты (Enter - пропустить): ").strip()
                graphics = graphics if graphics else None
                
                results = manager.search_by_criteria(min_ram, max_price, min_ssd, graphics)
                
                if results:
                    print(f"\nНайдено компьютеров: {len(results)}")
                    for comp in results:
                        print(comp)
                else:
                    print("Компьютеры не найдены")
            except ValueError as e:
                print(f"Ошибка ввода: {e}")
        
        elif choice == '2':
            print("\n--- СОРТИРОВКА ПО ЦЕНЕ ---")
            order = input("По возрастанию (1) или убыванию (2)?: ").strip()
            ascending = order == '1'
            sorted_comps = manager.sort_by_price(ascending)
            for comp in sorted_comps:
                print(comp)
        
        elif choice == '3':
            print("\n--- СОРТИРОВКА ПО СУММЕ ОЗУ+SSD ---")
            order = input("По возрастанию (1) или убыванию (2)?: ").strip()
            ascending = order == '1'
            sorted_comps = manager.sort_by_ram_ssd_sum(ascending)
            for comp in sorted_comps:
                print(comp)
        
        elif choice == '4':
            print("\n--- ДОБАВЛЕНИЕ НОВОГО КОМПЬЮТЕРА ---")
            try:
                new_id = int(input("ID: "))
                model = input("Модель: ")
                processor = input("Процессор: ")
                ram = int(input("ОЗУ (ГБ): "))
                ssd = int(input("SSD (ГБ): "))
                graphics = input("Видеокарта: ")
                price = float(input("Цена: "))
                
                new_computer = GamingComputer(new_id, model, processor, ram, ssd, graphics, price)
                manager.add_computer(new_computer)
            except ValueError as e:
                print(f"Ошибка: {e}")
        
        elif choice == '5':
            print("\n--- УДАЛЕНИЕ ПО ID ---")
            try:
                comp_id = int(input("Введите ID компьютера для удаления: "))
                manager.delete_by_id(comp_id)
            except ValueError:
                print("Неверный формат ID")
        
        elif choice == '6':
            print("\n--- УДАЛЕНИЕ ПО НОМЕРУ В СПИСКЕ ---")
            print("Текущий список:")
            for i, comp in enumerate(manager.computers):
                print(f"{i}. {comp.model} (ID: {comp.id})")
            try:
                index = int(input("Введите номер в списке: "))
                manager.delete_by_index(index)
            except ValueError:
                print("Неверный формат")
        
        elif choice == '7':
            print("\n--- УВЕЛИЧЕНИЕ ОЗУ ---")
            try:
                comp_id = int(input("ID компьютера: "))
                additional = int(input("Добавить ОЗУ (ГБ): "))
                manager.upgrade_ram(comp_id, additional)
            except ValueError:
                print("Неверный формат")
        
        elif choice == '8':
            print("\n--- ПОМЕТИТЬ КАК РАСПРОДАЖА ---")
            try:
                comp_id = int(input("ID компьютера: "))
                manager.mark_as_sale(comp_id)
            except ValueError:
                print("Неверный формат")
        
        elif choice == '9':
            print("\n--- САМЫЙ ДОРОГОЙ И ДЕШЕВЫЙ КОМПЬЮТЕР ---")
            expensive, cheap = manager.get_price_extremes()
            if expensive and cheap:
                print("Самый дорогой:")
                print(expensive)
                print("Самый дешевый:")
                print(cheap)
            else:
                print("Список компьютеров пуст")
        
        elif choice == '10':
            print("\n--- ПОИСК ПО ВИДЕОКАРТЕ ---")
            graphics = input("Минимальная модель видеокарты (например, RTX 3060): ")
            results = manager.filter_by_graphics(graphics)
            if results:
                print(f"\nНайдено компьютеров: {len(results)}")
                for comp in results:
                    print(comp)
            else:
                print("Компьютеры не найдены")
        
        elif choice == '11':
            print("\n--- ВСЕ КОМПЬЮТЕРЫ ---")
            if manager.computers:
                for comp in manager.computers:
                    print(comp)
            else:
                print("Список компьютеров пуст")
        
        elif choice == '0':
            print("Сохранение данных и выход...")
            manager.save_data()
            break
        
        else:
            print("Неверный выбор. Попробуйте снова.")
        
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()
