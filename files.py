""" Работа с файлами - их создание, изменение, удаление. """

import os
from pathlib import Path
from datetime import datetime


def get_name_for_file(extension: str) -> str:
    """ Генерирует имя для файла в виде текущей даты и времени. """
    name = f'{datetime.now().strftime("%y%m%d_%H%M%S_%f")}.{extension}'
    return name


def clear_folder(path: str | Path):
    """ Удаляет все файлы из папки. """
    for file in os.listdir(path):
        os.remove(Path(path, str(file)))


def download_text(text: str | None, path_to_text: str | Path):
    """ Записывает/дозаписывает текст в файл. """
    with open(path_to_text, 'a') as file:
        file.write(f'{text}\n')


def download_image(image: bytes, path_to_image: str | Path):
    """ Загружает изображение в файл. """
    with open(path_to_image, 'wb') as file:
        file.write(image)


def make_dir(path: str | Path):
    """ Создаёт папку по указанному пути. """
    Path(path).mkdir(parents=True, exist_ok=True)
