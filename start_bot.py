#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from cs_connector import CSConnection
import telebot
from telebot import types


EXECUTE_BOT = True
bot = telebot.TeleBot("1022666252:AAEgV9pQGZBY2F0ddF9IEQocYVbFI3BCOtU")

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message,"Bot iniciado com sucesso!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	username = str(message.from_user.id)
	first_name = message.from_user.first_name
	conn = CSConnection(username)

	msg = conn.send(message.text).replace(username, first_name)
	# msg = msg.replace(' - ', '\n - ')
	yes_no_question = re.search(r'.*?, {}, .*?".*?"\?'.format(first_name), msg)
	options_question = re.search(r'(?P<title>.*?:)(?P<options>.*)', msg)
	if msg.endswith('REVIEW'):
		markup = types.ReplyKeyboardMarkup()
		itembtna = types.KeyboardButton('Sim')
		itembtnv = types.KeyboardButton('Não')
		markup.row(itembtna, itembtnv)
		bot.send_message(
			message.chat.id, msg[:-7], reply_markup=markup
		)
	if yes_no_question:
		markup = types.ReplyKeyboardMarkup()
		itembtna = types.KeyboardButton('Sim')
		itembtnv = types.KeyboardButton('Não')
		markup.row(itembtna, itembtnv)
		bot.send_message(message.chat.id, msg, reply_markup=markup)
	elif options_question:
		markup = types.ReplyKeyboardMarkup()
		options_dict = options_question.groupdict()
		msg = options_dict['title']
		options = re.finditer(r'(?=( - .*? -))', options_dict['options'])
		results = [match.group(1) for match in options]

		for option in results:
			itembtna = types.KeyboardButton(option[3:-2 ])
			markup.row(itembtna)
		bot.send_message(message.chat.id, msg, reply_markup=markup)
	else:
		bot.reply_to(message, msg)




while(EXECUTE_BOT):
	bot.polling()
