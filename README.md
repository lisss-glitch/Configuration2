Конфигуранционное управление
Практическая работа №2
Вариант №4
Этап 1.

1. Общее описание.
Разработать инструмент визуализации графа зависимостей для менеджера пакетов. Готовые средства (менеджеры пакетов, библиотеки) для получения зависимостей использовать нельзя.
2. Описание всех функций и настроек.
Модуль config.py
Класс SettingsValidator
Валидатор параметров конфигурации с методами:

check_package_name(name) - проверяет корректность имени пакета

check_version(version) - валидирует версию пакета

check_output_file(filename) - проверяет имя и формат выходного файла

check_ascii_mode(mode) - валидирует режим ASCII-дерева

check_depth(depth) - проверяет глубину анализа

check_repository_url(url) - валидирует URL репозитория

check_test_mode(mode) - проверяет режим тестирования

Класс ConfigurationParser
Парсер конфигурационных файлов с методами:

parse_configuration(file_path) - основной метод парсинга конфигурации

_verify_file_existence(path) - проверяет наличие файла

_extract_config_data(path) - извлекает данные из CSV файла

_validate_config_row(row) - проверяет наличие обязательных полей

_process_config_values(raw_data) - обрабатывает и валидирует значения

Модуль cli.py
Класс ApplicationCore
Основной класс приложения с методами:

process_arguments() - обрабатывает аргументы командной строки

initialize_settings(config_path) - инициализирует настройки приложения

perform_validation() - выполняет дополнительную валидацию

display_current_configuration() - отображает текущую конфигурацию

execute_application() - запускает основную логику приложения

3. Описание команд для сборки проекта и запуска тестов.

Установка зависимостей
# Пока зависимости не указаны, но при их добавлении:
pip install -r requirements.txt

Запуск приложения:
# Базовый запуск с конфигурацией по умолчанию
python main.py

# Запуск с указанием файла конфигурации
python main.py --settings-file my_config.csv

# Запуск в режиме проверки конфигурации
python main.py --verify

# Запуск с пользовательской конфигурацией
python main.py --settings-file custom_config.csv --verify

Запуск тестов

# Для запуска тестов (когда они будут добавлены)
python -m pytest tests/

# Запуск с покрытием кода
python -m pytest --cov=.

# Запуск конкретного тестового модуля
python -m pytest tests/test_config.py -v

4. Примеры использования.

Пример 1: Базовая конфигурация
<img width="959" height="57" alt="image" src="https://github.com/user-attachments/assets/4808f4e4-210b-4ab2-843a-ceb8623ba4cb" />

Запуск:
python main.py

Ожидаемый вывод:
<img width="640" height="292" alt="image" src="https://github.com/user-attachments/assets/8a4a1e2a-25bb-4bca-ba44-ebabc0994b65" />

Пример 2: Проверка конфигурации
python main.py --verify --settings-file config.csv

Ожидаемый вывод:
<img width="422" height="59" alt="image" src="https://github.com/user-attachments/assets/5fb0dee0-c2e5-4dab-a7a5-5cdd9fd94182" />

Пример 3: Локальный анализ
package_name,package_version,output_filename,ascii_tree_mode,max_depth,repository_url,test_mode
my_package,1.0.0,local_deps.svg,disabled,2,file:///path/to/local/repo,true

Запуск:
python main.py --settings-file local_config.csv

Пример 4: Глубокий анализ
deep_config.csv:
package_name,package_version,output_filename,ascii_tree_mode,max_depth,repository_url,test_mode
complex_lib,2.1.0,deep_analysis.pdf,enabled,5,https://crates.io/crates/complex_lib,false

Запуск:
python main.py --settings-file deep_config.csv

Этап 2. Сбор данных

1. Описание всех функций и настроек.
Описание всех функций и настроек
Модуль config.py
Класс SettingsValidator
Валидатор параметров конфигурации с методами:

