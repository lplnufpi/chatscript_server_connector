#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
sys.path.append('../tools/enelvo')

import re
import time

import enelvo.normaliser

from cs_connector import CSConnection
import telebot
from telebot import types


EXECUTE_BOT = True
bot = telebot.TeleBot("1022666252:AAEgV9pQGZBY2F0ddF9IEQocYVbFI3BCOtU")
norm = enelvo.normaliser.Normaliser()


def title(text):
	return text[0].upper() + text[1:]


def get_markup(rows):
	if not rows:
		return None

	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	for row in rows:
		keyboard_row = [types.KeyboardButton(title(cel)) for cel in row]
		markup.row(*keyboard_row)
	return markup


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	user_id = str(message.from_user.id)
	first_name = message.from_user.first_name
	user_name = first_name+'_'+user_id
	conn = CSConnection(user_name)

	# Spell correction
	rcvd_msg = norm.normalise(message.text.lower())
	bot_msg = conn.send(
		rcvd_msg
	).replace(first_name.lower(), first_name.title())

	options_question = re.search(r'(?P<title>.*?:)(?P<options>.*)', bot_msg)
	yes_no_question = re.search(
		r'.*?, {}, .*?".*?"\?'.format(first_name), bot_msg
	)

	if 'REVIEW' in bot_msg or yes_no_question:

		buttons = [['Sim', 'Não']]
		bot_messages = bot_msg.split('REVIEW')

	elif options_question:
		options_dict = options_question.groupdict()
		options = re.finditer(r'(?=( - .*? -))', options_dict['options'])
		results = [match.group(1) for match in options]
		if results:
			buttons = [[opt[3:-2 ]] for opt in results]
			bot_messages = options_dict['title'].split('BREAK')
		else:
			buttons = []
			bot_messages = [bot_msg]
	else:
		buttons = []
		bot_messages = bot_msg.split('BREAK')

	markup = get_markup(buttons)
	num_messages = len(bot_messages) - 1
	for index, bot_msg in enumerate(bot_messages):
		send_msg = title(bot_msg.strip())
		send_markup = markup if index == num_messages else None
		bot.send_message(message.chat.id, send_msg, reply_markup=send_markup)
		time.sleep(0.3)


while(EXECUTE_BOT):
	bot.polling()
