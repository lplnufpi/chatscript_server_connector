#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append('../')
sys.path.append('../tools/enelvo')

import re
import time
import subprocess

from chatscript_generator import wordembedding
import enelvo.normaliser
from cs_connector import CSConnection
import telegram
import telebot
from telebot import types


bot = telebot.TeleBot("1214763382:AAEgrtYBxKRHOvj8ZspVejzLN0trxdwPNeo")
norm = enelvo.normaliser.Normaliser()
cbow = wordembedding.CBoW()

users = list()

users_profiles = {
	'1005448831': '0', # Professor 1
	'1016949742': '1', # Professor 2
	'222098113': '1', # Vitor
	'815033196': '2', # Patrício
	'986846182': '2', # Prof Lucas
	'1227416692': '3', # Prof Marina

	'111924266': '0',  # User Roney
	'781461851': '0',  # User Gabriel
	'73050958': '1',   # User João Paulo
	'737034449': '2',  # User Kauan
	'819573423': '3',  # User Gilvan
	'607631480': '3',  # User Leandro

	'356610632': '1',  # User João
	'1194861342': '2', # User Rafael
}

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
	if user_id in users_profiles:
		user_profile = users_profiles[user_id]
	else:
		user_profile = '0'
	user_str = 'User {} - Id {} - Profile {}'.format(first_name, user_id, user_profile)
	if user_str not in users:
		users.append(user_str)
		print(user_str)
		with open('arq.txt', 'a') as arq:
			arq.write('\n'.join(users))

	conn = CSConnection(user_id, botname='harry')

	if message.text.startswith(':'):
		if 'exit' in message.text:
			bot.send_message(message.chat.id, 'EXIT')
			bot.stop_polling()
			exit()
		rcvd_msg = message.text.lower()
	else:
		words = message.text.lower().split(' ')
		rcvd_msg = list()
		for word in words:
			if word in cbow.model:
				rcvd_msg.append(word)
			else:
				rcvd_msg.append(norm.normalise(word))
		rcvd_msg = ' '.join(rcvd_msg)

	bot_msg = conn.send(rcvd_msg)

	# Check if bot msg calls other proccess
	start_process = re.search(r'(?P<process>.*?\.py)(?P<args> .*?)?', bot_msg)
	if start_process:
		# Use user_profile to call process instead of user_id
		process_string = start_process.string.replace(user_id, user_profile)
		split_review = process_string.split('REVIEW')
		# Use just text before REVIEW
		process = ['python'] + split_review[0].lower().split(' ')
		bot_msg = subprocess.check_output(process).decode('utf-8')
		# Add removed BREAK and tail
		if len(split_review) > 1:
			bot_msg = 'REVIEW'.join([bot_msg] + split_review[1:])

	# Replace user_id and user_profile by the user first name
	bot_msg = bot_msg.replace('USER', first_name.title())

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
		if bot_msg:
			send_msg = title(bot_msg.strip())
			send_markup = markup if index == num_messages else None
			bot.send_message(
				message.chat.id,
				send_msg,
				reply_markup=send_markup,
				parse_mode=telegram.ParseMode.MARKDOWN
			)
			time.sleep(0.3)

bot.delete_webhook()
bot.polling()