check_package_name(name) - проверяет корректность имени пакета Rust

check_version(version) - валидирует версию пакета Cargo

check_output_file(filename) - проверяет имя и формат выходного файла

check_ascii_mode(mode) - валидирует режим ASCII-дерева

check_depth(depth) - проверяет глубину анализа зависимостей

check_repository_url(url) - валидирует URL репозитория (crates.io)

check_test_mode(mode) - проверяет режим тестирования

Класс ConfigurationParser
Парсер конфигурационных файлов с методами:

parse_configuration(file_path) - основной метод парсинга конфигурации

_verify_file_existence(path) - проверяет наличие файла конфигурации

_extract_config_data(path) - извлекает данные из CSV файла

_validate_config_row(row) - проверяет наличие обязательных полей

_process_config_values(raw_data) - обрабатывает и валидирует значения

Модуль dependency_analyzer.py
Класс DependencyAnalyzer
Основной анализатор зависимостей Rust с методами:

__init__(package_name, package_version, repository_url) - инициализация анализатора

extract_dependencies_from_cargo_toml(content) - извлекает зависимости из JSON API crates.io

fetch_cargo_toml_from_github() - получает информацию о пакете из crates.io API

analyze_dependencies() - основной метод анализа зависимостей

display_dependencies() - отображает найденные зависимости в структурированном виде

Модуль cli.py
Класс ApplicationCore
Основной класс приложения с расширенными методами:

process_arguments() - обрабатывает аргументы командной строки

initialize_settings(config_path) - инициализирует настройки приложения

perform_validation() - выполняет дополнительную валидацию

display_current_configuration() - отображает текущую конфигурацию

execute_dependency_analysis() - выполняет анализ зависимостей

execute_application() - запускает основную логику приложения

2. Команды для сборки проекта и запуска тестов

Установка зависимостей
# Пока зависимости не указаны, но при их добавлении:
pip install -r requirements.txt

Запуск приложения
# Базовый запуск с конфигурацией по умолчанию
python main.py

# Запуск с указанием файла конфигурации
python main.py --settings-file my_config.csv

# Запуск в режиме проверки конфигурации (без анализа)
python main.py --verify

# Запуск с пользовательской конфигурацией
python main.py --settings-file custom_config.csv --verify

Запуск тестов
# Для запуска тестов (когда они будут добавлены)
python -m pytest tests/

# Запуск с покрытием кода
python -m pytest --cov=.

# Запуск конкретного тестового модуля
python -m pytest tests/test_dependency_analyzer.py -v

Прямой запуск анализатора зависимостей
# Прямой запуск анализатора (для разработки)
python dependency_analyzer.py

3. Примеры использования
Пример 1: Анализ зависимостей пакета serde
config.csv:
<img width="979" height="63" alt="image" src="https://github.com/user-attachments/assets/4c4a0bdd-b951-426c-892c-8c5e8ac86b41" />
Запуск:
python main.py

Ожидаемый вывод:
<img width="830" height="833" alt="image" src="https://github.com/user-attachments/assets/66c12a46-a569-4b67-919a-2aa672f7dc07" />

Пример 2: Проверка конфигурации без выполнения анализа
python main.py --verify --settings-file config.csv

Ожидаемый вывод:
<img width="427" height="53" alt="image" src="https://github.com/user-attachments/assets/e10c62ee-3cc3-4051-9fab-704f833019f5" />

Пример 3: Анализ пакета requests с демонстрационными зависимостями
requests_config.csv:
package_name,package_version,output_filename,ascii_tree_mode,max_depth,repository_url,test_mode
requests,1.0.0,deps_analysis.svg,disabled,2,https://crates.io/crates/requests,false

Запуск:
python main.py --settings-file requests_config.csv

Ожидаемый вывод:
<img width="452" height="390" alt="image" src="https://github.com/user-attachments/assets/ec20f513-6859-4d72-a1b0-95568c435ba0" />
