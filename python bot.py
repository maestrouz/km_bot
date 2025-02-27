import telebot

API_TOKEN = '7799094741:AAHt16-4_mUypcrMbnU_MYDTrbksTSYrzHA'
START_GROUP_LINK = 'https://t.me/Kimyo_markaz1'
MAIN_GROUP_LINK = 'https://t.me/Kimyo_markaz12'

bot = telebot.TeleBot(API_TOKEN)

user_points = {}

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    if message.text.split(' ')[1:]:
        referrer = int(message.text.split(' ')[1])
        if referrer != user_id:
            user_points[referrer] = user_points.get(referrer, 0) + 1
            if user_points[referrer] == 5:
                bot.send_message(referrer, f"Tabriklaymiz! Siz 5 ta referal yig'dingiz! Asosiy guruh linki: {MAIN_GROUP_LINK}")
    
    referral_link = f'https://t.me/{bot.get_me().username}?start={user_id}'
    bot.send_message(user_id, f"Salom! Guruhimizga qo'shilish uchun 5 ta do'stingizni taklif qiling!\n\nSizning referal linkingiz: {referral_link}\n\nBoshlang'ich guruh: {START_GROUP_LINK}")

bot.polling(none_stop=True)

