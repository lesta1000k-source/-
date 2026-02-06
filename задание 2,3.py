class VideoGame:
    def __init__(self, title, genre, platform, age_rating, player_score, price, copies_sold):
        self.title = title
        self.genre = genre
        self.platform = platform
        self.age_rating = age_rating
        self.player_score = player_score
        self.price = price
        self.copies_sold = copies_sold
        self.is_hit = False  

    def update_hit_status(self):
        self.is_hit = self.player_score >= 8.5

    def __str__(self):
        hit_status = " (ХИТ)" if self.is_hit else ""
        return f"{self.title}{hit_status} | {self.genre} | {self.platform} | {self.age_rating}+ | Оценка: {self.player_score} | Цена: ${self.price:.2f} | Продано: {self.copies_sold}"


class GameManager:
    def __init__(self):
        self.games = []

    def add_game(self, game):
        self.games.append(game)
        game.update_hit_status()

    def search_by_title(self, substring):
        return [game for game in self.games if substring.lower() in game.title.lower()]

    def filter_games(self, age_rating=None, platform=None):
        filtered = self.games
        if age_rating is not None:
            filtered = [game for game in filtered if game.age_rating == age_rating]
        if platform is not None:
            filtered = [game for game in filtered if game.platform.lower() == platform.lower()]
        return filtered

    def sort_games(self, by='score', ascending=False)
        if by == 'score':
            return sorted(self.games, key=lambda g: g.player_score, reverse=not ascending)
        elif by == 'name':
            return sorted(self.games, key=lambda g: g.title.lower(), reverse=not ascending)
        else:
            return self.games

    def change_price_by_genre(self, genre, discount_percent)
        for game in self.games:
            if game.genre.lower() == genre.lower():
                game.price *= (1 - discount_percent / 100)

    def average_price(self):
        if not self.games:
            return 0.0
        total = sum(game.price for game in self.games)
        return total / len(self.games)

    def game_with_max_score(self):
        if not self.games:
            return None
        return max(self.games, key=lambda g: g.player_score)

    def mark_hits(self):
        for game in self.games:
            game.update_hit_status()

    def remove_out_of_stock(self):
        self.games = [game for game in self.games if game.copies_sold > 0]

    def print_games(self, games_list=None):
        if games_list is None:
            games_list = self.games
        for game in games_list:
            print(game)
        if not games_list:
            print("Список игр пуст.")

def main():
    manager = GameManager()

    manager.add_game(VideoGame("The Witcher 3", "RPG", "PC", 18, 9.7, 39.99, 50000000))
    manager.add_game(VideoGame("Minecraft", "Sandbox", "Multiplatform", 7, 9.0, 26.95, 300000000))
    manager.add_game(VideoGame("Cyberpunk 2077", "RPG", "PC", 18, 7.5, 49.99, 20000000))
    manager.add_game(VideoGame("FIFA 23", "Sports", "PS5", 3, 8.0, 69.99, 10000000))
    manager.add_game(VideoGame("The Last of Us", "Action", "PS5", 18, 9.5, 59.99, 0))  # Нет копий

    print("Все игры:")
    manager.print_games()
    print()


    print("Поиск по 'Witcher':")
    manager.print_games(manager.search_by_title("Witcher"))
    print()

    print("Фильтр по платформе 'PC':")
    manager.print_games(manager.filter_games(platform="PC"))
    print()

    print("Сортировка по оценке (по убыванию):")
    manager.print_games(manager.sort_games(by='score'))
    print()

    print("Скидка 20% на игры жанра RPG:")
    manager.change_price_by_genre("RPG", 20)
    manager.print_games()
    print()

    print(f"Средняя цена всех игр: ${manager.average_price():.2f}")
    print()

    max_score_game = manager.game_with_max_score()
    print(f"Игра с максимальной оценкой: {max_score_game}")
    print()

    manager.mark_hits()
    print("Игры после отметки хитов:")
    manager.print_games()
    print()

    print("Удаление игр с количеством копий 0:")
    manager.remove_out_of_stock()
    manager.print_games()


if __name__ == "__main__":
    main()









ЗАДАНИЕ 3

class OnlineCourse:
    def __init__(self, title, platform, difficulty, duration_hours, rating, price, students_enrolled):
        self.title = title
        self.platform = platform
        self.difficulty = difficulty  # "начинающий", "средний", "продвинутый"
        self.duration_hours = duration_hours
        self.rating = rating
        self.price = price
        self.students_enrolled = students_enrolled

    def __str__(self):
        return (f"{self.title} [{self.platform}] | "
                f"Уровень: {self.difficulty} | "
                f"Длительность: {self.duration_hours} ч. | "
                f"Рейтинг: {self.rating:.1f} | "
                f"Цена: ${self.price:.2f} | "
                f"Студентов: {self.students_enrolled}")


