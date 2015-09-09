__author__ = 'gaiar'

from sensors import Sensors
import telegram
import pyupm_i2clcd as lcd_screen

#print('UV: ' + str(Sensors().get_uv_sensor_data()))
print('Light: ' + str(Sensors().get_light_sensor_data()))
print('Humidity: ' + str(Sensors().get_humidity_sensor_data()))
print('Temperature: ' + str(Sensors().get_temp_sensor_data()))
Sensors().display_ths_sensor_data()

lcd = lcd_screen.Jhd1313m1(0, 0x3E, 0x62)
lcd.write('Hi, Gaiar!')

lcd.clear()
lcd.write(" Temp&Humidity  ")
#lcd.write("<-")
lcd.setCursor(1, 1)
print (str(Sensors().get_temp_sensor_data()))
lcd.write(str(Sensors().get_temp_sensor_data()))
lcd.write("C ")

# sprintf(number,"%d",getHumiSensorValue());
lcd.setCursor(1, 9)
lcd.write(str(Sensors().get_humidity_sensor_data()))
lcd.write("%")
# lcd.setCursor(numCols-2,1);
# lcd.write("->");

# display_ths_sensor_data()

raw_input("Press Enter if you believe...")
