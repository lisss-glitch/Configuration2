import csv
import sys
import os


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
    if not os.path.exists(file_path):
        print(f"Error: Config file {file_path} not found")
        return None

    config = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                param_name = row.get('parameter', '').strip()
                param_value = row.get('value', '').strip()

                if param_name:
                    config[param_name] = param_value

        return config

    except Exception as e:
        print(f"Error reading config file: {e}")
        return None


def validate_config(config, validator):
    errors = []

    # Check for missing parameters
    for param in validator.required_params:
        if param not in config:
            errors.append(f"Missing required parameter: {param}")

    # Validate each parameter
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


def print_config(config):
    print("Configuration parameters:")
    for param, value in config.items():
        print(f"  {param}: {value}")


def main():
    # Use config.csv by default if no argument provided
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = "config.csv"
        print(f"Using default config file: {config_file}")

    validator = ConfigValidator()

    config = read_config_file(config_file)
    if config is None:
        sys.exit(1)

    errors = validate_config(config, validator)

    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    print_config(config)
    print("Configuration is valid")


if __name__ == "__main__":
    main()