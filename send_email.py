""" Работа с SMTP-сервером, формирование и отправка email'ов. """

import mimetypes
from pathlib import Path
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

from config import HOST, PORT


def connect_to_server(login: str, password: str) -> SMTP:
    """ Подключается к SMTP-серверу и возвращает объект подключения. """
    server = SMTP(HOST, PORT)
    server.starttls()
    server.login(login, password)
    return server


def get_message(path_to_files: str | Path) -> MIMEMultipart:
    """ Формирует и возвращает объект сообщения. """
    message = MIMEMultipart()
    message["Subject"] = 'Сообщение от Email_bot'

    for file_path in path_to_files.iterdir():
        _message_attach(file_path, message)
    return message


def send_email(sender: str, recipient: str, password: str,
               message: MIMEMultipart):
    """ Подключается к серверу и оправляет сообщение. """
    with connect_to_server(sender, password) as server:
        server.sendmail(sender, recipient, message.as_string())


def _message_attach(path_to_file: str | Path, message: MIMEMultipart):
    """ Прикрепляет файл к message. """
    file_name = Path(path_to_file).name
    file_type, subtype = mimetypes.guess_type(file_name)[0].split('/')
    match file_type:
        case 'text':
            message.attach(_get_MIMEText(path_to_file))
        case 'image':
            message.attach(_get_MIMEImage(path_to_file, subtype))


def _get_MIMEText(path_to_file: str | Path) -> MIMEText:
    """ Читает текст из файла и возвращает его в виде MIMEText. """
    with open(path_to_file) as file:
        return MIMEText(file.read())


def _get_MIMEImage(path_to_file: str | Path, subtype: str) -> MIMEImage:
    """ Считывает изображение из файла и возвращает его в виде MIMEImage. """
    with open(path_to_file, "rb") as file:
        attached_file = MIMEImage(file.read(), subtype)
    attached_file.add_header('content-disposition', 'attachment',
                             filename=Path(path_to_file).name)
    return attached_file
