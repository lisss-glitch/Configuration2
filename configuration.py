import csv
import sys
import os
import json
import urllib.request
import urllib.error


class ConfigValidator:
    def __init__(self):
        self.required_params = [
            "package_name",
            "repository_url",
            "test_repo_mode",
            "package_version",
            "output_image",
            "ascii_tree",
            "max_depth"
        ]

    def validate_package_name(self, value):
        if not value.strip():
            return "Package name cannot be empty"
        return None

    def validate_repository_url(self, value):
        if not value.strip():
            return "Repository URL cannot be empty"
        return None

    def validate_test_repo_mode(self, value):
        normalized_value = value.lower()
        if normalized_value not in ["true", "false"]:
            return "test_repo_mode must be 'true' or 'false'"
        return None

    def validate_package_version(self, value):
        if not value.strip():
            return "Package version cannot be empty"
        return None

    def validate_output_image(self, value):
        if not value.strip():
            return "Output image filename cannot be empty"
        forbidden_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        if any(char in value for char in forbidden_chars):
            return "Filename contains invalid characters"
        return None

    def validate_ascii_tree(self, value):
        normalized_value = value.lower()
        if normalized_value not in ["true", "false"]:
            return "ascii_tree must be 'true' or 'false'"
        return None

    def validate_max_depth(self, value):
        try:
            depth = int(value)
            if depth <= 0:
                return "max_depth must be positive integer"
        except ValueError:
            return "max_depth must be integer"
        return None


def read_config_file(file_path):
    """Читает CSV конфигурационный файл"""
    if not os.path.exists(file_path):
        print(f"Error: Config file '{file_path}' not found")
        print("Please check if the file exists and the path is correct.")
        return None

    config = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if not row or len(row) < 2 or row[0].strip().startswith('#'):
                    continue
                param_name = row[0].strip()
                param_value = row[1].strip()
                config[param_name] = param_value
        return config
    except Exception as e:
        print(f"Error reading config file: {e}")
        return None


def validate_config(config, validator):
    errors = []
    for param in validator.required_params:
        if param not in config:
            errors.append(f"Missing required parameter: {param}")

    validation_methods = {
        "package_name": validator.validate_package_name,
        "repository_url": validator.validate_repository_url,
        "test_repo_mode": validator.validate_test_repo_mode,
        "package_version": validator.validate_package_version,
        "output_image": validator.validate_output_image,
        "ascii_tree": validator.validate_ascii_tree,
        "max_depth": validator.validate_max_depth
    }

    for param_name, validation_func in validation_methods.items():
        if param_name in config:
            error = validation_func(config[param_name])
            if error:
                errors.append(f"{param_name}: {error}")

    return errors


def parse_simple_toml(file_path):
    """Парсит зависимости из TOML файла для тестового режима"""
    if not os.path.exists(file_path):
        print(f"Error: TOML file '{file_path}' not found")
        return None

    dependencies = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            in_dependencies_section = False
            found_dependencies = False

            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line == '[dependencies]':
                    in_dependencies_section = True
                    continue
                if line.startswith('[') and in_dependencies_section:
                    break
                if in_dependencies_section and '=' in line:
                    dep_name = line.split('=')[0].strip()
                    dependencies.append(dep_name)
                    found_dependencies = True

        if not found_dependencies:
            print("No dependencies found in TOML file")

        return dependencies
    except Exception as e:
        print(f"Error parsing TOML file: {e}")
        return None


def get_cargo_dependencies_from_crates_io(package_name, package_version):
    """Получает зависимости через API crates.io"""
    try:
        # Получаем зависимости для конкретной версии
        deps_url = f"https://crates.io/api/v1/crates/{package_name}/{package_version}/dependencies"

        req = urllib.request.Request(
            deps_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
        )

        with urllib.request.urlopen(req) as deps_response:
            deps_data = json.loads(deps_response.read().decode('utf-8'))

        # Извлекаем имена зависимостей
        dependencies = []
        if 'dependencies' in deps_data:
            for dep in deps_data['dependencies']:
                # Берем только обычные зависимости (не dev/build)
                if dep.get('kind') in [None, 'normal']:
                    dependencies.append({
                        'name': dep['crate_id'],
                        'version': dep.get('req', '*')
                    })

        return dependencies

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Package '{package_name}' version '{package_version}' not found on crates.io")
            return None
        else:
            print(f"HTTP Error {e.code}: {e.reason}")
            return None
    except urllib.error.URLError as e:
        print(f"Network error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def get_all_dependencies_recursive(package_name, package_version, test_repo_mode, max_depth, current_depth=1,
                                   visited=None):
    """Рекурсивно получает все зависимости до указанной глубины"""
    if visited is None:
        visited = set()

    if current_depth > max_depth:
        return {}

    # Создаем ключ для отслеживания пакетов с версиями
    package_key = f"{package_name}@{package_version}"
    if package_key in visited:
        return {}
    visited.add(package_key)

    # Получаем прямые зависимости
    if test_repo_mode.lower() == "true":
        # В тестовом режиме возвращаем пустые зависимости для всех кроме корневого пакета
        if current_depth == 1:
            direct_deps = parse_simple_toml(package_name)  # В тестовом режиме package_name - это путь к файлу
            if direct_deps is None:
                return {}
            # Преобразуем в формат словаря для единообразия
            direct_deps_dict = [{'name': dep, 'version': '*'} for dep in direct_deps]
        else:
            direct_deps_dict = []
    else:
        direct_deps_dict = get_cargo_dependencies_from_crates_io(package_name, package_version)
        if direct_deps_dict is None:
            return {}

    result = {package_name: direct_deps_dict}

    # Рекурсивно получаем зависимости для каждой зависимости
    for dep in direct_deps_dict:
        # Для простоты используем ту же версию, что указана в требовании, или последнюю доступную
        dep_name = dep['name']
        dep_version = extract_version(dep['version']) or package_version

        sub_deps = get_all_dependencies_recursive(
            dep_name, dep_version, test_repo_mode,
            max_depth, current_depth + 1, visited
        )
        result.update(sub_deps)

    return result


