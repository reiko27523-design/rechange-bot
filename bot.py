from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import os, sqlite3

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID  = int(os.getenv("ADMIN_ID", "0"))

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

def db():
    c = sqlite3.connect("bot.db"); c.row_factory = sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS users(
      tg_id INTEGER PRIMARY KEY,
      balance INTEGER DEFAULT 0
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS orders(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      tg_id INTEGER, uid TEXT, server TEXT, pkg TEXT, amount INTEGER,
      status TEXT DEFAULT 'pending'
    )""")
    c.commit(); return c

home = ReplyKeyboardMarkup(resize_keyboard=True)
home.add(KeyboardButton("Login"), KeyboardButton("Getid"), KeyboardButton("Help"))

menu = ReplyKeyboardMarkup(resize_keyboard=True)
for t in ["📜 View Price List","💎 Top-up Instructions","🛒 Buy Diamonds","📖 View Top-up History"]:
    menu.add(KeyboardButton(t))

@dp.message_handler(commands=["start"])
async def start(m: types.Message):
    c = db(); c.execute("INSERT OR IGNORE INTO users(tg_id) VALUES(?)",(m.from_user.id,))
    c.commit(); c.close()
    await m.answer(f"Hello, {m.from_user.first_name}!\nYour user ID: {m.from_user.id}", reply_markup=home)

@dp.message_handler(commands=["menu"])
async def show_menu(m: types.Message):
    await m.answer("📋 Commands Menu:", reply_markup=menu)

@dp.message_handler(lambda x: x.text=="📜 View Price List")
async def price(m: types.Message):
    await m.answer("💰 Price List\n14D=1,000Ks | 28D=2,000Ks | 86D=5,800Ks ...")
