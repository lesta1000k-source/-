import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple


class Condition(Enum)
    NEW = "новый"
    GOOD = "хороший"
    WORN = "изношенный"
    NEEDS_REPAIR = "требует ремонта"
    
    def __str__(self):
        return self.value

@dataclass
class SportsEquipment:
    """Класс, представляющий сущность Спортивный инвентарь"""
    id: int
    name: str
    sport_type: str  # Вид спорта
    weight: float    # Вес в кг
    price: float     # Цена за единицу
    quantity: int    # Количество на складе
    condition: Condition  # Состояние
    
    def __str__(self):
        return (f"[ID: {self.id}] {self.name}\n"
                f"  Вид спорта: {self.sport_type}, Вес: {self.weight} кг\n"
                f"  Цена: {self.price:,.2f} руб., Кол-во: {self.quantity} шт.\n"
                f"  Состояние: {self.condition}\n")
    
    def total_value(self) -> float:
        """Общая стоимость данного инвентаря на складе"""
        return self.price * self.quantity
    
    def to_dict(self):
        """Преобразование в словарь для сохранения в JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'sport_type': self.sport_type,
            'weight': self.weight,
            'price': self.price,
            'quantity': self.quantity,
            'condition': self.condition.value
        }
    
    @classmethod
    def from_dict(cls, data):
        """Создание объекта из словаря"""
        # Преобразуем строку состояния обратно в Enum
        condition_value = data['condition']
        condition = next((c for c in Condition if c.value == condition_value), Condition.GOOD)
        
        return cls(
            id=data['id'],
            name=data['name'],
            sport_type=data['sport_type'],
            weight=data['weight'],
            price=data['price'],
            quantity=data['quantity'],
            condition=condition
        )


class InventoryManager:
    """Класс для управления складом спортивного инвентаря"""
    
    def __init__(self, filename='inventory.json'):
        self.filename = filename
        self.items: List[SportsEquipment] = []
        self.load_data()
    
    def load_data(self):
        """Загрузка данных из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.items = [SportsEquipment.from_dict(item) for item in data]
                print(f"Загружено {len(self.items)} позиций инвентаря")
            except Exception as e:
                print(f"Ошибка загрузки данных: {e}")
                self.items = []
                self.init_sample_data()
        else:
            self.items = []
            self.init_sample_data()
    
    def save_data(self):
        """Сохранение данных в файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            data = [item.to_dict() for item in self.items]
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def init_sample_data(self):
        """Инициализация тестовыми данными"""
        sample_items = [
            SportsEquipment(1, "Футбольный мяч", "футбол", 0.45, 2500, 50, Condition.GOOD),
            SportsEquipment(2, "Баскетбольный мяч", "баскетбол", 0.62, 3200, 30, Condition.NEW),
            SportsEquipment(3, "Теннисная ракетка", "теннис", 0.3, 8500, 15, Condition.NEW),
            SportsEquipment(4, "Гантель 5 кг", "фитнес", 5.0, 1200, 25, Condition.GOOD),
            SportsEquipment(5, "Гантель 10 кг", "фитнес", 10.0, 2200, 20, Condition.WORN),
            SportsEquipment(6, "Штанга", "тяжелая атлетика", 20.0, 15000, 5, Condition.GOOD),
            SportsEquipment(7, "Боксерские перчатки", "бокс", 0.5, 4500, 12, Condition.NEW),
            SportsEquipment(8, "Скакалка", "фитнес", 0.2, 800, 40, Condition.GOOD),
            SportsEquipment(9, "Велосипед", "велоспорт", 12.0, 35000, 3, Condition.NEW),
            SportsEquipment(10, "Лыжи", "лыжный спорт", 2.5, 18000, 8, Condition.NEEDS_REPAIR),
        ]
        self.items = sample_items
        self.save_data()
        print("Созданы тестовые данные")
    
    def search_by_sport_and_weight(self, sport_type: Optional[str] = None, 
                                   min_weight: Optional[float] = None, 
                                   max_weight: Optional[float] = None) -> List[SportsEquipment]:
        """
        Поиск инвентаря по виду спорта и диапазону веса
        """
        results = self.items
        
        if sport_type:
            results = [item for item in results if sport_type.lower() in item.sport_type.lower()]
        
        if min_weight is not None:
            results = [item for item in results if item.weight >= min_weight]
        
        if max_weight is not None:
            results = [item for item in results if item.weight <= max_weight]
        
        return results
    
    def sort_by_price(self, ascending=True) -> List[SportsEquipment]:
        """Сортировка по цене"""
        return sorted(self.items, key=lambda x: x.price, reverse=not ascending)
    
    def sort_by_quantity_desc(self) -> List[SportsEquipment]:
        """Сортировка по количеству на складе (по убыванию)"""
        return sorted(self.items, key=lambda x: x.quantity, reverse=True)
    
    def write_off(self, item_id: int, quantity: int) -> bool:
        """
        Списать инвентарь - уменьшить количество на складе
        Возвращает True, если операция успешна
        """
        item = next((i for i in self.items if i.id == item_id), None)
        if not item:
            print(f"Инвентарь с ID {item_id} не найден")
            return False
        
        if quantity <= 0:
            print("Количество для списания должно быть положительным")
            return False
        
        if item.quantity < quantity:
            print(f"Недостаточно инвентаря на складе. Доступно: {item.quantity}")
            return False
        
        item.quantity -= quantity
        self.save_data()
        print(f"Списано {quantity} ед. инвентаря '{item.name}'. Остаток: {item.quantity}")
        
        # Автоматическое удаление, если количество стало 0
        if item.quantity == 0:
            print(f"Количество инвентаря '{item.name}' стало равно 0. Рекомендуется удалить.")
        
        return True
    
    def calculate_total_warehouse_value(self) -> float:
        """Подсчитать общую стоимость склада"""
        total = sum(item.total_value() for item in self.items)
        return total
    
    def get_new_items(self) -> List[SportsEquipment]:
        """Вывести инвентарь в состоянии «новый»"""
        return [item for item in self.items if item.condition == Condition.NEW]
    
    def mark_for_repair(self) -> List[SportsEquipment]:
        """
        Пометить инвентарь как «требует ремонта», если состояние не равно «новый»
        Возвращает список помеченных предметов
        """
        marked_items = []
        for item in self.items:
            if item.condition != Condition.NEW and item.condition != Condition.NEEDS_REPAIR:
                item.condition = Condition.NEEDS_REPAIR
                marked_items.append(item)
        
        if marked_items:
            self.save_data()
            print(f"Помечено как 'требует ремонта': {len(marked_items)} позиций")
        else:
            print("Нет инвентаря для пометки на ремонт")
        
        return marked_items
    
    def get_heaviest_item(self) -> Optional[SportsEquipment]:
        """Найти самый тяжёлый инвентарь"""
        if not self.items:
            return None
        return max(self.items, key=lambda x: x.weight)
    
    def delete_zero_quantity(self) -> int:
        """
        Удалить инвентарь с количеством на складе равным 0
        Возвращает количество удаленных позиций
        """
        initial_count = len(self.items)
        self.items = [item for item in self.items if item.quantity > 0]
        deleted_count = initial_count - len(self.items)
        
        if deleted_count > 0:
            self.save_data()
            print(f"Удалено {deleted_count} позиций с нулевым количеством")
        else:
            print("Нет позиций с нулевым количеством")
        
        return deleted_count


def print_menu():
    """Вывод меню"""
    print("\n" + "="*60)
    print("УПРАВЛЕНИЕ СКЛАДОМ СПОРТИВНОГО ИНВЕНТАРЯ")
    print("="*60)
    print("1. Поиск инвентаря по виду спорта и диапазону веса")
    print("2. Сортировка по цене")
    print("3. Сортировка по количеству на складе (по убыванию)")
    print("4. Списать инвентарь (уменьшить количество)")
    print("5. Подсчитать общую стоимость склада")
    print("6. Показать инвентарь в состоянии «новый»")
    print("7. Пометить инвентарь как «требует ремонта»")
    print("8. Найти самый тяжёлый инвентарь")
    print("9. Удалить инвентарь с количеством = 0")
    print("10. Показать весь инвентарь")
    print("0. Выход")
    print("="*60)


def main():
    manager = InventoryManager()
    
    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()
        
        if choice == '1':
            print("\n--- ПОИСК ПО ВИДУ СПОРТА И ДИАПАЗОНУ ВЕСА ---")
            try:
                sport = input("Вид спорта (Enter - пропустить): ").strip()
                sport = sport if sport else None
                
                min_weight = input("Минимальный вес (кг, Enter - пропустить): ").strip()
                min_weight = float(min_weight) if min_weight else None
                
                max_weight = input("Максимальный вес (кг, Enter - пропустить): ").strip()
                max_weight = float(max_weight) if max_weight else None
                
                results = manager.search_by_sport_and_weight(sport, min_weight, max_weight)
                
                if results:
                    print(f"\nНайдено позиций: {len(results)}")
                    for item in results:
                        print(item)
                else:
                    print("Инвентарь не найден")
            except ValueError as e:
                print(f"Ошибка ввода: {e}")
        
        elif choice == '2':
            print("\n--- СОРТИРОВКА ПО ЦЕНЕ ---")
            order = input("По возрастанию (1) или убыванию (2)?: ").strip()
            ascending = order == '1'
            sorted_items = manager.sort_by_price(ascending)
            for item in sorted_items:
                print(item)
        
        elif choice == '3':
            print("\n--- СОРТИРОВКА ПО КОЛИЧЕСТВУ (ПО УБЫВАНИЮ) ---")
            sorted_items = manager.sort_by_quantity_desc()
            for item in sorted_items:
                print(item)
        
        elif choice == '4':
            print("\n--- СПИСАНИЕ ИНВЕНТАРЯ ---")
            try:
                
                print("Доступный инвентарь:")
                for item in manager.items:
                    print(f"ID: {item.id} - {item.name} (в наличии: {item.quantity})")
                
                item_id = int(input("\nID инвентаря для списания: "))
                quantity = int(input("Количество для списания: "))
                manager.write_off(item_id, quantity)
            except ValueError:
                print("Неверный формат числа")
        
        elif choice == '5':
            print("\n--- ОБЩАЯ СТОИМОСТЬ СКЛАДА ---")
            total = manager.calculate_total_warehouse_value()
            print(f"Общая стоимость всех товаров на складе: {total:,.2f} руб.")
            
        
            total_items = sum(item.quantity for item in manager.items)
            print(f"Всего единиц инвентаря: {total_items} шт.")
        
        elif choice == '6':
            print("\n--- ИНВЕНТАРЬ В СОСТОЯНИИ «НОВЫЙ» ---")
            new_items = manager.get_new_items()
            if new_items:
                for item in new_items:
                    print(item)
            else:
                print("Нет нового инвентаря")
        
        elif choice == '7':
            print("\n--- ПОМЕТИТЬ ИНВЕНТАРЬ КАК «ТРЕБУЕТ РЕМОНТА» ---")
            marked = manager.mark_for_repair()
            if marked:
                print("Помеченный инвентарь:")
                for item in marked:
                    print(f"  - {item.name} (ID: {item.id})")
        
        elif choice == '8':
            print("\n--- САМЫЙ ТЯЖЁЛЫЙ ИНВЕНТАРЬ ---")
            heaviest = manager.get_heaviest_item()
            if heaviest:
                print("Самый тяжёлый предмет:")
                print(heaviest)
            else:
                print("Склад пуст")
        
        elif choice == '9':
            print("\n--- УДАЛЕНИЕ ИНВЕНТАРЯ С НУЛЕВЫМ КОЛИЧЕСТВОМ ---")
            deleted = manager.delete_zero_quantity()
            print(f"Удалено позиций: {deleted}")
        
        elif choice == '10':
            print("\n--- ВЕСЬ ИНВЕНТАРЬ ---")
            if manager.items:
                for item in manager.items:
                    print(item)
              
                total_value = manager.calculate_total_warehouse_value()
                print(f"\nИтого позиций: {len(manager.items)}")
                print(f"Общая стоимость: {total_value:,.2f} руб.")
            else:
                print("Склад пуст")
        
        elif choice == '0':
            print("Сохранение данных и выход...")
            manager.save_data()
            break
        
        else:
            print("Неверный выбор. Попробуйте снова.")
        
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()