def extract_version(version_req):
    """Извлекает версию из требования версии"""
    import re
    match = re.search(r'[\d]+\.[\d]+\.[\d]+', version_req)
    return match.group(0) if match else "1.0.0"


def print_dependency_tree(dependencies_tree, package_name, current_depth=0, is_last=True, parent_prefix=""):
    """Выводит дерево зависимостей в ASCII формате"""
    if current_depth == 0:
        print(package_name)

    deps = dependencies_tree.get(package_name, [])
    count = len(deps)

    for i, dep in enumerate(deps):
        is_last_dep = (i == count - 1)

        if current_depth == 0:
            prefix = "└── " if is_last_dep else "├── "
        else:
            prefix = parent_prefix + ("└── " if is_last else "├── ")

        connector = "    " if is_last_dep else "│   "

        print(f"{prefix}{dep['name']} {dep['version']}")

        # Рекурсивно выводим поддерево
        if dep['name'] in dependencies_tree:
            print_dependency_tree(
                dependencies_tree, dep['name'], current_depth + 1,
                is_last_dep, parent_prefix + connector
            )


def print_dependencies_flat(dependencies_tree, package_name):
    """Выводит зависимости в плоском формате"""
    for pkg, deps in dependencies_tree.items():
        if pkg == package_name:
            print(f"\nDirect dependencies for {package_name}:")
        else:
            print(f"\nDependencies for {pkg}:")

        if deps:
            for i, dep in enumerate(deps, 1):
                print(f"  {i}. {dep['name']} {dep['version']}")
        else:
            print("  (no dependencies)")


def main():
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        print(f"Using config file: {config_file}")
    else:
        config_file = "configuration.csv"
        print(f"Using default config file: {config_file}")

    validator = ConfigValidator()
    config = read_config_file(config_file)

    if config is None:
        print("Failed to read configuration. Exiting.")
        sys.exit(1)

    errors = validate_config(config, validator)
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)


    # Этап 2: Получение зависимостей
    print("\n=== Stage 2: Dependency Collection ===")

    package_name = config.get("package_name")
    repository_url = config.get("repository_url")
    test_repo_mode = config.get("test_repo_mode")
    package_version = config.get("package_version")
    ascii_tree = config.get("ascii_tree", "false").lower() == "true"
    max_depth = int(config.get("max_depth", 3))

    print(f"Searching for dependencies of '{package_name}' version '{package_version}'...")

    # Получаем все зависимости рекурсивно
    all_dependencies = get_all_dependencies_recursive(
        package_name, package_version, test_repo_mode, max_depth
    )

    if not all_dependencies:
        print(f"No dependencies found for package '{package_name}' version '{package_version}'")
        print("This could mean:")
        print("  - The package doesn't exist")
        print("  - The version doesn't exist")
        print("  - The package has no dependencies")
        print("  - There was a network error")
        sys.exit(1)

    if ascii_tree:
        print(f"\nDependency tree for package '{package_name}' version '{package_version}' (max depth: {max_depth}):")
        print_dependency_tree(all_dependencies, package_name)
    else:
        print(f"\nAll dependencies for package '{package_name}' version '{package_version}' (max depth: {max_depth}):")
        print_dependencies_flat(all_dependencies, package_name)

    total_deps = sum(len(deps) for deps in all_dependencies.values())
    unique_packages = len(all_dependencies)
    print(f"\nSummary:")
    print(f"  Total dependencies found: {total_deps}")
    print(f"  Total unique packages in tree: {unique_packages}")

    print("Stage 2 completed successfully")


if __name__ == "__main__":
    main()