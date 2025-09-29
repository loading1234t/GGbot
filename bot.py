import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart

# --- КОНФИГУРАЦИЯ ---
# !!! ВСТАВЬТЕ СЮДА ВАШ ТОКЕН, ПОЛУЧЕННЫЙ ОТ @BotFather !!!
# Замените этот текст на ваш реальный токен бота
BOT_TOKEN = "ВСТАВЬТЕ_ВАШ_ТОКЕН_СЮДА" 

# URL вашего WebApp (сайта на GitHub Pages)
WEB_APP_URL = "https://loading1234t.github.io/GGbot/"

# --- ИНИЦИАЛИЗАЦИЯ ---
# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- ОБРАБОТЧИК КОМАНДЫ /start ---
@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    """
    Обрабатывает команду /start. 
    Отправляет приветственное сообщение и кнопку, открывающую WebApp.
    """
    
    # 1. Создаем объект WebAppInfo, указывая URL нашего приложения
    web_app_info = WebAppInfo(url=WEB_APP_URL)
    
    # 2. Создаем кнопку, которая откроет WebApp
    # Мы используем ReplyKeyboardMarkup, чтобы кнопка появилась внизу, как в вашем примере.
    web_app_button = KeyboardButton(
        text="🛍️ Открыть маркет", 
        web_app=web_app_info
    )
    
    # 3. Создаем клавиатуру с этой кнопкой
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[web_app_button]], # Клавиатура с одной кнопкой в одном ряду
        resize_keyboard=True,         # Сделать клавиатуру компактной
        one_time_keyboard=False       # Оставить клавиатуру видимой
    )

    # 4. Отправляем приветственное сообщение с клавиатурой
    await message.answer(
        f"Добро пожаловать в GGPoint Маркет, {message.from_user.full_name}!\n\n"
        "Нажмите кнопку 'Открыть маркет' ниже, чтобы начать покупки или управлять своими товарами.",
        reply_markup=keyboard
    )

# --- ЗАПУСК БОТА ---
async def main():
    if BOT_TOKEN == "ВСТАВЬТЕ_ВАШ_ТОКЕН_СЮДА":
        print("!!! ОШИБКА: Пожалуйста, замените 'ВСТАВЬТЕ_ВАШ_ТОКЕН_СЮДА' на реальный токен вашего бота.")
        return
        
    print("Бот запущен и готов к работе. Нажмите Ctrl+C для остановки.")
    # Запускаем опрос сервера Telegram для получения новых сообщений
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен вручную.")
    except Exception as e:
        print(f"Произошла ошибка при запуске бота: {e}")
