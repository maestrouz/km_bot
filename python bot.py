import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import json

TOKEN = "7799094741:AAHt16-4_mUypcrMbnU_MYDTrbksTSYrzHA"
FIRST_GROUP_LINK = "https://t.me/Kimyo_markaz1"
MAIN_GROUP_LINK = "https://t.me/Kimyo_markaz2"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Foydalanuvchi ballarini saqlash uchun fayl
DATA_FILE = "users.json"

# JSON fayl bilan ishlash
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

users = load_data()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    user_id = str(message.from_user.id)
    
    if user_id not in users:
        users[user_id] = {"referrals": 0}
        save_data(users)
    
    referral_link = f"https://t.me/YOUR_BOT_USERNAME?start={user_id}"
    
    text = (
        f"Salom, {message.from_user.first_name}! 👋\n\n"
        f"📢 Ushbu guruhga qo'shilish uchun siz 5 ta do‘stingizni taklif qilishingiz kerak!\n\n"
        f"📩 Sizning referal havolangiz:\n{referral_link}\n\n"
        f"✅ Har bir yangi foydalanuvchi uchun 1 ball olasiz.\n"
        f"🎯 5 ball to‘plaganingizda, asosiy guruh havolasini olasiz!\n\n"
        f"🔗 Birinchi guruhga qo'shiling: {FIRST_GROUP_LINK}"
    )
    
    await message.answer(text)

@dp.message(Command("start"))
async def referral_handler(message: Message):
    args = message.text.split()
    if len(args) > 1:
        referrer_id = args[1]
        user_id = str(message.from_user.id)

        if user_id != referrer_id and user_id not in users:
            users[user_id] = {"referrals": 0}
            if referrer_id in users:
                users[referrer_id]["referrals"] += 1
                await bot.send_message(referrer_id, f"🎉 Sizning do‘stingiz qo‘shildi! Sizda {users[referrer_id]['referrals']} ball bor!")

                if users[referrer_id]["referrals"] >= 5:
                    await bot.send_message(referrer_id, f"🎊 Tabriklaymiz! Siz 5 ta do‘stingizni taklif qildingiz!\nAsosiy guruhga qo'shilish havolasi: {MAIN_GROUP_LINK}")

            save_data(users)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
