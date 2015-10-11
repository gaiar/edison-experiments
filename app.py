#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'gaiar'

import sys
import operator
import time
from flask import Flask, request, render_template
from werkzeug import serving
import telegram
import threading
import atexit

from sensors import Sensors
import botan
from iotkit import iot_kit
import logging
from logging.handlers import RotatingFileHandler
from werkzeug.contrib.cache import SimpleCache

global mysensors
mysensors = Sensors()

iot = ""
BOTAN_TOKEN = '3332aa98-4a97-4617-a68b-902122df9cc0'
IOTKIT_TEMPERATURE_CID = '219d3236-332b-45ec-9d65-68cd82ed0387'
IOTKIT_HUMIDITY_CID = '1f398387-b688-4f07-a111-1a27461e1216'
IOTKIT_LIGHT_CID = 'b7fb5543-1b94-4b5c-bf93-4b7c94c31613'
IOTKIT_UV_CID = 'c2c69303-f70a-43cc-9b37-fd5ab9bef54a'
IOTKIT_MOISTURE_CID = '93382cb9-2549-456c-97f0-16abb1929c0b'

isBackLightOn = True

getSensorValueList = [
    {'sensor': 'temperature', 'value': Sensors().get_temp_sensor_data},
    {'sensor': 'humidity', 'value': Sensors().get_humidity_sensor_data},
    {'sensor': 'light', 'value': Sensors().get_light_sensor_data},
    {'sensor': 'uv', 'value': Sensors().get_uv_sensor_data},
    {'sensor': 'encoder', 'value': Sensors().get_encoder_data},
    {'sensor': 'moisture', 'value': Sensors().get_moisture_sensor_data}]

ops = {
    ">": operator.ge,
    "<": operator.lt,
    "=": operator.eq
}

global bot
bot = telegram.Bot(token='129517685:AAF78SRwWNdaL8XY0z3tDSIKLqcxV6N8eIw')

# Seconds before cloud data update
POOL_TIME = 30

# thread handler
iot_thread = threading.Thread()

iot_lock = threading.Lock()

iot = ''


# value, condition, Actuator, action
# SensorConfig = [
#     {'sensor': 'Temperature', 'value': 85, 'condition': '>', 'handler': sleep_handle, 'trigger': 1},
#     {'sensor': 'Humidity', 'value': 100, 'condition': '>', 'handler': sleep_handle, 'trigger': 1},
#     {'sensor': 'Light', 'value': 200, 'condition': '<', 'handler': servo_handle, 'trigger': 90},
#     {'sensor': 'UV', 'value': 1023, 'condition': '>', 'handler': sleep_handle, 'trigger': 1},
#     {'sensor': 'PIR', 'value': 2, 'condition': '=', 'handler': buzzer_handle, 'trigger': 1},
#     {'sensor': 'Moisture', 'value': 600, 'condition': '<', 'handler': relay_handle, 'trigger': 1}
# ]

current_milli_time = lambda: int(round(time.time() * 1000))


def SIGINTHandler(signum, frame):
    raise SystemExit


def exitHandler():
    print("Exiting")
    sys.exit(0)


def print_settings():
    print('The Sensors Configurations as follow:')
    i = 0
    for i in range(0, SENSOR_COUNT):
        print(SensorConfig[i]['sensor'] + " " + SensorConfig[i]['condition']) + " " + str(SensorConfig[i]['value'])

        i += 1
    print("\n")
    print("The Sensors Value as follow:")
    i = 0
    for i in range(0, SENSOR_COUNT):
        print(getSensorValueList[i]['sensor'] + ' = ' + str(getSensorValueList[i]['value']()))
        i += 1
    print("\n")


def create_app():
    app = Flask(__name__)
    def interrupt():
        global iot_thread
        iot_thread.cancel()

    def send_iot_data():
        global iot_thread
        global iot
        with iot_lock:
            iot.create_observations(IOTKIT_TEMPERATURE_CID, str(Sensors().get_temp_sensor_data()), current_milli_time())
            iot.create_observations(IOTKIT_HUMIDITY_CID, str(Sensors().get_humidity_sensor_data()),
                                    current_milli_time())
            iot.create_observations(IOTKIT_LIGHT_CID, str(Sensors().get_light_sensor_data()), current_milli_time())
            iot.create_observations(IOTKIT_UV_CID, str(Sensors().get_uv_sensor_data()), current_milli_time())

        iot_thread = threading.Timer(POOL_TIME, send_iot_data, ())
        iot_thread.start()

    def start_iot_thread():
        global iot_thread
        global  iot
        iot = iot_kit()
        iot_thread = threading.Timer(POOL_TIME, send_iot_data, ())
        iot_thread.start()


        #start_iot_thread()
    atexit.register(interrupt)
    return app


