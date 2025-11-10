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

Цель: реализовать основную логику получения данных о зависимостях для их
дальнейшего анализа и визуализации. Запрещено пользоваться менеджерами
пакетов и сторонними библиотеками для получения информации о зависимостях
пакетов.
Требования:
1. Использовать формат пакетов Rust (Cargo).
2. Информацию необходимо получить для заданной пользователем версии
пакета.
3. Извлечь информацию о прямых зависимостях заданного пользователем
пакета, используя URL-адрес репозитория.
4. (только для этого этапа) Вывести на экран все прямые зависимости
заданного пользователем пакета.
5. Результат выполнения этапа сохранить в репозиторий стандартно
оформленным коммитом.
