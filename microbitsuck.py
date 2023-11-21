
# MICROBIT CODE




# onstart block
#คำเตือนน ต่อไฟเลี้ยงmicrobit 2 สาย
#รับข้อมูลจาก usb
serial.redirect_to_usb()

#ปรับ servo
servos.P0.set_pulse(500)
servos.P1.set_pulse(500)
servos.P2.set_pulse(500)
# setค่า
SerialData = ""
str_count_2 = 0
str_count_1 = 0
str_count_3 = 0

# set neopixel
strip: neopixel.Strip = None
strip = neopixel.create(DigitalPin.P8, 30, NeoPixelMode.RGB)

#end


# funtion
# นับ จำนวนขยะ
def count3():
    global str_count_3
    str_count_3 += 1
def count2():
    global str_count_2
    str_count_2 += 1
def count():
    global str_count_1
    str_count_1 += 1





#ทำงานเหมือน forever

#ถ้ามี data เข้ามา : 


def on_data_received():
    global SerialData
    SerialData = serial.read_until(serial.delimiters(Delimiters.NEW_LINE))
    music.play(music.tone_playable(523, music.beat(BeatFraction.QUARTER)),
        music.PlaybackMode.UNTIL_DONE)
    if SerialData == "recycle":
        count()
        basic.show_string("recycle :")
        basic.show_number(str_count_1)
        basic.pause(500)
        servos.P0.set_angle(90)
        basic.pause(500)
        servos.P0.set_angle(0)
        strip.show_color(neopixel.colors(NeoPixelColors.BLUE))
    elif SerialData == "biowaste":
        count2()
        basic.show_string("biowaste :")
        basic.show_number(str_count_2)
        servos.P1.set_angle(90)
        basic.pause(500)
        servos.P1.set_angle(0)
        strip.show_color(neopixel.colors(NeoPixelColors.GREEN))
    elif SerialData == "dangerous":
        count3()
        basic.show_string("dangrous :")
        basic.show_number(str_count_3)
        servos.P2.set_angle(90)
        basic.pause(500)
        servos.P2.set_angle(0)
        strip.show_color(neopixel.colors(NeoPixelColors.RED))
    elif SerialData == "back":
        strip.clear()
serial.on_data_received(serial.delimiters(Delimiters.NEW_LINE), on_data_received)
