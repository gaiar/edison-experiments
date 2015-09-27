__author__ = 'gaiar'

import time, sys, signal, atexit
from sensors import Sensors
import telegram
import operator
import time
import botan

global mysensors
mysensors = Sensors()

BOTAN_TOKEN = '3332aa98-4a97-4617-a68b-902122df9cc0'

CMDSTR_MAX_LEN = 128
LOW_TEMP = 10
NOM_TEMP = 25
HIGH_TEMP = 40

SENSOR_COUNT = 6
ACTUATOR_COUNT = 4
VAR1_COUNT = SENSOR_COUNT
VAR2_COUNT = ACTUATOR_COUNT + 1
isBackLightOn = True
cmdstr = ''

BLColorRGB = {0x00, 0x00, 0xFF}

numRows = 2
numCols = 16

MenuCount = 5
MenuIndex = 0

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


def servo_handle(value):
    curt = current_milli_time
    if (current_milli_time - curt > 1000):
        # servo.setAngle(value)
        curt = current_milli_time


def sleep_handle():
    return


def relay_handle():
    return


def buzzer_handle():
    return


SensorValue = []

ActuatorHandlerList = [relay_handle, buzzer_handle, servo_handle, sleep_handle]

# value, condition, Actuator, action
SensorConfig = [
    {'sensor': 'Temperature', 'value': 85, 'condition': '>', 'handler': sleep_handle, 'trigger': 1},
    {'sensor': 'Humidity', 'value': 100, 'condition': '>', 'handler': sleep_handle, 'trigger': 1},
    {'sensor': 'Light', 'value': 200, 'condition': '<', 'handler': servo_handle, 'trigger': 90},
    {'sensor': 'UV', 'value': 1023, 'condition': '>', 'handler': sleep_handle, 'trigger': 1},
    {'sensor': 'PIR', 'value': 2, 'condition': '=', 'handler': buzzer_handle, 'trigger': 1},
    {'sensor': 'Moisture', 'value': 600, 'condition': '<', 'handler': relay_handle, 'trigger': 1}
]

current_milli_time = lambda: int(round(time.time() * 1000))


## Exit handlers ##
# This function stops python from printing a stacktrace when you hit control-C
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


def serial_request_handler():
    changed_value = 0
    i = 0

    for i in range(0, SENSOR_COUNT):
        if (SensorConfig[i][3] == servo_handle):
            changed_value = 0
        else:
            changed_value = not SensorConfig[i][1]
        if (ops[SensorConfig[i][2]](getSensorValueList[i], SensorConfig[i][1])):
            SensorConfig[i][3](SensorConfig[i][4])
        else:
            SensorConfig[i][3](changed_value)
        i += 1


def is_button_pressed():
    return button.value()


# def relay_handle(state):

# atexit.register(exitHandler)
# signal.signal(signal.SIGINT, SIGINTHandler)






def BuzzerHandler(val):
    return


def temp_color_handler():
    return


def display_menu():
    return


def get_menu_index():
    return ''


def display_menu():
    return ''


LAST_UPDATE_ID = None


def main():
    global LAST_UPDATE_ID

    bot = telegram.Bot(token='129517685:AAF78SRwWNdaL8XY0z3tDSIKLqcxV6N8eIw')
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None
    while True:
        sensor_bot(bot)


def sensor_bot(bot):
    global LAST_UPDATE_ID
    custom_keyboard = [['Temperature'], ['Humidity'], ['Light', 'UV'], ['Moisture']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)

    for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
        # print(update.message)
        try:
            chat_id = update.message.chat_id
            message = update.message
            user_id = update.message.from_user.id
            message_text = update.message.text.encode('utf-8')
        except (IndexError, ValueError, KeyError, TypeError) as error:
            print(error)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        # print(message_text)
        if (message_text):
            print(message_text)

            # mysensors.switch_light()
            if 'Temperature' in message_text:
                print('Sending Temp')
                bot.sendMessage(chat_id=chat_id, text='Temperature: ' + str(Sensors().get_temp_sensor_data()) + 'C',
                                reply_markup=reply_markup)
                botan.track(BOTAN_TOKEN, user_id, str(update), 'Temperature')

            if 'Light' in message_text:
                print('Sending Light')
                bot.sendMessage(chat_id=chat_id, text='Light: ' + str(Sensors().get_light_sensor_data()),
                                reply_markup=reply_markup)
                botan.track(BOTAN_TOKEN, user_id, str(update), 'Light')

            if 'Humidity' in message_text:
                print('Sending Hum')
                bot.sendMessage(chat_id=chat_id,
                                text='Humidity: ' + str(Sensors().get_humidity_sensor_data()) + '%',
                                reply_markup=reply_markup)
                botan.track(BOTAN_TOKEN, user_id, str(update), 'Humidity')

            if 'UV' in message_text:
                print('Sending UV')
                bot.sendMessage(chat_id=chat_id, text='UV: ' + str(Sensors().get_uv_sensor_data()),
                                reply_markup=reply_markup)
                botan.track(BOTAN_TOKEN, user_id, str(update), 'UV')

            if 'Moisture' in message_text:
                print('Sending Moisture')
                bot.sendMessage(chat_id=chat_id, text='Moisture: ' + str(Sensors().get_moisture_sensor_data()),
                                reply_markup=reply_markup)
                botan.track(BOTAN_TOKEN, user_id, str(update), 'Moisture')

            if '/start' in message_text:
                bot.sendMessage(chat_id=chat_id, text='What do you want to know?',
                                reply_markup=reply_markup)
                botan.track(BOTAN_TOKEN, user_id, str(update), 'Start')
                # print ('Sleeping')
                # time.sleep(2)
                # mysensors.switch_light()
            LAST_UPDATE_ID = update.update_id + 1


if __name__ == '__main__':
    main()

    # print_settings()
