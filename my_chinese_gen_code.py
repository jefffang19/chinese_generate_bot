# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API

# webhook version
# https://towardsdatascience.com/how-to-deploy-a-telegram-bot-using-heroku-for-free-9436f89575d2

from transformers import BertTokenizer, GPT2LMHeadModel, TextGenerationPipeline
from opencc import OpenCC
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import torch
import os

PORT = int(os.environ.get('PORT', '8443'))
tokenizer = BertTokenizer.from_pretrained("uer/gpt2-chinese-lyric")
model = GPT2LMHeadModel.from_pretrained("uer/gpt2-chinese-lyric")
text_generator = TextGenerationPipeline(model, tokenizer)

# init transformer chinese text generator model

# tranditional and simpified chinese convert
cc_t2s = OpenCC('t2s')
cc_s2t = OpenCC('s2t')

# TOKEN
TOKEN = "5119579713:AAFGIVE9E9Y13m8TtR8cmukmKutpEkJrd5o"


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def echo(update, context):
    """fit text generation model"""
    # get text
    user_text = update.message.text
    print(user_text)
    try:
        # generate text
        model_gen = text_generator(cc_t2s.convert(
            user_text), max_length=80, do_sample=True)
        t_chi_gen_text = cc_s2t.convert(
            str(model_gen[0]['generated_text']))

        # responed
        responed_text = t_chi_gen_text
        update.message.reply_text(responed_text)
        print(responed_text)
        print('==========================')
    except:
        pass


def main():
    print(torch.__version__)

    # start bot
    updater = Updater(TOKEN, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    # on noncommand i.e message
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot
    updater.start_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN,
        webhook_url='https://telegram-bot-gen-text-v2.herokuapp.com/' + TOKEN,
    )

    print('start webhook')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
