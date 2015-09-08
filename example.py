__author__ = 'Gaiar'

# !/usr/bin/env python
import time
import pyupm_i2clcd
import pyupm_grove
import random
import pyupm_grovemoisture
import subprocess
import ftplib

light_time_on = 6  # in hours military time (6 am)
light_time_off = 22  # in hours military time (10 pm)
vid_hr = 1  # time video is made and uploaded in hours military time (1:00 am)
vid_min = 0

display_dt = 60  # refresh display every minute (60 seconds)
pic_dt = 15  # take picture and check sensors every 15 minutes
moist_dt = 15
light_dt = 15
temp_dt = 15
t_start = int(time.time())  # starting time
t = 0
t0 = 0

# Grove upm objects
x = pyupm_i2clcd.Jhd1313m1(0, 0x3E, 0x62)
moist_sensor = pyupm_grovemoisture.GroveMoisture(2)
pump_relay = pyupm_grove.GroveRelay(6)
temp_sensor = pyupm_grove.GroveTemp(1)
light_sensor = pyupm_grove.GroveLight(0)
light_relay = pyupm_grove.GroveRelay(5)

while True:
    t = int(time.time())  # time for this round of processing

    # output time and date and name and random background color--updates every minute
    x.setCursor(0, 0)
    x.write("Team Tomato")
    x.setCursor(1, 0)
    x.write(time.strftime("%I:%M %a %m-%d"))
    x.setColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    print
    "Team Tomato", time.strftime("%I:%M %a %m-%d")

    # check moisture and store values in file
    # average 10 sensor readings over one second
    min = time.strftime('%M', time.localtime())
    if int(min) % moist_dt == 0:  # test every 15 minutes
        m = []
        for i in range(0, 10):
            m.append(moist_sensor.value())
            time.sleep(0.1)

        mave = sum(m) / 10
        mave = '{0}'.format(mave)
        print
        "Moisture level = " + mave
        # see if file is already started and get starting time use try so failure doesn't stop script
        try:
            with open("/media/sdcard/myprog/moistdata.txt", "r") as myfile:
                t0 = int(myfile.readline().strip('\n'))
            print
            "First line of moistdata.txt = " + str(t0)
        except:
            # file not started so put starting time as first entry
            try:
                with open("/media/sdcard/myprog/moistdata.txt", "w") as myfile:
                    myfile.write(str(t_start) + '\n')
                print
                "Starting moistdata.txt file with " + str(t_start)
                t0 = t_start
            except:
                print
                "Could not open moistdata.txt."

        # calculate time since start in seconds
        t -= t0

        # if moisture sensor above 200 run pump
        if int(mave) > 200:
            try:
                with open("/media/sdcard/myprog/pumpsettings.txt", "r") as myfile:
                    time_on = myfile.readlines()  # get number of seconds to run pump from file
                time_on = time_on[0].strip()
                try:
                    with open("/media/sdcard/myprog/pumptimes.txt", "a") as myfile:
                        myfile.write('on,' + time_on + ',' + str(t) + '\n')  # store pump data
                    pump_relay.on()
                    time.sleep(int(time_on))
                    print
                    "Run Pump for " + time_on + " seconds."
                    pump_relay.off()
                    try:
                        with open("/media/sdcard/myprog/moistdata.txt", "a") as myfile:
                            myfile.write(
                                '[' + str(t) + ',' + mave + ',500]' + '\n')  # store moisture and pump data for web page
                    except:
                        print
                        "Could not open moistdata.txt to write pump on."
                except:
                    print
                    "Could not write to pumptimes.txt."
            except:
                print
                "Could not read from pumpsettings.txt."
        else:
            try:
                with open("/media/sdcard/myprog/moistdata.txt", "a") as myfile:
                    myfile.write('[' + str(t) + ',' + mave + ',0]' + '\n')
            except:
                print
                "Could not open moistdata.txt to write pump off."

    # check temp
    if int(min) % temp_dt == 0:
        c = []
        for i in range(0, 10):
            c.append(temp_sensor.value())
            time.sleep(0.1)

        cave = sum(c) / 10.
        fave = cave * 1.8 + 32.
        cave = '{0:.1f}'.format(cave)
        fave = '{0:.1f}'.format(fave)

        try:
            with open("/media/sdcard/myprog/tempdata.txt", "r") as myfile:
                t0 = int(myfile.readline().strip('\n'))
        except:
            try:
                with open("/media/sdcard/myprog/tempdata.txt", "a") as myfile:
                    myfile.write(str(t_start) + '\n')
                print
                "Starting tempdata.txt file with " + str(t_start)
            except:
                print
                "Could not open tempdata.txt."
        try:
            with open("/media/sdcard/myprog/tempdata.txt", "a") as myfile:
                myfile.write('[' + str(t) + ',' + cave + ',' + fave + ']' + '\n')
            print
            'Temperature = ' + fave
        except:
            print
            "Could not open tempdata.txt for append."

    # check light --> light on or off
    if int(min) % light_dt == 0:
        h = time.strftime('%H')
        if int(h) >= light_time_on and int(h) < light_time_off:
            l1 = 500;
            light_relay.on()
            print
            "Light is on."
        else:
            l1 = 0
            light_relay.off()
            print
            "Light is off."
        l2 = []
        for i in range(0, 10):
            l2.append(light_sensor.raw_value())
            time.sleep(0.1)

        l2ave = sum(l2) / 10
        l2ave = '{0:.1f}'.format(l2ave)

        try:
            with open("/media/sdcard/myprog/lightdata.txt", "r") as myfile:
                t0 = int(myfile.readline().strip('\n'))
        except:
            try:
                with open("/media/sdcard/myprog/lightdata.txt", "a") as myfile:
                    myfile.write(str(t_start) + '\n')
                print
                "Starting lightdata.txt file with " + str(t_start)
            except:
                print
                "Could not open lightdata.txt."
        try:
            with open("/media/sdcard/myprog/lightdata.txt", "a") as myfile:
                myfile.write('[' + str(t) + ',' + l2ave + ',' + str(l1) + ']' + '\n')
            print
            'Light value = ' + l2ave
        except:
            print
            "Could not open lightdata.txt for append."

    # check pic --> vid --> upload
    if int(min) % pic_dt == 0:
        try:  # pictures have to be numbered consecutively for ffmpeg to turn them into a video
            with open('/media/sdcard/myprog/picnum.txt', 'r') as myfile:
                n = myfile.readline().strip()
            n = str(int(n) + 1)
            if len(n) == 1:
                n = '000' + n
            if len(n) == 2:
                n = '00' + n
            if len(n) == 3:
                n = '0' + n
        except:
            print
            "error opening picnum first time"
        try:
            with open('/media/sdcard/myprog/picnum.txt', 'w') as myfile:
                myfile.write(n)
        except:
            print
            "error opening picnum 2nd time"
        try:
            proc = subprocess.check_output(
                '/media/sdcard/myprog/ffmpeg/ffmpeg -ss 0.5 -i /dev/video0 -vframes 1 -s 720x480 -f image2 /media/sdcard/myprog/images/Imgp' + n + '.jpg',
                shell=True)

            p = subprocess.Popen("echo " + proc, shell=True)
            p.communicate()
            print
            'Saved image as Imgp' + n + '.jpg'
        except:
            print
            "error with pic process"
    # make video and upload files once per day at 1 am
    if int(time.strftime('%H', time.localtime())) == vid_hr and int(time.strftime('%M', time.localtime())) == vid_min:
        try:
            proc = subprocess.check_output(
                "rm -r /media/sdcard/myprog/images/video.mp4", shell=True)
            p = subprocess.Popen("echo " + proc, shell=True)
            p.communicate()
        except:
            print
            "Could not remove video file."

        time.sleep(5)
        try:
            proc = subprocess.check_output(
                "/media/sdcard/myprog/ffmpeg/ffmpeg -f image2 -i '/media/sdcard/myprog/images/Imgp%04d.jpg' -pix_fmt yuv420p -codec:v libx264 -profile:v high -preset slow -b:v 500k -maxrate 500k -bufsize 1000k /media/sdcard/myprog/images/video.mp4",
                shell=True)

            p = subprocess.Popen("echo " + proc, shell=True)
            p.communicate()

            print
            "Prcessed video"
        except:
            print
            "Could not process video."
        try:  # upload video and data files
            ftp = ftplib.FTP("website.com")
            ftp.login("username", "password")

            ftp.storlines("STOR lightdata.txt", open("/media/sdcard/myprog/lightdata.txt"))
            ftp.storlines("STOR moistdata.txt", open("/media/sdcard/myprog/moistdata.txt"))
            ftp.storlines("STOR tempdata.txt", open("/media/sdcard/myprog/tempdata.txt"))
            ftp.storbinary("STOR video.mp4", open("/media/sdcard/myprog/images/video.mp4", "rb"))
            ftp.close()
            print
            "Files uploaded."
        except:
            print
            "Files not uploaded."

    # get number of second in current time
    sec = time.strftime('%S', time.localtime())
    # wait until next minute before repeating
    time.sleep(display_dt - int(sec))
