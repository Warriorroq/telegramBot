import logging
import re
from telegram import *
from telegram.ext import *
from requests import *
from random import *

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
updater = Updater("5347249231:AAEJAR3s1oTRrbz1ex6-epcK_Ds95Npq38A", use_context=True)
dp = updater.dispatcher

this_person_not_exist = "https://thispersondoesnotexist.com/image"
random_numbers_texts = [
    "Sammy has {} balloons.",
    "You have {} girlfriends.",
    "{} your unlucky number",
    ]


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


def send_random_integer(update, context):
    nums = re.findall(r'\d+', update.message.text)
    item = random_numbers_texts[randint(0, len(random_numbers_texts) - 1)]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=item.format(get_randint_from_last_array_elements(nums)),
    )


def get_randint_from_last_array_elements(nums):
    if len(nums) >= 3:
        return randint(int(nums[-1]), int(nums[-2]))
    else:
        return randint(0, 10)

def send_non_existing_person(update, context):
    image = get(this_person_not_exist).content
    if image:
        context.bot.sendMediaGroup(
            chat_id=update.effective_chat.id,
            media=[InputMediaPhoto(image, caption="")]
        )
    update.message.reply_text("Done!")


def greetings(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome!",
        # reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Start')]])
    )


def error(self, update, context):
    self.logger.warning('Update "%s" caused error "%s"', update, context.error)
