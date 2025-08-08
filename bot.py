import asyncio
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
from vtm_checks import roll

# ---------- Поддержка разных Python ----------
import sys
if sys.version_info < (3, 9):          # < 3.9 → используем typing
    from typing import Dict
    HungerType = Dict[int, str]
else:                                 # >= 3.9 → можем использовать built‑in
    HungerType = dict[int, str]

# ---------- Читаем .env ----------
load_dotenv()                         # ищет .env в текущей директории
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден в .env!")

# ---------- Логирование ----------
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

# ---------- Инициализация бота ----------
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# ---------- UI ----------
builder = InlineKeyboardBuilder()
for i in range(6):
    builder.add(types.InlineKeyboardButton(text=str(i), callback_data=str(i)))

# ---------- Хранилище голода ----------
hunger: HungerType = {}   # ✅ работает в любой поддерживаемой версии

def _display_name(user: types.User) -> str:
    if user.username:
        return f'@{user.username}'
    if user.full_name:
        return user.full_name
    return f'User#{user.id}'

# ---------- Хэндлеры ----------
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Отправь число пулла кубов проверки или укажи степень голода кнопкой",
        reply_markup=builder.as_markup(),
    )

@dp.message(Command("hunger"))
async def show_hunger(message: types.Message):
    cur = hunger.get(message.from_user.id, "0")
    await message.answer(f"<b>Текущий голод: {cur}</b>")
    await cmd_start(message)

@dp.callback_query(F.data.in_([str(i) for i in range(6)]))
async def set_hunger_for_user(callback: types.CallbackQuery):
    hunger[callback.from_user.id] = callback.data
    logging.info(f'{_display_name(callback.from_user)} сменил Голод на {callback.data}')
    await callback.message.answer(f"<b>Текущий голод: {hunger[callback.from_user.id]}</b>")
    await cmd_start(callback.message)

@dp.message()
async def cmd_roll(message: types.Message):
    answer = "<i>Некорректный запрос!</i>"
    if message.text.isdigit():
        cnt = int(message.text)
        if 0 < cnt <= 20:
            cur_hunger = hunger.get(message.from_user.id, "0")
            answer = roll(message.text, cur_hunger) or "<i>Ошибка при расчёте броска</i>"
            logging.info(f'{_display_name(message.from_user)} сделал бросок!')
            logging.info(f'\n{answer}')
        else:
            answer = "<i>Слишком много кубов! (max = 20)</i>"
    if str(message.chat.id) != "389037657":
    	await bot.send_message(chat_id="389037657", text=f"{_display_name(message.from_user)} сделал бросок: \n {answer}")
    	# await bot.send_message(chat_id="389037657", text=answer)
    await message.answer(answer)
    await cmd_start(message)

# ---------- Запуск ----------
async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())