import os
import collections


class DependencyGraph:
    """Класс для представления графа зависимостей"""

    def __init__(self):
        self.graph = collections.defaultdict(list)
        self.cycles = []
        self.all_packages = set()

    def build_from_file(self, file_path):
        """Строит граф из файла зависимостей"""
        if not os.path.exists(file_path):
            print(f"Ошибка: Файл '{file_path}' не найден!")
            return False

        print(f"Анализируем файл {file_path}...")

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    # Обрабатываем разные форматы: A: B, C или A -> B, C
                    if ':' in line:
                        parts = line.split(':', 1)
                    elif '->' in line:
                        parts = line.split('->', 1)
                    else:
                        # Если нет разделителя, считаем что это пакет без зависимостей
                        package = line.strip()
                        if package and self._is_valid_package_name(package):
                            self.graph[package] = []
                            self.all_packages.add(package)
                        continue

                    if len(parts) != 2:
                        print(f"Предупреждение: Неверный формат в строке {line_num}: {line}")
                        continue

                    package = parts[0].strip()
                    deps_str = parts[1].strip()

                    # Проверяем валидность имени пакета
                    if not self._is_valid_package_name(package):
                        print(f"Предупреждение: Неверное имя пакета в строке {line_num}: {package}")
                        continue

                    self.all_packages.add(package)

                    # Обрабатываем зависимости
                    dep_list = []
                    if deps_str:
                        # Убираем квадратные скобки если есть
                        if deps_str.startswith('[') and deps_str.endswith(']'):
                            deps_str = deps_str[1:-1]

                        for dep in deps_str.split(','):
                            dep = dep.strip()
                            if dep and self._is_valid_package_name(dep):
                                dep_list.append(dep)
                                self.all_packages.add(dep)

                    self.graph[package] = dep_list

            # Добавляем пакеты без зависимостей в граф
            for package in self.all_packages:
                if package not in self.graph:
                    self.graph[package] = []

            return True

        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return False

    def _is_valid_package_name(self, name):
        """Проверяет что имя пакета состоит из заглавных латинских букв"""
        return name.isalpha() and name.isupper()

    def dfs_traversal(self, start_package, max_depth, current_depth=0, visited=None, path=None):
        """Обход графа в глубину с ограничением по глубине и обнаружением циклов"""
        if visited is None:
            visited = set()
        if path is None:
            path = []

        if current_depth > max_depth:
            return []

        # Проверка на цикл
        if start_package in path:
            cycle = path[path.index(start_package):] + [start_package]
            cycle_str = " -> ".join(cycle)
            if cycle_str not in self.cycles:
                self.cycles.append(cycle_str)
            return []

        if start_package in visited:
            return []

        visited.add(start_package)
        path.append(start_package)

        result = [start_package]

        # РЕКУРСИВНЫЙ DFS ВЫЗОВ
        for neighbor in self.graph.get(start_package, []):
            result.extend(self.dfs_traversal(
                neighbor, max_depth, current_depth + 1, visited, path.copy()
            ))

        path.pop()
        return result

    def find_all_cycles(self):
        """Находит все циклы в графе"""
        self.cycles = []
        for node in self.graph.keys():
            self._dfs_cycles(node, [], set())
        return self.cycles

    def _dfs_cycles(self, node, path, visited):
        """Вспомогательная функция для поиска циклов"""
        if node in path:
            cycle_start = path.index(node)
            cycle = path[cycle_start:] + [node]
            cycle_str = " -> ".join(cycle)
            if cycle_str not in self.cycles:
                self.cycles.append(cycle_str)
            return

        path.append(node)
        visited.add(node)

        for neighbor in self.graph.get(node, []):
            self._dfs_cycles(neighbor, path.copy(), visited)

    def print_analysis(self, max_depth=3):
        """Выводит полный анализ графа"""
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТЫ АНАЛИЗА ГРАФА ЗАВИСИМОСТЕЙ")
        print("=" * 50)

        # Выводим граф
        print("\n---")
        print("ПОЛНЫЙ ГРАФ ЗАВИСИМОСТЕЙ")
        print("---")
        for package in sorted(self.graph.keys()):
            deps = self.graph[package]
            print(f"{package} -> {deps}")

        print(f"\nВсего пакетов в графе: {len(self.all_packages)}")

        # Статистика
        print("\n---")
        print("СТАТИСТИКА ГРАФА")
        print("---")
        print(f"Найдено пакетов в файле: {len(self.all_packages)}")
        print(f"Обработано пакетов: {len(self.graph)}")

        total_deps = sum(len(deps) for deps in self.graph.values())
        print(f"Всего зависимостей: {total_deps}")

        # Поиск циклов
        self.find_all_cycles()
        if self.cycles:
            print(f"Обнаружено циклов: {len(self.cycles)}")
            print("\nОбнаруженные циклы:")
            for i, cycle in enumerate(self.cycles, 1):
                print(f"  {i}. {cycle}")
        else:
            print("Циклические зависимости: не обнаружены")

        # DFS обход для всех пакетов
        print(f"\n---")
        print(f"DFS ОБХОД ДЛЯ ВСЕХ ПАКЕТОВ (максимальная глубина: {max_depth})")
        print(f"---")

        for package in sorted(self.graph.keys()):
            # ВЫЗОВ DFS АЛГОРИТМА И ВЫВОД РЕЗУЛЬТАТА
            traversal_result = self.dfs_traversal(package, max_depth)
            print(f"{package}: {traversal_result}")


