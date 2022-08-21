""" Непосредственно сам telegram-бот. """

from aiogram import Bot, Dispatcher, executor, types

import files
import config
from middlewares import AccessMiddleware
from keyboards import markup
from send_email import send_email, get_message

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(config.MY_ID))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """ Отправляет сообщение приветствия/помощи. """
    await message.answer(
        "Бот для отправки email'ов"
        "Чтобы отправить email, пришли мне фото/текст\n"
        "/send чтобы отправить email сообщение,\n"
        "/cancel чтобы отменить отправку и сформировать сообщение заново.\n\n"
        "А также: \n"
        "/sender - изменить отправителя,\n"
        "/receiver -  изменить получателя,\n"
        "/password - изменить пароль.\n"
    )


@dp.message_handler(commands=['send'])
async def send(message: types.Message):
    """ Формирует email сообщение из загруженных данных и отправляет его. """
    if list(config.DOWNLOAD_PATH.iterdir()):  # Если папка с файлами не пуста
        msg = await bot.send_message(message.from_user.id, "Отправка...")
        email_message = get_message(config.DOWNLOAD_PATH)
        send_email(config.SENDER,
                   config.RECEIVER,
                   config.PASSWORD,
                   email_message)
        await msg.edit_text("Отправлено ✅")
        files.clear_folder(config.DOWNLOAD_PATH)
    else:  # Если папка пуста и отправлять нечего
        await bot.send_message(message.from_user.id, "Нечего отправлять 🤷‍♀\n"
                                                     "Пришли мне что-нибудь "
                                                     "и тогда я отправлю это.")


@dp.message_handler(commands=['cancel'])
async def cancel_sending(message: types.Message):
    """ Стирает все внесенные в email сообщение данные. """
    files.clear_folder(config.DOWNLOAD_PATH)
    await bot.send_message(message.from_user.id, "Сообщение отменено ❌")


@dp.message_handler(commands=['sender'])
async def set_sender(message: types.Message):
    """ Изменяет значение эл. почты отправителя. """
    if len(message.text.split()) == 2:
        config.SENDER = message.text.split()[1]
        await bot.send_message(message.from_user.id, "Отправитель изменен ✅")
    else:
        await bot.send_message(message.from_user.id,
                               "Неверный формат команды ❌\n"
                               "Введи /sender и email отправителя.\n"
                               "Например, /sender name@email.com")


@dp.message_handler(commands=['receiver'])
async def set_receiver(message: types.Message):
    """ Изменяет значение эл. почты получателя. """
    if len(message.text.split()) == 2:
        config.RECEIVER = message.text.split()[1]
        await bot.send_message(message.from_user.id, "Получатель изменен ✅")
    else:
        await bot.send_message(message.from_user.id,
                               "Неверный формат команды ❌\n"
                               "Введи /receiver и email получателя.\n"
                               "Например, /receiver name@email.com")


@dp.message_handler(commands=['password'])
async def set_password(message: types.Message):
    """ Изменяет пароль от эл. почты отправителя. """
    if len(message.text.split()) == 2:
        config.PASSWORD = message.text.split()[1]
        await bot.send_message(message.from_user.id, "Пароль изменен ✅")
    else:
        await bot.send_message(message.from_user.id,
                               "Неверный формат команды ❌\n"
                               "Введи /password и пароль отправителя.\n"
                               "Например, /password 12345678")


@dp.message_handler(content_types=['photo'])
async def download_photo(message: types.Message):
    """ Загружает изображения. """
    if message.caption:
        files.download_text(message.caption,
                            config.DOWNLOAD_PATH / 'message_text.txt')
        await bot.send_message(message.from_user.id, "Текст загружен")

    image_id = message.photo[-1].file_id
    image = await bot.get_file(image_id)
    image_path = image.file_path
    download_path = config.DOWNLOAD_PATH / files.get_name_for_file('png')
    await bot.download_file(image_path, download_path)
    await bot.send_message(message.from_user.id, "Фото загружено",
                           reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def download_text(message: types.Message):
    """ Загружает текст в файл. """
    files.download_text(message.text,
                        config.DOWNLOAD_PATH / 'message_text.txt')
    await bot.send_message(message.from_user.id, "Текст записан",
                           reply_markup=markup)


if __name__ == '__main__':
    files.make_dir(config.DOWNLOAD_PATH)
    executor.start_polling(dp, skip_updates=True)
