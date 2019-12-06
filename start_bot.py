#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from cs_connector import CSConnection
import telebot
from telebot import types


EXECUTE_BOT = True
bot = telebot.TeleBot("1022666252:AAEgV9pQGZBY2F0ddF9IEQocYVbFI3BCOtU")

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
	username = str(message.from_user.id)
	first_name = message.from_user.first_name
	conn = CSConnection(username)

	bot_msg = conn.send(message.text.lower()).replace(username, first_name)

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

		buttons = [[opt[3:-2 ]] for opt in results]
		bot_messages = options_dict['title'].split('BREAK')
	else:
		buttons = []
		bot_messages = bot_msg.split('BREAK')

	markup = get_markup(buttons)
	for bot_msg in bot_messages:
		bot.send_message(message.chat.id, bot_msg, reply_markup=markup)


while(EXECUTE_BOT):
	bot.polling()