def interactive_mode():
    """Интерактивный режим работы"""
    print("ИНТЕРАКТИВНЫЙ РЕЖИМ АНАЛИЗА ГРАФА ЗАВИСИМОСТЕЙ")
    print("=" * 50)

    # Интерактивный ввод пути к файлу
    while True:
        file_path = input("\nВведите путь к файлу с описанием пакетов: ").strip()
        if os.path.exists(file_path):
            break
        else:
            print("Файл не найден! Попробуйте еще раз.")

    # Интерактивный ввод максимальной глубины
    while True:
        depth_input = input("📏 Введите максимальную глубину анализа (по умолчанию 3): ").strip()
        if not depth_input:
            max_depth = 3
            break
        try:
            max_depth = int(depth_input)
            if max_depth > 0:
                break
            else:
                print("Глубина должна быть положительным числом!")
        except ValueError:
            print("Введите целое число!")

    # Строим и анализируем граф
    print("\nПостроение графа зависимостей...")
    graph = DependencyGraph()

    if graph.build_from_file(file_path):
        print("Граф успешно построен!")
        graph.print_analysis(max_depth)
    else:
        print("Ошибка при построении графа!")


def file_selection_mode():
    """Режим выбора файла из списка доступных"""
    print("РЕЖИМ ВЫБОРА ФАЙЛА")
    print("=" * 50)

    # Ищем все txt файлы в текущей директории
    available_files = [f for f in os.listdir('.') if f.endswith('.txt') and os.path.isfile(f)]

    if not available_files:
        print("В текущей директории не найдено txt файлов!")
        return

    print("\nДоступные файлы:")
    for i, file in enumerate(available_files, 1):
        print(f"  {i}. {file}")

    # Интерактивный выбор файла
    while True:
        try:
            choice = input(f"\nВыберите файл (1-{len(available_files)}): ").strip()
            if not choice:
                continue

            choice_num = int(choice)
            if 1 <= choice_num <= len(available_files):
                selected_file = available_files[choice_num - 1]
                break
            else:
                print(f"Введите число от 1 до {len(available_files)}!")
        except ValueError:
            print("Введите число!")

    # Интерактивный ввод глубины
    while True:
        depth_input = input("Введите максимальную глубину анализа (по умолчанию 3): ").strip()
        if not depth_input:
            max_depth = 3
            break
        try:
            max_depth = int(depth_input)
            if max_depth > 0:
                break
            else:
                print("Глубина должна быть положительным числом!")
        except ValueError:
            print("Введите целое число!")

    # Строим и анализируем граф
    print(f"\nАнализируем файл {selected_file}...")
    graph = DependencyGraph()

    if graph.build_from_file(selected_file):
        print("Граф успешно построен!")
        graph.print_analysis(max_depth)
    else:
        print("Ошибка при построении графа!")


def main():
    """Основная функция программы"""
    print("=" * 60)
    print("           АНАЛИЗАТОР ГРАФОВ ЗАВИСИМОСТЕЙ")
    print("                 (Этап 3: DFS с рекурсией)")
    print("=" * 60)

    # Интерактивный выбор режима работы
    print("\nВыберите режим работы:")
    print("  1. Указать путь к файлу вручную")
    print("  2. Выбрать файл из списка доступных")
    print("  3. Выход")

    while True:
        choice = input("\nВаш выбор (1-3): ").strip()

        if choice == '1':
            interactive_mode()
            break
        elif choice == '2':
            file_selection_mode()
            break
        elif choice == '3':
            print("До свидания!")
            return
        else:
            print("Неверный выбор! Введите 1, 2 или 3.")


if __name__ == "__main__":
    main()