import json
import os
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from datetime import datetime

@dataclass
class Movie:
    
    id: int
    title: str
    year: int              # Год выпуска
    genre: str             # Жанр
    duration: int          # Длительность в минутах
    rating: float          # Рейтинг (например, от 0 до 10)
    price: float           # Цена билета/продажи
    is_epic: bool = False  # Флаг "эпик" (длительность > 150 мин)
    
    def __str__(self):
        epic_mark = " [ЭПИК]" if self.is_epic else ""
        return (f"[ID: {self.id}] {self.title}{epic_mark}\n"
                f"  Год: {self.year}, Жанр: {self.genre}\n"
                f"  Длительность: {self.duration} мин, Рейтинг: {self.rating:.1f}\n"
                f"  Цена: {self.price:,.2f} руб.\n")
    
    def to_dict(self):
        """Преобразование в словарь для сохранения в JSON"""
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'genre': self.genre,
            'duration': self.duration,
            'rating': self.rating,
            'price': self.price,
            'is_epic': self.is_epic
        }
    
    @classmethod
    def from_dict(cls, data):
        """Создание объекта из словаря"""
        return cls(
            id=data['id'],
            title=data['title'],
            year=data['year'],
            genre=data['genre'],
            duration=data['duration'],
            rating=data['rating'],
            price=data['price'],
            is_epic=data.get('is_epic', False)
        )