app = create_app()

current_milli_time = lambda: int(round(time.time() * 1000))

cache = SimpleCache()

# @app.before_first_request
# def prepare_cache():
#     current_sensors = []
#
#     current_sensors.append({
#         'number': 1,
#         'name': 'Temperature',
#         'value': str(Sensors().get_temp_sensor_data()),
#         'measurement': 'C'
#     })
#
#     current_sensors.append({
#         'number': 2,
#         'name': 'Humidity',
#         'value': str(Sensors().get_humidity_sensor_data()),
#         'measurement': '%'
#     })
#
#     current_sensors.append({
#         'number': 3,
#         'name': 'Light',
#         'value': str(Sensors().get_light_sensor_data()),
#         'measurement': 'Lux'
#     })
#
#     current_sensors.append({
#         'number': 4,
#         'name': 'UV',
#         'value': str(Sensors().get_uv_sensor_data()),
#         'measurement': 'UVs'
#     })
#     cache.set('sensors', current_sensors, timeout=5 * 60)


@app.route('/')
def index():
    current_sensors = cache.get('sensors')
    if current_sensors is None:
        current_sensors = []

        current_sensors.append({
            'number': 1,
            'name': 'Temperature',
            'value': str(Sensors().get_temp_sensor_data()),
            'measurement': 'C'
        })

        current_sensors.append({
            'number': 2,
            'name': 'Humidity',
            'value': str(Sensors().get_humidity_sensor_data()),
            'measurement': '%'
        })

        current_sensors.append({
            'number': 3,
            'name': 'Light',
            'value': str(Sensors().get_light_sensor_data()),
            'measurement': 'Lux'
        })

        current_sensors.append({
            'number': 4,
            'name': 'UV',
            'value': str(Sensors().get_uv_sensor_data()),
            'measurement': 'UVs'
        })
        cache.set('sensors', current_sensors, timeout=5 * 60)

    return render_template('index.html', sensors=current_sensors)


@app.route('/bot', methods=['GET', 'POST'])
def sensor_bot():
    if request.method == "POST":
        custom_keyboard = [['Temperature'], ['Humidity'], ['Light', 'UV'], ['Moisture']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
        update = telegram.Update.de_json(request.get_json(force=True))

        try:
            chat_id = update.message.chat_id
            user_id = update.message.from_user.id
            message_text = update.message.text.encode('utf-8')
        except (IndexError, ValueError, KeyError, TypeError) as error:
            app.logger.warning(error)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        if (message_text):

            # mysensors.switch_light()
            if 'Temperature' in message_text:
                # print('Sending Temp')
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                bot.sendMessage(chat_id=chat_id, text='Temperature: ' + str(Sensors().get_temp_sensor_data()) + 'C',
                                reply_markup=reply_markup)
                botan.track(BOTAN_TOKEN, user_id, str(update), 'Temperature')

            if 'Light' in message_text:
                # print('Sending Light')
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                bot.sendMessage(chat_id=chat_id, text='Light: ' + str(Sensors().get_light_sensor_data()),
                                reply_markup=reply_markup)
                botan.track(BOTAN_TOKEN, user_id, str(update), 'Light')

            if 'Humidity' in message_text:
                # print('Sending Hum')
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                bot.sendMessage(chat_id=chat_id,
                                text='Humidity: ' + str(Sensors().get_humidity_sensor_data()) + '%',
                                reply_markup=reply_markup)
                botan.track(BOTAN_TOKEN, user_id, str(update), 'Humidity')

            if 'UV' in message_text:
                # print('Sending UV')

                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                bot.sendMessage(chat_id=chat_id, text='UV: ' + str(Sensors().get_uv_sensor_data()),
                                reply_markup=reply_markup)
                botan.track(BOTAN_TOKEN, user_id, str(update), 'UV')

            if 'Moisture' in message_text:
                # print('Sending Moisture')
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                bot.sendMessage(chat_id=chat_id, text='Moisture: ' + str(Sensors().get_moisture_sensor_data()),
                                reply_markup=reply_markup)
                botan.track(BOTAN_TOKEN, user_id, str(update), 'Moisture')

            if '/start' in message_text:
                bot.sendMessage(chat_id=chat_id, text='What do you want to know?',
                                reply_markup=reply_markup)
                botan.track(BOTAN_TOKEN, user_id, str(update), 'Start')
                # mysensors.switch_light()
            return ('{}')
    else:
        app.logger.info('Bot is here!')
        return ('Bot is here!')


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    bot.setWebhook('')
    s = bot.setWebhook('https://iotbot.ru/bot')
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


if __name__ == '__main__':
    handler = RotatingFileHandler('iotbot.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    try:
        app.run()
    except Exception:
        app.logger.exception('Failed')
