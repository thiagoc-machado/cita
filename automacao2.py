import telebot

TOKEN = '5871766373:AAF5ktYG9WRr54LbLCHLq7FcK8zMnsJiN3I'
chat_id = '1854822221'


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.lower() == 'sim':
        bot.send_message(message.chat.id, 'Oi, tudo bem?')
    elif message.text.lower() == 'não':
        bot.send_message(message.chat.id, 'Que estranho.')

bot.send_message(chat_id, 'Você está aí?')
bot.polling()
