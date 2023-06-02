import telebot

TOKEN = ':'
chat_id = ''


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.lower() == 'sim':
        bot.send_message(message.chat.id, 'Oi, tudo bem?')
    elif message.text.lower() == 'não':
        bot.send_message(message.chat.id, 'Que estranho.')

bot.send_message(chat_id, 'Você está aí?')
bot.polling()
