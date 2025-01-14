import time
import badger2040
import urequests
import jpegdec

display = badger2040.Badger2040()
jpeg = jpegdec.JPEG(display.display)

display.led(255)

sleeptime = 10 #Minutes

if badger2040.woken_by_rtc():
    timeout = 10 #Seconds
else:
    timeout = 30 #Seconds

lastPress = time.time()


class Page():
    MAIN = 0
    NOWA = 1
    NEXTA = 2
    NOWB = 3
    NEXTB = 4
    NOWC = 5
    NEXTC = 6

curPage = Page.MAIN
    

URL = "http://schedule.emfcamp.dan-nixon.com/now-and-next?fake_epoch=2024-05-02T10:00:00%2b01:00&venue=Stage+A&venue=Stage+B&venue=Stage+C"
#URL = "http://schedule.emfcamp.dan-nixon.com/now-and-next?venue=Stage+A&venue=Stage+B&venue=Stage+C" # For using at EMF

display.connect()

display.set_pen(15)
display.clear()
display.set_pen(0)

display.set_update_speed(badger2040.UPDATE_MEDIUM)

def get_data():
    global nowA, nextA, nowB, nextB, nowC, nextC, j
    
    req = URL
    print(f"Requesting URL: {req}")
    r = urequests.get(req)
    j = r.json()
    print("Data obtained!")
    try:
        start = j["guide"]["Stage A"]["now"]["start_time"]
    except:
        nowA = "Nothing on Stage A"
    else:
        end = j["guide"]["Stage A"]["now"]["end_time"]
        nowA = "{} {} - {} ".format(start, j["guide"]["Stage A"]["now"]["title"], j["guide"]["Stage A"]["now"]["speaker"])
    print (nowA)
    
    try:
        start = j["guide"]["Stage A"]["next"]["start_time"]
    except:
        nextA = "Nothing on Stage A"
    else:
        end = j["guide"]["Stage A"]["next"]["end_time"]
        nextA = "{} {} - {} ".format(start, j["guide"]["Stage A"]["next"]["title"], j["guide"]["Stage A"]["next"]["speaker"])
    print (nextA)
        
    try:
        start = j["guide"]["Stage B"]["now"]["start_time"]
    except:
        nowB = "Nothing on Stage B"
    else:
        end = j["guide"]["Stage B"]["now"]["end_time"]
        nowB = "{} {} - {} ".format(start, j["guide"]["Stage B"]["now"]["title"], j["guide"]["Stage B"]["now"]["speaker"])
    print (nowB)
    
    try:
        start = j["guide"]["Stage B"]["next"]["start_time"]
    except:
        nextB = "Nothing on Stage B"
    else:
        end = j["guide"]["Stage B"]["next"]["end_time"]
        nextB = "{} {} - {} ".format(start, j["guide"]["Stage B"]["next"]["title"], j["guide"]["Stage B"]["next"]["speaker"])
    print (nextB)
    
    try:
        start = j["guide"]["Stage C"]["now"]["start_time"]
    except:
        nowC = "Nothing on Stage C"
    else:
        end = j["guide"]["Stage C"]["now"]["end_time"]
        nowC = "{} {} - {} ".format(start, j["guide"]["Stage C"]["now"]["title"], j["guide"]["Stage C"]["now"]["speaker"])
    print (nowC)
    
    try:
        start = j["guide"]["Stage C"]["next"]["start_time"]
    except:
        nextC = "Nothing on Stage C"
    else:
        end = j["guide"]["Stage C"]["next"]["end_time"]
        nextC = "{} {} - {} ".format(start, j["guide"]["Stage C"]["next"]["title"], j["guide"]["Stage C"]["next"]["speaker"])
    print (nextC)
    

