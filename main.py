import time
from pimoroni import Button, RGBLED
from machine import Pin
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4

# We're only using a few colours so we can use a 4 bit/16 colour palette and save RAM!
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)

display.set_backlight(0.8)
display.set_font("bitmap6")

WIDTH, HEIGHT = display.get_bounds()

led = RGBLED(6, 7, 8)
led.set_rgb(0, 0, 0)

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
BLUE = display.create_pen(10, 220, 252)
RED = display.create_pen(252, 21, 0)
YELLOW = display.create_pen(252, 223, 2)
GREEN = display.create_pen(62, 188, 98)

turn = 1 # 1 or 2
setupTime = 600
setupIncrement = 0

player1time = 0
player2time = 0

def convert(seconds):
    minutes = int(seconds / 60)
    seconds = int(seconds % 60)
    return str(minutes)+":"+str('{0:02d}'.format(seconds))


# sets up a handy function we can call to clear the screen
def clear(color):
    display.set_pen(color)
    display.clear()
    display.update()
    
def getStartPos(text):
    textWidth = display.measure_text(convert(text), 5)
    startPos = int((HEIGHT - textWidth) / 2)
    return startPos

def displayTime(turn):
    if turn == 1:
        display.set_pen(GREEN)
        display.rectangle(30, 0, 50, 200)
        display.set_pen(WHITE)
        display.text(convert(player1time), 65, getStartPos(player1time), 50, 5, 90)
    elif turn == 2:
        display.set_pen(GREEN)
        display.rectangle(160, 0, 50, 200)
        display.set_pen(WHITE)
        display.text(convert(player2time), 175, 130-getStartPos(player2time), 50, 5, 270)

def chessTimer(seconds, increment):
    global player1time, player2time, turn
    player1time = seconds
    player2time = seconds
    clear(GREEN)
    display.set_pen(WHITE)
    display.text("PLAYER 1", 27, 27, 100, 2, 90)
    display.text("PLAYER 2", 213, 108, 100, 2, 270)
    display.text(convert(player1time), 65, getStartPos(player1time), 50, 5, 90)
    display.text(convert(player2time), 175, 130-getStartPos(player2time), 50, 5, 270)
    
    start_time = time.ticks_ms()
    elapsed = 0
    
    while player1time > 0 and player2time > 0:
        current_time = time.ticks_ms()
        elapsed = time.ticks_diff(current_time, start_time)
        
        if button_x.read():
            switchTurn()
        if button_y.read():
            switchTurn()
        if button_a.read():
            switchTurn()
        if button_b.read():
            switchTurn()

        if elapsed >= 1000:  # 1 second passed
            if turn == 1:
                player1time -= 1
            else:
                player2time -= 1
            start_time = current_time  # reset timer

        # Always redraw and update display (as fast as possible)
        displayTime(turn)
        display.update()

        # Small sleep to avoid hogging CPU — 10ms is fine
        time.sleep(0.01)
            
def displaySetupTime(string):
    display.set_pen(GREEN)
    display.rectangle(0, 36, 240, 50)
    
    display.set_pen(WHITE)
    textWidth = display.measure_text(convert(string), 6)
    startPos = int((WIDTH - textWidth) / 2)
    display.text(convert(string), startPos, 40, 240, 6)
    
    display.update()
    
def countdown():
    startPos = 110
    
    clear(GREEN)
    display.set_pen(WHITE)
    display.text("3", startPos, 50, 240, 6)
    display.update()
    time.sleep(1)
    
    clear(GREEN)
    display.set_pen(WHITE)
    display.text("2", startPos, 50, 240, 6)
    display.update()
    time.sleep(1)
    
    clear(GREEN)
    display.set_pen(WHITE)
    display.text("1", startPos, 50, 240, 6)
    display.update()
    time.sleep(1)
    
    clear(GREEN)
 
debounce_time = 20  # Debounce time in milliseconds
last_press_time = 0
def switchTurn():
    global last_press_time
    current_time = time.ticks_ms()
    
    if current_time - last_press_time > debounce_time:
        global turn, player1time, player2time, setupIncrement
        if turn == 1:
            player1time += setupIncrement
            displayTime(turn)
            turn = 2
        else:
            player2time += setupIncrement
            displayTime(turn)
            turn = 1
        last_press_time = current_time
            
            
            
clear(GREEN)

while True:
    if button_a.read():
        time.sleep(0.2)
        clear(GREEN)
        display.set_pen(WHITE)
        
        display.text("<", 10, 10, 240, 4)
        display.text("-", 15, 85, 240, 6)
        display.text("+", 210, 85, 240, 6)
        
        display.text("PER PERSON", 65, 98, 240, 2)
        
        displaySetupTime(setupTime)
        
        while button_a.read() == False: # Change the time
            if button_y.read():
                setupTime += 30
                displaySetupTime(setupTime)
                time.sleep(0.2)
            if button_b.read():
                if setupTime - 30 != 0:
                    setupTime -= 30
                displaySetupTime(setupTime)
                time.sleep(0.2)
        
        clear(GREEN)
        time.sleep(0.2)
        
    elif button_b.read(): # Change the increment
        time.sleep(0.2)
        clear(GREEN)
        display.set_pen(WHITE)
        
        display.text("<", 10, 10, 240, 4)
        display.text("-", 15, 85, 240, 6)
        display.text("+", 210, 85, 240, 6)
        
        display.text("PER MOVE", 75, 98, 240, 2)
        
        displaySetupTime(setupIncrement)
        
        while button_a.read() == False:
            if button_y.read():
                setupIncrement += 1
                displaySetupTime(setupIncrement)
                time.sleep(0.2)
            if button_b.read():
                if setupIncrement != 0:
                    setupIncrement -= 1
                displaySetupTime(setupIncrement)
                time.sleep(0.2)
        
        clear(GREEN)
        time.sleep(0.2)
        
    elif button_x.read(): # start the chess clock
        countdown()
        chessTimer(setupTime, setupIncrement)
        machine.reset()
    else:
        display.set_pen(WHITE)
        fs = 3
        display.text("TIME", 10, 20, 240, fs)
        display.text("INCREMENT", 10, 95, 240, fs)
        
        display.text("START", 140, 20, 240, fs)
        display.update()
    time.sleep(0.1)  # this number is how frequently the Pico checks for button presses
