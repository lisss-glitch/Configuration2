import csv  # модуль для работы с CSV-файлами
import sys  # модуль для работы с аргументами командной строки
import os   # модуль для работы с файловой системой
import collections  # модуль для специальных структур данных

class DependencyGraph:
    """Класс для представления графа зависимостей"""

    def __init__(self):
        self.graph = collections.defaultdict(list)  # граф в виде словаря: пакет -> список зависимостей
        self.cycles = []  # список для хранения обнаруженных циклов
        self.all_packages = set()  # множество всех пакетов в системе

    def build_from_file(self, file_path):
        """Строит граф из файла зависимостей"""
        if not os.path.exists(file_path):  # проверка существования файла
            print(f"Ошибка: Файл '{file_path}' не найден!")
            return False

        print(f"Анализируем файл {file_path}...")

        try:
            with open(file_path, 'r', encoding='utf-8') as file:  # открытие файла для чтения
                for line_num, line in enumerate(file, 1):  # чтение файла построчно с нумерацией
                    line = line.strip()  # удаление пробелов в начале и конце строки
                    if not line or line.startswith('#'):  # пропуск пустых строк и комментариев
                        continue

                    if ':' in line:  # обработка формата "A: B, C"
                        parts = line.split(':', 1)  # разделение по первому вхождению ':'
                    elif '->' in line:  # обработка формата "A -> B, C"
                        parts = line.split('->', 1)  # разделение по первому вхождению '->'
                    else:  # пропуск строк некорректного формата
                        continue

                    if len(parts) != 2:  # проверка корректности разделения
                        print(f"Предупреждение: Неверный формат в строке {line_num}: {line}")
                        continue

                    package = parts[0].strip()  # извлечение имени пакета
                    deps_str = parts[1].strip()  # извлечение строки зависимостей

                    if not self._is_valid_package_name(package):  # валидация имени пакета
                        print(f"Предупреждение: Неверное имя пакета в строке {line_num}: {package}")
                        continue

                    self.all_packages.add(package)  # добавление пакета в общее множество

                    dep_list = []  # список зависимостей текущего пакета
                    if deps_str:  # обработка зависимостей, если они есть
                        for dep in deps_str.split(','):  # разделение зависимостей по запятым
                            dep = dep.strip()  # очистка от пробелов
                            if dep and self._is_valid_package_name(dep):  # проверка валидности зависимости
                                dep_list.append(dep)  # добавление зависимости в список
                                self.all_packages.add(dep)  # добавление зависимости в общее множество

                    self.graph[package] = dep_list  # добавление пакета и его зависимостей в граф

            for package in self.all_packages:  # добавление пакетов без зависимостей в граф
                if package not in self.graph:  # если пакет не был добавлен ранее
                    self.graph[package] = []  # добавляем с пустым списком зависимостей

            print(f"Успешно загружено пакетов: {len(self.all_packages)}")  # вывод статистики
            return True

        except Exception as e:  # обработка ошибок чтения файла
            print(f"Ошибка при чтении файла: {e}")
            return False

    def _is_valid_package_name(self, name):
        """Проверяет что имя пакета состоит из заглавных латинских букв"""
        return name.isalpha() and name.isupper()  # имя должно содержать только заглавные буквы

    def get_load_order(self, package_name):
        """
        Возвращает порядок загрузки зависимостей для заданного пакета
        используя алгоритм топологической сортировки (Kahn's algorithm)
        """
        if package_name not in self.all_packages:  # проверка существования пакета
            print(f"Пакет '{package_name}' не найден в графе!")
            return None

        nodes = set()  # множество всех достижимых узлов
        stack = [package_name]  # стек для обхода в глубину
        while stack:  # обход графа в глубину
            node = stack.pop()  # извлечение узла из стека
            if node not in nodes:  # если узел еще не посещен
                nodes.add(node)  # добавляем узел в посещенные
                for dep in self.graph.get(node, []):  # для каждой зависимости узла
                    if dep not in nodes:  # если зависимость еще не посещена
                        stack.append(dep)  # добавляем зависимость в стек

        reverse_graph = collections.defaultdict(list)  # обратный граф для топологической сортировки
        for node in nodes:  # построение обратного графа
            for dep in self.graph.get(node, []):  # для каждой зависимости
                if dep in nodes:  # если зависимость в множестве достижимых узлов
                    reverse_graph[dep].append(node)  # добавляем обратную связь

        in_degree = {node: 0 for node in nodes}  # словарь входящих степеней узлов
        for node in nodes:  # вычисление входящих степеней
            for dep in self.graph.get(node, []):  # для каждой зависимости
                if dep in nodes:  # если зависимость в множестве достижимых узлов
                    in_degree[dep] += 1  # увеличиваем входящую степень зависимости

        queue = collections.deque()  # очередь для алгоритма Кана
        for node in nodes:  # поиск узлов без входящих зависимостей
            if in_degree[node] == 0:  # если у узла нет входящих зависимостей
                queue.append(node)  # добавляем узел в очередь

        load_order = []  # результирующий порядок загрузки
        while queue:  # пока очередь не пуста
            node = queue.popleft()  # извлекаем узел из начала очереди
            load_order.append(node)  # добавляем узел в порядок загрузки
            for neighbor in reverse_graph.get(node, []):  # для каждого соседа в обратном графе
                in_degree[neighbor] -= 1  # уменьшаем входящую степень соседа
                if in_degree[neighbor] == 0:  # если у соседа больше нет входящих зависимостей
                    queue.append(neighbor)  # добавляем соседа в очередь

        if len(load_order) != len(nodes):  # проверка на циклические зависимости
            print("Обнаружены циклические зависимости! Невозможно определить порядок загрузки.")
            return None

        return load_order  # возврат порядка загрузки

    def print_load_order_analysis(self, package_name):
        """Выводит полный анализ порядка загрузки для заданного пакета"""
        print("\n" + "=" * 60)  # разделитель
        print(f"АНАЛИЗ ПОРЯДКА ЗАГРУЗКИ ДЛЯ ПАКЕТА: {package_name}")  # заголовок
        print("=" * 60)

        load_order = self.get_load_order(package_name)  # получение порядка загрузки

        if load_order is None:  # если порядок загрузки не определен
            return False

        print(f"Найдено зависимостей для '{package_name}': {len(load_order)} пакетов")  # статистика

        print("\nПОРЯДОК ЗАГРУЗКИ ЗАВИСИМОСТЕЙ:")  # заголовок раздела
        print("-" * 40)  # разделитель
        for i, package in enumerate(load_order, 1):  # вывод порядка загрузки с нумерацией
            print(f"   {i}. {package}")  # вывод номера и имени пакета

        print("\nОБЪЯСНЕНИЕ ПОРЯДКА:")  # заголовок раздела
        print("-" * 40)  # разделитель
        print("Порядок основан на топологической сортировке графа зависимостей.")  # объяснение
        print("Каждый пакет загружается после всех своих зависимостей.")  # принцип работы
        print("Это гарантирует, что при загрузке пакета все его зависимости уже доступны.")  # преимущество

        print("\nСРАВНЕНИЕ С РЕАЛЬНЫМИ МЕНЕДЖЕРАМИ ПАКЕТОВ:")  # заголовок раздела
        print("-" * 40)  # разделитель
        print("В реальных менеджерах пакетов могут быть расхождения из-за:")  # предупреждение
        print("  1. Учета версий зависимостей")  # фактор 1
        print("  2. Разрешения конфликтов версий")  # фактор 2
        print("  3. Оптимизации для параллельной загрузки")  # фактор 3
        print("  4. Учета дополнительных метаданных пакетов")  # фактор 4
        print("  5. Поддержки альтернативных зависимостей")  # фактор 5
        print("  6. Кэширования уже загруженных пакетов")  # фактор 6

        print("\nВЕРОЯТНЫЕ РАСХОЖДЕНИЯ:")  # заголовок раздела
        print("-" * 40)  # разделитель
        print("Cargo (Rust): Может объединять одинаковые версии зависимостей")  # пример для Cargo
        print("npm (Node.js): Использует плоскую структуру node_modules")  # пример для npm
        print("pip (Python): Учитывает совместимость версий Python")  # пример для pip
        print("Maven (Java): Учитывает scope зависимостей (compile/test/runtime)")  # пример для Maven

        return True  # успешное завершение


