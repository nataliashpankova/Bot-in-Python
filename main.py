import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from dotenv import load_dotenv


# --- 1. IMPOSTAZIONI (Compila con i tuoi dati!) ---

NAME = "<b>Natalia Shpankova</b>"
ROLE = "Junior IT"
SHORT_DESC = "<i>Junior IT con esperienza nel settore edilizio e forte orientamento all’innovazione digitale. Ho maturato competenze in project management, analisi dei dati, sicurezza cantieri e modellazione BIM. Appassionata di nuove tecnologie, in continuo aggiornamento con corsi su Java, SQL e Python & Machine Learning, attualmente in percorso di certificazione Oracle. Collaborativa, precisa e orientata ai risultati, desidero contribuire a progetti sfidanti in un contesto dinamico e internazionale.</i>"

LINK_GITHUB = "https://github.com/nataliashpankova"
LINK_TG_CHANNEL = "https://web.telegram.org/k/#@ChMAI_bot"
LINK_PORTFOLIO = ""

CONTACT_TG = "https://t.me/nshpankova"
CONTACT_EMAIL = "nataliashpankova@gmail.com"
CONTACT_LINKEDIN = "https://www.linkedin.com/in/nataliashpankova/"

PHOTO_ID = (
    ""
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN non è stato trovato! Controla il file .env")

ADMIN_ID = os.getenv("ADMIN_ID")
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# --- 2. TASTIERA ---

def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="About"), KeyboardButton(text="Projects")],
            [KeyboardButton(text="Contacts"), KeyboardButton(text="Photo")],
            [KeyboardButton(text="Hide menu")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Scegle un pulsante nel menu..."
    )

#
def nav_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Menu")]], resize_keyboard=True
    )

#
def get_footer() -> str:
    return "\n\nPremere Menu per tornare al menu principale."


# --- 3. GENERAZIONE DEL TESTO ---

def text_home() -> str:
    return (
        f"Ciao!\n\n"
        f"Sono il bot Change Managment AI Assistent. Mi chiamo {NAME}.\n\n"
        "Scegle menu"
    )

def text_about() -> str:
    parts = [
        f"{NAME}",
        f"{ROLE}\n",
        f"{SHORT_DESC}\n",
        f"Mi puoi trovare:",
        f"Telegram_channel",
        f"GitHub",
    ]
    if LINK_PORTFOLIO:
        parts.append(f"Portfolio")

    return "\n".join(parts) + get_footer()

def text_projects() -> str:
    return (
        "<b>Miei progetti</b>\n\n"
        "Dai un'occhiata agli esempi di codice e ai casi di studio:\n"
        f"<a href = 'https://github.com/nataliashpankova'>Mio GitHub</a>\n"
        + get_footer()
    )

def text_contacts() -> str:
    return (
        "Contattami\n\n"
        f"Telegram: scrivimi un messagio\n"
        f"Email: {CONTACT_EMAIL}"
        + get_footer()
    )

# --- 4. OPERATORI ---

@dp.message(Command("start"))
@dp.message(F.text == "Menu")
async def cmd_start(message: types.Message):
    await message.answer(text_home(), reply_markup=main_menu())


@dp.message(F.text == "About me")
@dp.message(Command("about"))
async def show_about(message: types.Message):
    await message.answer(text_about(), reply_markup=nav_menu())


@dp.message(F.text == "Projects")
@dp.message(Command("projects"))
async def show_projects(message: types.Message):
    await message.answer(text_projects(), reply_markup=nav_menu())

@dp.message(F.text == "Contacts")
@dp.message(Command("contacts"))
async def show_contacts(message: types.Message):
    # Invia una risposta all'utente (come prima)
    await message.answer(text_contacts(), reply_markup=nav_menu())

    # Inviamo una notifica all'ADMIN (tu)
    user_name = message.from_user.full_name
    user_login = message.from_user.username

    # Formazione del testo di notifica
    alert_text = (
        f"Qualcuno ti sta cercando!\n"
        f"User: {user_name}\n"
        f"Login: @{user_login if user_login else 'non ce login'}"
    )

    # Stiamo inviando un messaggio al tuo ID
    await bot.send_message(chat_id=ADMIN_ID, text=alert_text)

@dp.message(F.text == "Photo")
@dp.message(Command("photo"))
async def show_photo(message: types.Message):
    if not PHOTO_ID:
        await message.answer(
            "La foto non è impostata.\n"
            "Inviami l'immagine, ti darò il file_id e potrai inserirlo nel codice.",
            reply_markup=nav_menu(),
        )
        return
    await message.answer_photo(
        PHOTO_ID, caption=f"Это я, {NAME}!" + get_footer(), reply_markup=nav_menu()
    )

@dp.message(F.text == "Hide menu")
async def btn_hide(message: types.Message):
    await message.answer(
        "Menu è nascosto. Scrivi /start", reply_markup=ReplyKeyboardRemove()
    )


# --- 5. RESPONSABILI TECNICI ---

# Scatta una fototessera
@dp.message(F.photo)
async def get_photo_id(message: types.Message):
    await message.answer(f"Foto ID : {message.photo[-1].file_id}")

#
@dp.message()
async def fallback_handler(message: types.Message):
    await message.answer(
        "Non capisco ancora questi messaggi\n" "Per favore usa i pulsanti del menu.",
        reply_mark=nav_menu(),
    )


# --- 6. INIZIO ---

async def main():
    print("Bot funziona! Premi Ctrl+C per fermarlo.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot interrotto")
