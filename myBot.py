import logging
import re
from telegram import *
from telegram.ext import *
from requests import *
from random import *
from iqPlayer import *

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
updater = Updater(open("token", "r").read(), use_context=True)
dp = updater.dispatcher

this_person_not_exist = "https://thispersondoesnotexist.com/image"
random_numbers_texts = open("textsForRandomInt", "r").read().split('\n')

games = {
    0: { #game id
     0 : iqplayer('0') #player's id and info
    }
}


def bot_start():
    dp.add_handler(CommandHandler("start", greetings))
    dp.add_handler(CommandHandler("Punk2077_bot", handle_message))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


def handle_message(update, context):
    msg_text = update.message.text
    if "Give random person" in msg_text:
        send_non_existing_person(update, context)
    if "Random num" in msg_text:
        send_random_integer(update, context)
    if "Start IQ game" in msg_text:
        try_to_create_iq_game(update, context)
    if "Register in IQ game" in msg_text:
        try_to_register_in_iq_game(update, context)
    if "Check IQ" in msg_text:
        try_to_play_iq_game(update, context)


def try_to_play_iq_game(update, context):
    chat_id = update.message.chat.id
    users_id = update.message.from_user.id
    if chat_id in games:
        if users_id in games[chat_id]:
            games[chat_id][users_id].play_game(update, context)
        else:
            answer_reply(update, context, "you are not registered in game")
    else:
        answer_reply(update, context, "you haven't registered game yet")

def try_to_register_in_iq_game(update, context):
    chat_id = update.message.chat.id
    users_id = update.message.from_user.id
    if chat_id in games:
        if users_id in games[chat_id]:
            answer_reply(update, context, "you have already registered in game")
        else:
            games[chat_id][users_id] = iqplayer(update.message.from_user.username)
            answer_reply(update, context, "registered: {}".format(games[chat_id][users_id].nickname))
    else:
        answer_reply(update, context, "you haven't registered game yet")


def try_to_create_iq_game(update, context):
    chat_id = update.message.chat.id
    if chat_id in games:
        answer_reply(update, context, "game exist id:{}".format(chat_id))
        return
    games[chat_id] = {}
    answer_reply(update, context,"game started id:{}".format(chat_id))


def send_random_integer(update, context):
    nums = re.findall(r'\d+', update.message.text)
    string_to_format = random_numbers_texts[randint(0, len(random_numbers_texts) - 1)]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=string_to_format.format(get_randint_from_last_array_elements(nums)),
    )


def get_randint_from_last_array_elements(nums):
    if len(nums) >= 3:
        num1 = int(nums[-1])
        num2 = int(nums[-2])
        if (num1 > num2):
            return randint(num2, num1)
        return randint(num1, num2)
    else:
        return randint(0, 10)


def send_non_existing_person(update, context):
    image = get(this_person_not_exist).content
    if image:
        context.bot.sendMediaGroup(
            chat_id=update.effective_chat.id,
            media=[InputMediaPhoto(image, caption="")]
        )
    answer_reply(update, context, "Done!")


def greetings(update, context):
    answer_reply(update, context, "Welcome!")


def error(self, update, context):
    self.logger.warning('Update "%s" caused error "%s"', update, context.error)


def answer_reply(update, context, text):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
    )