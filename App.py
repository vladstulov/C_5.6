import telebot
from Config import keys, TOKEN
from Utils import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nпользователь может увидеть список доступных валют для конвертирования: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Число параметров не равно трём')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    #биткоин доллар 1
    #quote_ticker, base_ticker = keys[quote], Keys[base]
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать комманду\n{e}')
    else:
        text = f'цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()

#@bot.message_handler()
#def echo_test(message: telebot.types.Message):
  #  bot.send_message(message.chat.id, 'hello')

#bot.polling()