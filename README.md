# Email telegram bot
Telegram бот для простой отправки email сообщений.

## Сборка репозитория и локальный запуск
### Клонирование
Выполните в консоли:
```
git clone https://github.com/yakubanik/email-telegram-bot.git
pip install -r requirements.txt
```
### Настройка
В переменных окружения необходимо проставить:

`MY_ID` - id аккаунта, от которого будут приниматься сообщения<br/>
`TOKEN` - API токен бота<br/>
`SENDER` - email от которого отправляются сообщения по умолчанию<br/>
`PASSWORD` - пароль от email аккаунта отправителя<br/>
`RECEIVER` - email получателя.

### Запуск
Чтобы запустить бота, выполните в консоли:
```
python3 bot.py
```