def display_main():
    curPage = Page.MAIN
    
    w, h = display.get_bounds()
    
    display.set_pen(15)
    display.clear()
    display.set_pen(0)
    display.rectangle(0, 0, w, 10)
    display.rectangle(0, 0, 27, h)
    display.line(0, 49, w, 49)
    display.line(0, 89, w, 89)
    
    display.set_pen(15)
    display.set_font("bitmap8")
    display.set_thickness(4)
    display.text("EMF - Now and Next - Main Stages" , 50, 2, scale=1)
    
    s = 1.3
    display.set_pen(15)
    display.set_font("sans")
    display.set_thickness(4)
    display.text("A" , 2, 30, scale=s)
    display.text("B" , 0, 70, scale=s)
    display.text("C" , 0, 110, scale=s)
 
    s = 0.35
    l = 32
    display.set_pen(0)
    display.set_font("bitmap8")
    display.set_thickness(2)
    display.text(nowA , l, 15, scale=s)
    display.text(nextA , l, 30, scale=s)
    display.text(nowB , l, 55, scale=s)
    display.text(nextB , l, 70, scale=s)
    display.text(nowC , l, 95, scale=s)
    display.text(nextC , l, 110, scale=s)
    
    display.update()


def display_Stage(stage, nownext):
    
    w, h = display.get_bounds()
    
    display.set_pen(15)
    display.clear()
    display.set_pen(0)
    display.rectangle(0, 0, w, 10)
    display.rectangle(0, 0, 27, h)
    
    display.set_pen(15)
    display.set_font("bitmap8")
    display.set_thickness(4)
    display.text("EMF - {} - {}".format(nownext, stage) , 50, 2, scale=1) ####
    
    s = 1.3
    display.set_pen(15)
    display.set_font("sans")
    display.set_thickness(4)
    display.text(stage.replace("Stage ", "") , 0, 70, scale=s) ####

    s1 = 0.5
    s2 = 0.4
    l = 35
    display.set_pen(0)
    display.set_font("bitmap14_outline")
    display.set_thickness(1)
    try:
        a = j["guide"][stage][nownext]["start_time"] ####
    except:
        jpeg.open_file("/icons/icon-cryingTilda.jpg")
        jpeg.decode(178,10)
        display.set_pen(0)
        display.set_font("sans")
        display.set_thickness(2)
        display.text("Nothing", l, 50, scale=1.2 )
        display.text("{}".format(nownext), l, 85, scale=1.2 )
        
    else:
        display.set_font("bitmap14_outline")
        display.set_thickness(2)
        display.text("{} - {}".format(j["guide"][stage][nownext]["start_time"],j["guide"][stage][nownext]["end_time"]) , l, 15, scale=s1) ####
        display.text(j["guide"][stage][nownext]["title"], l, 30, scale=s2)  ####
        display.set_font("bitmap8")
        display.text(j["guide"][stage][nownext]["speaker"], l, 45, scale=1)  ####
        desc = j["guide"][stage][nownext]["description"]
        while desc.rfind("\r\n\r\n") != -1:
            desc = desc.replace("\r\n\r\n", "\r\n")
        display.text(desc, l, 60, wordwrap=w-l, scale=1.5)
    display.update()
    

get_data()
display_main()
badger2040.reset_pressed_to_wake()

while True:
    if display.pressed(badger2040.BUTTON_UP):
        lastPress = time.time()
        if curPage != Page.MAIN:
            display_main()
    if display.pressed(badger2040.BUTTON_DOWN):
        get_data()
        display_main()
    if display.pressed(badger2040.BUTTON_A):
        lastPress = time.time()
        if curPage == Page.NOWA:
            curPage = Page.NEXTA
            display_Stage("Stage A", "next")
        else:
            curPage = Page.NOWA
            display_Stage("Stage A", "now")
            
    if display.pressed(badger2040.BUTTON_B):
        lastPress = time.time()
        if curPage == Page.NOWB:
            curPage = Page.NEXTB
            display_Stage("Stage B", "next")
        else:
            curPage = Page.NOWB
            display_Stage("Stage B", "now")
            
    if display.pressed(badger2040.BUTTON_C):
        lastPress = time.time()
        if curPage == Page.NOWC:
            curPage = Page.NEXTC
            display_Stage("Stage C", "next")
        else:
            curPage = Page.NOWC
            display_Stage("Stage C", "now")
    
    if time.time() - lastPress > timeout:
        badger2040.sleep_for(sleeptime)