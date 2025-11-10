# Импорт модуля для работы с CSV файлами
import csv
# Импорт модуля для работы с операционной системой (проверка существования файлов)
import os


# Класс для валидации параметров конфигурации
class SettingsValidator:
    """Валидатор параметров конфигурации"""

    # Статический метод для проверки имени пакета
    @staticmethod
    def check_package_name(name):
        # Проверяем что имя не пустое и является строкой
        if not name or not isinstance(name, str):
            raise ValueError("Некорректное имя пакета")
        # Возвращаем очищенное от пробелов имя
        return name.strip()

    # Статический метод для проверки версии пакета
    @staticmethod
    def check_version(version):
        # Проверяем что версия указана
        if not version:
            raise ValueError("Версия пакета не указана")
        # Возвращаем очищенную от пробелов версию
        return version.strip()

    # Статический метод для проверки имени выходного файла
    @staticmethod
    def check_output_file(filename):
        # Проверяем что имя файла не пустое
        if not filename:
            raise ValueError("Имя файла не может быть пустым")
        # Список разрешенных расширений файлов
        allowed = ('.png', '.jpg', '.jpeg', '.svg', '.pdf')
        # Проверяем что файл имеет разрешенное расширение
        if not filename.lower().endswith(allowed):
            raise ValueError("Неподдерживаемый формат файла")
        # Возвращаем очищенное имя файла
        return filename.strip()

    # Статический метод для проверки режима ASCII
    @staticmethod
    def check_ascii_mode(mode):
        # Допустимые значения режима
        valid_modes = {'enabled', 'disabled', 'true', 'false'}
        # Очищаем и приводим к нижнему регистру
        clean_mode = mode.strip().lower()
        # Проверяем что режим допустимый
        if clean_mode not in valid_modes:
            raise ValueError("Недопустимый режим ASCII")
        # Возвращаем проверенный режим
        return clean_mode

    # Статический метод для проверки глубины анализа
    @staticmethod
    def check_depth(depth):
        try:
            # Пытаемся преобразовать в целое число
            depth_val = int(depth)
            # Проверяем что значение положительное
            if depth_val <= 0:
                raise ValueError("Глубина должна быть положительной")
            # Возвращаем проверенное значение
            return depth_val
        except (ValueError, TypeError):
            # Обрабатываем ошибки преобразования типов
            raise ValueError("Глубина должна быть целым числом")

    # Статический метод для проверки URL репозитория
    @staticmethod
    def check_repository_url(url):
        # Проверяем что URL не пустой и является строкой
        if not url or not isinstance(url, str):
            raise ValueError("Некорректный URL репозитория")
        # Очищаем URL от пробелов
        clean_url = url.strip()
        # Базовая проверка формата URL
        if not clean_url.startswith(('http://', 'https://', 'file://', '/')):
            raise ValueError("Некорректный формат URL репозитория")
        return clean_url

    # Статический метод для проверки режима тестирования
    @staticmethod
    def check_test_mode(mode):
        # Допустимые значения режима тестирования
        valid_modes = {'true', 'false', 'enabled', 'disabled', 'yes', 'no'}
        # Очищаем и приводим к нижнему регистру
        clean_mode = mode.strip().lower()
        # Проверяем что режим допустимый
        if clean_mode not in valid_modes:
            raise ValueError("Недопустимый режим тестирования")
        # Возвращаем проверенный режим
        return clean_mode


# Класс для парсинга конфигурационных файлов
class ConfigurationParser:
    """Парсер конфигурационных файлов"""

    # Конструктор класса
    def __init__(self):
        # Список обязательных параметров конфигурации
        self.required_params = [
            'package_name',  # Имя пакета
            'package_version',  # Версия пакета
            'output_filename',  # Имя выходного файла
            'ascii_tree_mode',  # Режим ASCII дерева
            'max_depth',  # Максимальная глубина
            'repository_url',  # URL репозитория
            'test_mode'  # Режим тестирования
        ]

    # Основной метод парсинга конфигурации
    def parse_configuration(self, file_path='config.csv'):
        """Основной метод парсинга конфигурации"""
        # Проверяем существование файла
        self._verify_file_existence(file_path)
        # Извлекаем данные конфигурации из файла
        config_data = self._extract_config_data(file_path)
        # Обрабатываем и возвращаем значения конфигурации
        return self._process_config_values(config_data)

    # Внутренний метод для проверки существования файла
    def _verify_file_existence(self, path):
        """Проверяет наличие файла"""
        # Если файл не существует, вызываем исключение
        if not os.path.exists(path):
            raise FileNotFoundError(f"Конфигурационный файл {path} не найден")

    # Внутренний метод для извлечения данных из CSV файла
    def _extract_config_data(self, path):
        """Извлекает данные из CSV файла"""
        try:
            # Открываем файл для чтения с кодировкой UTF-8
            with open(path, 'r', encoding='utf-8') as file:
                # Создаем DictReader для чтения CSV
                reader = csv.DictReader(file)
                # Читаем все строки в список
                rows = [row for row in reader]

                # Проверяем что файл не пустой
                if not rows:
                    raise ValueError("Файл конфигурации пуст")

                # Возвращаем проверенную первую строку
                return self._validate_config_row(rows[0])

        except csv.Error as e:
            # Обрабатываем ошибки чтения CSV
            raise ValueError(f"Ошибка чтения CSV: {e}")

    # Внутренний метод для проверки наличия всех обязательных полей
    def _validate_config_row(self, row):
        """Проверяет наличие всех необходимых полей"""
        # Проверяем каждое обязательное поле
        for field in self.required_params:
            # Если поле отсутствует, вызываем исключение
            if field not in row:
                raise ValueError(f"Отсутствует поле: {field}")
        # Возвращаем проверенную строку
        return row

    # Внутренний метод для обработки и валидации значений
    def _process_config_values(self, raw_data):
        """Обрабатывает и валидирует значения параметров"""
        # Создаем экземпляр валидатора
        validator = SettingsValidator()

        # Создаем словарь с обработанными и проверенными значениями
        processed_config = {
            'package_name': validator.check_package_name(raw_data['package_name']),
            'package_version': validator.check_version(raw_data['package_version']),
            'output_filename': validator.check_output_file(raw_data['output_filename']),
            'ascii_tree_mode': validator.check_ascii_mode(raw_data['ascii_tree_mode']),
            'max_depth': validator.check_depth(raw_data['max_depth']),
            'repository_url': validator.check_repository_url(raw_data['repository_url']),
            'test_mode': validator.check_test_mode(raw_data['test_mode'])
        }

        # Возвращаем обработанную конфигурацию
        return processed_config