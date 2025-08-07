import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from vtm_checks import roll


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Объект бота
bot = Bot(token="6678799564:AAGj6r2qCint7J66XJNXWDXF0eSPUeJ3u3Q", parse_mode="HTML")
# Диспетчер
dp = Dispatcher()
builder = InlineKeyboardBuilder()
for i in range(0, 6):
    builder.add(types.InlineKeyboardButton(
        text=str(i),
        callback_data=str(i))
    )
hunger = {}


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    global builder
    await message.answer("Отправь число пулла кубов проверки или укажи степень голода кнопкой", reply_markup=builder.as_markup())

@dp.message(Command("hunger"))
async def show_hunger(message: types.Message):
    global hunger, builder
    user = message.from_user.id
    hunger_user = hunger.get(user, '0')
    await message.answer(f'<b>Текущий голод: {hunger_user}</b>')
    await cmd_start(message)

@dp.callback_query(F.data.in_([str(i) for i in range(0,6)]))
async def set_hunger_for_user(callback: types.CallbackQuery):
    global hunger, builder
    hunger[callback.from_user.id] = callback.data
    logging.info(f'{callback.from_user.username} сменил Голод на {callback.data}')
    await callback.message.answer(f'<b>Текущий голод: {hunger[callback.from_user.id]}</b>')
    await cmd_start(callback.message)

@dp.message()
async def cmd_roll(message: types.Message):
    answer = '<i>Некорректный запрос!</i>'
    if message.text.isdigit():
        global hunger, builder
        if 0 < int(message.text) <= 20:
            answer = roll(message.text, hunger.get(message.from_user.id, '0'))
            logging.info(f'{message.from_user.username} сделал бросок!')
            logging.info(f'\n{answer}')
        else:
            answer = '<i>Слишком много кубов!</i>'
    await message.answer(answer)
    await cmd_start(message)

if __name__ == "__main__":
    asyncio.run(main())