def main():
    """Основная функция программы"""
    if len(sys.argv) != 2:  # проверка количества аргументов командной строки
        print("Использование: python config4.py <конфигурационный_файл.csv>")  # инструкция
        print("   Пример: python config4.py configuration4_simple.csv")  # пример использования
        sys.exit(1)  # завершение программы с ошибкой

    config_file = sys.argv[1]  # получение имени конфигурационного файла

    if not os.path.exists(config_file):  # проверка существования файла
        print(f"Конфигурационный файл '{config_file}' не найден!")  # сообщение об ошибке
        sys.exit(1)  # завершение программы с ошибкой

    print("ЗАПУСК ЭТАПА 4: АНАЛИЗ ПОРЯДКА ЗАГРУЗКИ ЗАВИСИМОСТЕЙ")  # заголовок этапа
    print("=" * 60)  # разделитель

    config = {}  # словарь для хранения конфигурации
    try:
        with open(config_file, 'r', encoding='utf-8') as file:  # открытие конфигурационного файла
            reader = csv.reader(file)  # создание CSV-ридера
            for row in reader:  # чтение файла построчно
                if not row or len(row) < 2 or row[0].strip().startswith('#'):  # пропуск некорректных строк
                    continue
                param_name = row[0].strip()  # извлечение имени параметра
                param_value = row[1].strip()  # извлечение значения параметра
                config[param_name] = param_value  # сохранение параметра в словаре
    except Exception as e:  # обработка ошибок чтения
        print(f"Ошибка чтения конфигурационного файла: {e}")  # сообщение об ошибке
        sys.exit(1)  # завершение программы с ошибкой

    required_params = ["package_name", "repository_url", "test_repo_mode"]  # обязательные параметры
    missing_params = [param for param in required_params if param not in config]  # поиск отсутствующих параметров
    if missing_params:  # если есть отсутствующие параметры
        print(f"Отсутствуют обязательные параметры: {', '.join(missing_params)}")  # сообщение об ошибке
        sys.exit(1)  # завершение программы с ошибкой

    package_name = config.get("package_name")  # получение имени пакета для анализа
    repository_url = config.get("repository_url")  # получение пути к файлу зависимостей
    test_repo_mode = config.get("test_repo_mode")  # получение режима тестирования

    if test_repo_mode.lower() != "true":  # проверка режима тестирования
        print("Этап 4 требует test_repo_mode=true")  # сообщение об ошибке
        sys.exit(1)  # завершение программы с ошибкой

    print("ПАРАМЕТРЫ КОНФИГУРАЦИИ:")  # заголовок раздела
    print(f"   Пакет для анализа: {package_name}")  # вывод имени пакета
    print(f"   Файл зависимостей: {repository_url}")  # вывод пути к файлу
    print(f"   Режим тестирования: {test_repo_mode}")  # вывод режима тестирования

    print("\nПОСТРОЕНИЕ ГРАФА ЗАВИСИМОСТЕЙ...")  # сообщение о начале построения графа
    graph = DependencyGraph()  # создание объекта графа

    if not graph.build_from_file(repository_url):  # построение графа из файла
        print(f"Ошибка построения графа из файла: {repository_url}")  # сообщение об ошибке
        sys.exit(1)  # завершение программы с ошибкой

    success = graph.print_load_order_analysis(package_name)  # выполнение анализа порядка загрузки

    if success:  # если анализ завершен успешно
        print("\nАНАЛИЗ ЗАВЕРШЕН УСПЕШНО!")  # сообщение об успехе
    else:  # если анализ завершен с ошибками
        print("\nАНАЛИЗ ЗАВЕРШЕН С ОШИБКАМИ!")  # сообщение об ошибке
        sys.exit(1)  # завершение программы с ошибкой


if __name__ == "__main__":
    main()  # запуск основной функции при прямом вызове скрипта