class MovieManager:
    """Класс для управления коллекцией фильмов"""
    
    def __init__(self, filename='movies.json'):
        self.filename = filename
        self.movies: List[Movie] = []
        self.load_data()
    
    def load_data(self):
        """Загрузка данных из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.movies = [Movie.from_dict(item) for item in data]
                print(f"Загружено {len(self.movies)} фильмов")
            except Exception as e:
                print(f"Ошибка загрузки данных: {e}")
                self.movies = []
                self.init_sample_data()
        else:
            self.movies = []
            self.init_sample_data()
    
    def save_data(self):
        """Сохранение данных в файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            data = [movie.to_dict() for movie in self.movies]
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def init_sample_data(self):
        """Инициализация тестовыми данными"""
        sample_movies = [
            Movie(1, "Побег из Шоушенка", 1994, "драма", 142, 9.3, 350),
            Movie(2, "Крёстный отец", 1972, "криминал", 175, 9.2, 400),
            Movie(3, "Тёмный рыцарь", 2008, "боевик", 152, 9.0, 380),
            Movie(4, "Криминальное чтиво", 1994, "криминал", 154, 8.9, 320),
            Movie(5, "Бойцовский клуб", 1999, "триллер", 139, 8.8, 300),
            Movie(6, "Форрест Гамп", 1994, "драма", 142, 8.8, 330),
            Movie(7, "Начало", 2010, "фантастика", 148, 8.8, 390),
            Movie(8, "Матрица", 1999, "фантастика", 136, 8.7, 310),
            Movie(9, "Хороший, плохой, злой", 1966, "вестерн", 178, 8.8, 280),
            Movie(10, "Зелёная миля", 1999, "драма", 189, 8.9, 340),
            Movie(11, "Список Шиндлера", 1993, "драма", 195, 9.0, 360),
            Movie(12, "1+1", 2011, "комедия", 112, 8.8, 320),
            Movie(13, "Интерстеллар", 2014, "фантастика", 169, 8.7, 400),
            Movie(14, "Гладиатор", 2000, "боевик", 155, 8.5, 330),
            Movie(15, "Король Лев", 1994, "мультфильм", 88, 8.5, 300),
        ]
        
        # Автоматически помечаем фильмы с длительностью > 150 минут
        for movie in sample_movies:
            movie.is_epic = movie.duration > 150
            
        self.movies = sample_movies
        self.save_data()
        print("Созданы тестовые данные")
    
    def search_by_year_range_and_genre(self, year_from: Optional[int] = None, 
                                       year_to: Optional[int] = None,
                                       genre: Optional[str] = None) -> List[Movie]:
        """
        Поиск фильмов по диапазону годов выпуска и жанру
        """
        results = self.movies
        
        if year_from is not None:
            results = [m for m in results if m.year >= year_from]
        
        if year_to is not None:
            results = [m for m in results if m.year <= year_to]
        
        if genre:
            results = [m for m in results if genre.lower() in m.genre.lower()]
        
        return results
    
    def sort_by_duration(self, ascending=True) -> List[Movie]:
        """Сортировка фильмов по длительности"""
        return sorted(self.movies, key=lambda x: x.duration, reverse=not ascending)
    
    def sort_by_rating_desc(self) -> List[Movie]:
        """Сортировка фильмов по рейтингу (по убыванию)"""
        return sorted(self.movies, key=lambda x: x.rating, reverse=True)
    
    def calculate_average_duration(self) -> float:
        """Подсчет средней длительности фильмов"""
        if not self.movies:
            return 0.0
        total_duration = sum(movie.duration for movie in self.movies)
        return total_duration / len(self.movies)
    
    def get_top_3_by_rating(self) -> List[Movie]:
        """Вывести топ-3 фильма по рейтингу"""
        sorted_movies = self.sort_by_rating_desc()
        return sorted_movies[:3]
    
    def increase_price_for_old_movies(self, year_threshold: int = 2000, increase_percent: float = 20.0) -> List[Movie]:
        """
        Увеличить цену фильмов, выпущенных до указанного года
        Возвращает список измененных фильмов
        """
        affected_movies = []
        for movie in self.movies:
            if movie.year < year_threshold:
                old_price = movie.price
                movie.price *= (1 + increase_percent / 100)
                affected_movies.append((movie, old_price, movie.price))
        
        if affected_movies:
            self.save_data()
            print(f"Увеличена цена для {len(affected_movies)} фильмов (до {year_threshold} года)")
            for movie, old_price, new_price in affected_movies:
                print(f"  - {movie.title} ({movie.year}): {old_price:,.0f} → {new_price:,.0f} руб. (+{increase_percent}%)")
        else:
            print(f"Нет фильмов, выпущенных до {year_threshold} года")
        
        return [m[0] for m in affected_movies]
    
    def mark_epic_movies(self, duration_threshold: int = 150) -> List[Movie]:
        """
        Пометить фильмы длительностью более указанной как «эпик»
        Возвращает список помеченных фильмов
        """
        marked_movies = []
        for movie in self.movies:
            if movie.duration > duration_threshold and not movie.is_epic:
                movie.is_epic = True
                marked_movies.append(movie)
        
        if marked_movies:
            self.save_data()
            print(f"Помечено как «эпик»: {len(marked_movies)} фильмов")
            for movie in marked_movies:
                print(f"  - {movie.title} ({movie.duration} мин)")
        else:
            print("Нет новых фильмов для пометки «эпик»")
        
        return marked_movies
    
    def get_movies_by_genre(self, genre: str) -> List[Movie]:
        """Получить фильмы по жанру"""
        return [m for m in self.movies if genre.lower() in m.genre.lower()]
    
    def get_statistics(self) -> dict:
        """Получить статистику по коллекции"""
        if not self.movies:
            return {}
        
        stats = {
            'total_movies': len(self.movies),
            'average_rating': sum(m.rating for m in self.movies) / len(self.movies),
            'average_duration': self.calculate_average_duration(),
            'total_value': sum(m.price for m in self.movies),
            'oldest_year': min(m.year for m in self.movies),
            'newest_year': max(m.year for m in self.movies),
            'epic_count': sum(1 for m in self.movies if m.is_epic),
            'genres': len(set(m.genre for m in self.movies))
        }
        return stats


def print_menu():
    """Вывод меню"""
    print("\n" + "="*60)
    print("УПРАВЛЕНИЕ КОЛЛЕКЦИЕЙ ФИЛЬМОВ")
    print("="*60)
    print("1. Поиск фильмов по годам и жанру")
    print("2. Сортировка по длительности")
    print("3. Сортировка по рейтингу (по убыванию)")
    print("4. Подсчитать среднюю длительность фильмов")
    print("5. Вывести топ-3 фильма по рейтингу")
    print("6. Увеличить цену фильмов, выпущенных до 2000 года")
    print("7. Пометить фильмы длительностью > 150 мин как «эпик»")
    print("8. Показать все фильмы")
    print("9. Статистика коллекции")
    print("0. Выход")
    print("="*60)


