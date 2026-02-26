import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# ==========================================
# 1. IMPOSTAZIONI BOT
# ==========================================
TUTOR_NAME = "Natalia Shpankova"
SUBJECT = "Tutor d'italiano"

TEXT_ABOUT = (
    "About me\n\n"
    "Ti aiuto a parlare senza paura e a superare l'esame di Stato unificato con un punteggio di 90+.\n"
    "L'italiano è uno strumento, non una materia noiosa."
)

TEXT_SERVICES = (
    "I miei servizi:\n\n"
    "Lezione individuale (60 min) — 15€.\n"
    "Preparazione all'Esame di Stato Unificato (90 min) — 20€.\n"
    "Lezione di prova (30 min) — gratuita!"
)


PHOTO_ID = "AgACAgIAAxkBAAOLaZQgEJNuQFqg3t-Qb9tNSAFTTQEAAhkWaxt6XqFI8yyLmPY196YBAAMCAAN5AAM6BA"

# ==========================================
# 2. CONNESSIONE
# ==========================================
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID_RAW = os.getenv("ADMIN_ID")

if not TOKEN or not ADMIN_ID_RAW:
    raise ValueError("В .env non c'è BOT_TOKEN или ADMIN_ID!")

ADMIN_ID = int(ADMIN_ID_RAW)

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# ==========================================
# 3. TASTIERE
# ==========================================
def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="About me"), KeyboardButton(text="Servizi")],
            [KeyboardButton(text="Iscriviti a una lezione")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Seleziona una sezione"
    )

def back_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Al menu principale")]],
        resize_keyboard=True
    )

def get_footer() -> str:
    return "\n\nClicca su 'Torna al menu principale' per tornare."

# ==========================================
# 4. MANIPOLATORI DI BASE
# ==========================================
@dp.message(Command("start"))
@dp.message(F.text == "Al menu principale")
async def cmd_start(message: types.Message):
    welcome_text = (
        "Buongiorno!\n"
        f"{TUTOR_NAME} — {SUBJECT}.\n\n"
        "Seleziona una sezione dal menu sottostante."
    )
    if PHOTO_ID:
        await message.answer_photo(photo=PHOTO_ID, caption=welcome_text, reply_markup=main_menu())
    else:
        await message.answer(welcome_text, reply_markup=main_menu())

@dp.message(F.text == "About me")
async def show_about(message: types.Message):
    await message.answer(TEXT_ABOUT + get_footer(), reply_markup=back_menu())

@dp.message(F.text == "Servizi")
async def show_services(message: types.Message):
    await message.answer(TEXT_SERVICES + get_footer(), reply_markup=back_menu())

# ==========================================
# 5. GENERAZIONE DI LEAD
# ==========================================
@dp.message(F.text == "Iscriviti a una lezione")
async def take_lead(message: types.Message):
    await message.answer(
        "Ottima scelta!\n"
        "Ho passato i tuoi dati di contatto all'insegnante. Ti contatteranno presto!",
        reply_markup=back_menu()
    )

    user_name = message.from_user.full_name
    user_login = message.from_user.username
    login_text = f"@{user_login}" if user_login else "accesso nascosto"

    alert_text = (
        "NUOVA DOMANDA DI LEZIONE\n\n"
        f"Nome: {user_name}\n"
        f"Login: {login_text}\n"
    )

    await bot.send_message(chat_id=ADMIN_ID, text=alert_text)

# ==========================================
# 6. PROTEZIONE DA ERRORI E FOTO
# ==========================================
@dp.message(F.photo)
async def get_photo_id(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(f"Foto ID: {message.photo[-1].file_id}")
    else:
        await fallback_handler(message)

@dp.message()
async def fallback_handler(message: types.Message):
    await message.answer(
        "Mi dispiace, per ora capisco solo i pulsanti.\n"
        "Seleziona una sezione dal menu",
        reply_markup=main_menu()
    )

# ==========================================
# 7. INVIO
# ==========================================
async def main():
    print("Il biglietto da visita PRO-Tutor è stato lanciato con successo!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot interrotto")

