

import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


# 1 Carichiamo token da .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Controllo se token non c'è
if not TOKEN:
    print("Errore: token non esiste nel file .env")
    exit()

PHOTO_ID = (
    ""
)
# 2 Impostazioni del bot
# HTML
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


# 3 /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Ciao!\n"
        "Al momento so fare pochi cose ma studio veloce.\n"
        "Premi /help per sapere i dettagli"
    )


# /help
@dp.message(Command("help"))
async def cnd_help(message: types.Message):
    await message.answer(
        "Informazioni:\n\n"
        "/start - Inizio dall'inizio\n"
        "/help - Mostrami questo messaggio\n"
        "/about - Di me\n"
        "/photo - Foto\n\n"
        "Semplecimente mandami un testo qualsiasi e ti rispondero."
    )


# /about
@dp.message(Command("about"))
async def cmd_about(message: types.Message):
    content = (
        "<b>About me</b>\n\n"
        "Sono un bot di Change Managmant AI Assistent.\n"
        "Mi ha creato Natalia Shpankova.\n"
        "Il mio email: nataliashpankova@gmail.com\n"
        "LinkedIn: <a href = 'https://www.linkedin.com/in/nataliashpankova/'>Natalia Shpankova</a>\n"
        "GitHub: <a href = 'https://github.com/nataliashpankova'>Natalia Shpankova</a>\n\n"
        "Scrivimi qualcosa e te lo ripeterò!"
    )
    await message.answer(content)


# foto
dp.message(Command("photo"))


async def cmd_photo(message: types.Message):
    if PHOTO_ID == "":
        await message.answer("Per primo imposta PHOTO_ID nel cosice!")
        return

    await message.answer_photo(photo=PHOTO_ID, caption="Ecco il tuo foto!")


@dp.message(F.photo)
async def get_photo_id(message: types.Message):
    photo_data = message.photo[-1]
    file_id = photo_data.file_id

    await message.answer(
        f"Foto è stato ricevuto!\n\n"
        f"Coppia questo ID a inserisca in PHOTO_ID:\n"
        f"{file_id}"
    )


@dp.message(F.document)
async def warning_doc(message: types.Message):
    await message.answer(
        "Hai mandato questo come un file.\n"
        "Telegram non fa vedere i anteprima per i file.\n"
        "Per favore, mandami proprio come Foto."
    )


# 4 echo
@dp.message()
async def echo_handler(message: types.Message):
    # Bot manda indietro lo stesso testo
    if message.text:
        await message.answer(f"Hai scritto: {message.text}")
    else:
        await message.answer("Capisco solo il testo, scusa")


# 5
async def main():
    print("Bot funziona! Premi Ctrl+C per fermarlo.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot interrotto")
