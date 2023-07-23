import os

from dotenv import load_dotenv

# Загрузка переменных из файла .env для локального запуска тестов
load_dotenv()


class UserData:
    LOGIN = "test@test.ru"
    PASSWORD = "123qwe"
    NAME = "test_user"


DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE'))
