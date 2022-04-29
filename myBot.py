import logging
from telegram import *
from telegram.ext import *
from requests import *

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
updater = Updater("5347249231:AAEJAR3s1oTRrbz1ex6-epcK_Ds95Npq38A", use_context=True)
dp = updater.dispatcher
this_person_not_exist = "https://thispersondoesnotexist.com/image"


def bot_start():
    dp.add_handler(CommandHandler("start", greetings))
    dp.add_handler(CommandHandler("Punk2077_bot", handle_message))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


def handle_message(update, context):
    if "Give random person" in update.message.text:
        send_non_existing_person(update, context)


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
