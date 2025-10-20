import configparser
import os
from functools import wraps


def main():
    file_path = 'config.ini'

    create_default_config_file(file_path)
    modify_config_file(file_path)

    read_config_file(file_path)


def create_default_config_file(file_path):
    config = configparser.ConfigParser()

    config["database"] = {
        "host": "localhost",
        "port": "5432",
        "user": "admin"
    }
    config["settings"] = {
        "debug": "True",
        "log_level": "INFO"
    }

    with open(file_path, "w", encoding="utf-8") as f:
        config.write(f)


def modify_config_file(file_path):
    config = configparser.ConfigParser()
    config.read(file_path, encoding="utf-8")

    config["settings"]["timeout"] = "30"
    config["Paths"] = {
        "home": "/usr/local/app"
    }

    with open(file_path, "w", encoding="utf-8") as f:
        config.write(f)


def check_file_exists(func):
    @wraps(func)
    def wrapper(file_path):
        if not os.path.exists(file_path):
            print(f"Не существует файла с заданным путем: {file_path}")
            return
        return func(file_path)

    return wrapper


@check_file_exists
def read_config_file(file_path):
    config = configparser.ConfigParser()
    config.read(file_path, encoding="utf-8")

    if not is_data_valid(config):
        print('Данные некорректны')
        return

    for section in config.sections():
        print(f"\nСекция [{section}]")
        print("-" * 30)
        for key, value in config.items(section):
            print(f"{key} = {value}")
        print("-" * 30)


def is_data_valid(config):
    return (
        config["database"].get("host")
        and config["database"].get("user")
        and config["database"]["port"].isdigit()
        and config["settings"]["debug"].capitalize() in ('True', 'False')
    )


if __name__ == "__main__":
    main()