def main():
    manager = MovieManager()
    
    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()
        
        if choice == '1':
            print("\n--- ПОИСК ПО ГОДАМ И ЖАНРУ ---")
            try:
                year_from = input("Год выпуска с (Enter - пропустить): ").strip()
                year_from = int(year_from) if year_from else None
                
                year_to = input("Год выпуска по (Enter - пропустить): ").strip()
                year_to = int(year_to) if year_to else None
                
                genre = input("Жанр (Enter - пропустить): ").strip()
                genre = genre if genre else None
                
                results = manager.search_by_year_range_and_genre(year_from, year_to, genre)
                
                if results:
                    print(f"\nНайдено фильмов: {len(results)}")
                    for movie in results:
                        print(movie)
                else:
                    print("Фильмы не найдены")
            except ValueError as e:
                print(f"Ошибка ввода: {e}")
        
        elif choice == '2':
            print("\n--- СОРТИРОВКА ПО ДЛИТЕЛЬНОСТИ ---")
            order = input("По возрастанию (1) или убыванию (2)?: ").strip()
            ascending = order == '1'
            sorted_movies = manager.sort_by_duration(ascending)
            for movie in sorted_movies:
                print(movie)
        
        elif choice == '3':
            print("\n--- СОРТИРОВКА ПО РЕЙТИНГУ (ПО УБЫВАНИЮ) ---")
            sorted_movies = manager.sort_by_rating_desc()
            for i, movie in enumerate(sorted_movies, 1):
                print(f"{i}. {movie.title} - Рейтинг: {movie.rating:.1f}")
        
        elif choice == '4':
            print("\n--- СРЕДНЯЯ ДЛИТЕЛЬНОСТЬ ФИЛЬМОВ ---")
            avg_duration = manager.calculate_average_duration()
            print(f"Средняя длительность: {avg_duration:.1f} минут")
            print(f"({avg_duration/60:.1f} часов)")
        
        elif choice == '5':
            print("\n--- ТОП-3 ФИЛЬМА ПО РЕЙТИНГУ ---")
            top_movies = manager.get_top_3_by_rating()
            if top_movies:
                for i, movie in enumerate(top_movies, 1):
                    print(f"\n{i}. {movie.title}")
                    print(f"   Рейтинг: {movie.rating:.1f}, Год: {movie.year}")
                    print(f"   Длительность: {movie.duration} мин, Жанр: {movie.genre}")
            else:
                print("Нет фильмов в коллекции")
        
        elif choice == '6':
            print("\n--- УВЕЛИЧЕНИЕ ЦЕНЫ ФИЛЬМОВ ДО 2000 ГОДА ---")
            confirm = input("Увеличить цену на 20% для фильмов до 2000 года? (д/н): ").strip().lower()
            if confirm in ['д', 'да', 'y', 'yes']:
                manager.increase_price_for_old_movies(2000, 20.0)
            else:
                print("Операция отменена")
        
        elif choice == '7':
            print("\n--- ПОМЕТИТЬ ФИЛЬМЫ КАК «ЭПИК» (>150 МИН) ---")
            manager.mark_epic_movies(150)
        
        elif choice == '8':
            print("\n--- ВСЕ ФИЛЬМЫ ---")
            if manager.movies:
                
                movies_by_genre = {}
                for movie in manager.movies:
                    if movie.genre not in movies_by_genre:
                        movies_by_genre[movie.genre] = []
                    movies_by_genre[movie.genre].append(movie)
                
                for genre, movies in movies_by_genre.items():
                    print(f"\n=== {genre.upper()} ===")
                    for movie in movies:
                        print(f"  {movie.title} ({movie.year}) - {movie.duration} мин, рейтинг: {movie.rating:.1f}")
            else:
                print("Коллекция пуста")
        
        elif choice == '9':
            print("\n--- СТАТИСТИКА КОЛЛЕКЦИИ ---")
            stats = manager.get_statistics()
            if stats:
                print(f"Всего фильмов: {stats['total_movies']}")
                print(f"Средний рейтинг: {stats['average_rating']:.2f}")
                print(f"Средняя длительность: {stats['average_duration']:.1f} мин")
                print(f"Общая стоимость (сумма цен): {stats['total_value']:,.0f} руб.")
                print(f"Годы выпуска: {stats['oldest_year']} - {stats['newest_year']}")
                print(f"Фильмов «эпик»: {stats['epic_count']}")
                print(f"Количество жанров: {stats['genres']}")
            else:
                print("Коллекция пуста")
        
        elif choice == '0':
            print("Сохранение данных и выход...")
            manager.save_data()
            break
        
        else:
            print("Неверный выбор. Попробуйте снова.")
        
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()