class CourseManager:
    def __init__(self):
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)
      
    def search_by_platform_and_difficulty(self, platform=None, difficulty=None):
        """Поиск курсов по платформе и/или уровню сложности"""
        result = self.courses
        if platform:
            result = [c for c in result if c.platform.lower() == platform.lower()]
        if difficulty:
            result = [c for c in result if c.difficulty.lower() == difficulty.lower()]
        return result

    def sort_courses(self, by='duration', ascending=True):
        """Сортировка по длительности или количеству студентов"""
        if by == 'duration':
            return sorted(self.courses, 
                         key=lambda c: c.duration_hours, 
                         reverse=not ascending)
        elif by == 'students':
            return sorted(self.courses, 
                         key=lambda c: c.students_enrolled, 
                         reverse=not ascending)
        else:
            return self.courses

    def total_revenue(self):
        """Общий доход от всех курсов"""
        return sum(course.price * course.students_enrolled for course in self.courses)

    def increase_price_for_advanced(self, percent=15):
        """Увеличить цену продвинутых курсов на указанный процент"""
        for course in self.courses:
            if course.difficulty.lower() == "продвинутый":
                course.price *= (1 + percent / 100)

    def courses_longer_than(self, hours):
        """Курсы длительностью больше указанного количества часов"""
        return [course for course in self.courses if course.duration_hours > hours]

    def course_with_min_rating(self):
        """Курс с минимальным рейтингом"""
        if not self.courses:
            return None
        return min(self.courses, key=lambda c: c.rating)

    def merge_platforms(self, platform1, platform2):
        """Объединить курсы двух платформ"""
        platform1_lower = platform1.lower()
        platform2_lower = platform2.lower()
        return [course for course in self.courses 
                if course.platform.lower() in [platform1_lower, platform2_lower]]

    def remove_low_rating_courses(self, threshold=4.0):
        """Удалить курсы с рейтингом ниже указанного порога"""
        self.courses = [course for course in self.courses if course.rating >= threshold]

    def print_courses(self, courses_list=None):
        """Вспомогательный метод для вывода списка курсов"""
        if courses_list is None:
            courses_list = self.courses
        
        if not courses_list:
            print("Список курсов пуст.")
            return
            
        for course in courses_list:
            print(course)


def main():
    manager = CourseManager()

    # Добавляем курсы
    manager.add_course(OnlineCourse("Python для начинающих", "Coursera", "начинающий", 24, 4.5, 49.99, 15000))
    manager.add_course(OnlineCourse("Машинное обучение", "Udemy", "продвинутый", 56, 4.8, 89.99, 8000))
    manager.add_course(OnlineCourse("Веб-разработка", "Stepik", "средний", 42, 4.2, 59.99, 12000))
    manager.add_course(OnlineCourse("Data Science", "Coursera", "продвинутый", 68, 4.9, 99.99, 6500))
    manager.add_course(OnlineCourse("Основы программирования", "Udemy", "начинающий", 18, 3.8, 29.99, 20000))
    manager.add_course(OnlineCourse("Алгоритмы и структуры данных", "Coursera", "продвинутый", 72, 4.7, 79.99, 9500))

    print("Все курсы:")
    manager.print_courses()
    print()

    print("Курсы на Coursera продвинутого уровня:")
    found = manager.search_by_platform_and_difficulty(platform="Coursera", difficulty="продвинутый")
    manager.print_courses(found)
    print()

    print("Курсы, отсортированные по длительности (по возрастанию):")
    sorted_by_duration = manager.sort_courses(by='duration', ascending=True)
    manager.print_courses(sorted_by_duration)
    print()
  
    total = manager.total_revenue()
    print(f"Общий доход от всех курсов: ${total:,.2f}")
    print()

    print("Увеличение цены продвинутых курсов на 15%:")
    manager.increase_price_for_advanced(15)
    manager.print_courses()
    print()

    print("Курсы длительностью более 50 часов:")
    long_courses = manager.courses_longer_than(50)
    manager.print_courses(long_courses)
    print()

    min_rating_course = manager.course_with_min_rating()
    print(f"Курс с минимальным рейтингом: {min_rating_course}")
    print()
  
    print("Курсы с платформ Coursera и Udemy:")
    merged = manager.merge_platforms("Coursera", "Udemy")
    manager.print_courses(merged)
    print()

    print("Удаление курсов с рейтингом ниже 4.0:")
    manager.remove_low_rating_courses(4.0)
    print("Оставшиеся курсы:")
    manager.print_courses()


if __name__ == "__main__":
    main()
