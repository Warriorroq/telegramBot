import datetime
from datetime import *
import math
import random

cooldown_time = 5
iq_lower_texts = open("textsForLoweringIQ", "r").read().split('\n')
iq_increase_texts = open("textsForIncreasingIQ", "r").read().split('\n')

class iqplayer:
    def __init__(self, nickname):
        self.iq = 90.0
        self.nickname = nickname

    def play_game(self, update, context):
        iq_change = self.change_iq()
        self.iq += iq_change
        string_to_format = '{} {}'
        if iq_change < 0:
            string_to_format = iq_lower_texts[random.randint(0, len(iq_lower_texts) - 1)]
        elif iq_change >= 0:
            string_to_format = iq_increase_texts[random.randint(0, len(iq_increase_texts) - 1)]
        context.bot.send_message(
            chat_id=update.message.chat.id,
            text=string_to_format.format(iq_change, self.iq, self.nickname),
        )

    def change_iq(self):
        # minimum f : y = 0.07 + (90/x) * |sin(x/50)|
        # 0.15 - minimum chance
        # 90/x - increase chance to up iq if it is lower than 90

        # |sin(x/50)| - slightly lowering chance until value of 157 (max chance >1),
        # after increasing 224 (max chance is 0.33) and again lowering until 314
        # and again increasing 386(max chance is 0.17)...545(max 0.104)...703(0.06)...

        # it won't be possible to get more than 1000
        chance = 0.15 + 90/self.iq * abs(math.sin(self.iq/50.0))
        current_value = random.uniform(0, 1)
        max_iq_change = int(15 * int((self.iq / 90) * 100) / 100)
        if current_value < chance:
            return random.randint(0, max_iq_change)
        else:
            return -random.randint(1, max_iq_change)