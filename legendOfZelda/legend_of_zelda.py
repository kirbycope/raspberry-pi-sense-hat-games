from sense_hat import SenseHat, ACTION_PRESSED, ACTION_RELEASED
sense = SenseHat()
import threading
import time
from pixel_art import *
from legend_of_zelda_items import *

playerThread = None
currentMap = "d1_d5"
linkXPosition = 3
linkYPosition = 6
hideLink = False

smallKeys = 0
d1_d4_floor = False
d1_d4_key = False
d1_c5_key = False
d1_c5_unlocked = False
d1_compass = False
d1_map = False

def clamp(value, min_value=0, max_value=7):
    return min(max_value, max(min_value, value))

def check_doorway():
    global currentMap, linkXPosition, linkYPosition
    dungeon = currentMap[0:2]
    cell = currentMap[3:]
    column = cell[0]
    row = cell[1]
    # Top doorway
    if linkYPosition == 0:
        # Set new map
        row = int(row) - 1
        currentMap = dungeon + "_" + column + str(row)
        # Draw the new map
        draw_map()
        # Move Link (Link will be drawn in the next playerThread cycle)
        linkYPosition = 6
    # Botton doorway
    if linkYPosition == 7:
        # Set new map
        row = int(row) + 1
        currentMap = dungeon + "_" + column + str(row)
        # Draw the new map
        draw_map()
        # Move Link (Link will be drawn in the next playerThread cycle)
        linkYPosition = 1
    # Right doorway
    if linkXPosition == 7:
        # Set new map
        if column == "a":
            column = "b"
        elif column == "b":
            column = "c"
        elif column == "c":
            column = "d"
        elif column == "d":
            column = "e"
        elif column == "e":
            column = "f"
        elif column == "f":
            column = "g"
        currentMap = dungeon + "_" + column + row
        # Draw the new map
        draw_map()
        # Move Link (Link will be drawn in the next playerThread cycle)
        linkXPosition = 1
    # Left doorway
    if linkXPosition == 0:
        # Set new map
        if column == "g":
            column = "f"
        elif column == "f":
            column = "e"
        elif column == "e":
            column = "d"
        elif column == "d":
            column = "c"
        elif column == "c":
            column = "b"
        elif column == "b":
            column = "a"
        currentMap = dungeon + "_" + column + row
        # Draw the new map
        draw_map()
        # Move Link (Link will be drawn in the next playerThread cycle)
        linkXPosition = 6

# Returns True if there is a colored pixel in the given x,y coordinates.
def check_pixel(x, y):
    global smallKeys, hideLink
    global d1_d4_floor, d1_d4_key, d1_c5_key, d1_c5_unlocked, d1_compass, d1_map
    returnValue = False
    try:
        rgb = sense.get_pixel(x, y)
        # Check for key pickup
        if rgb == SLV:
            smallKeys = smallKeys + 1
            if currentMap == "d1_d4":
                d1_d4_key = True
            if currentMap == "d1_c5":
                d1_c5_key = True
            show_small_key()
            returnValue = False
        # Check for item chest
        elif rgb == GLD:
            # Dungeon map
            if currentMap == "d1_e4":
                d1_map = True
                show_map()
            # Compass
            elif currentMap == "d1_b5":
                d1_compass = True
                show_compass()
        # Check for locked door or floor switch
        elif rgb == BRN or rgb == [144, 72, 0]:
            # Floors
            if currentMap == "d1_d4":
                # Set the floor to "switched"
                d1_d4_floor = True
                if d1_d4_key == False:
                    # Show the small key
                    draw_keys()
                returnValue = False
            # Doors
            if smallKeys > 0:
                smallKeys = smallKeys - 1
                if currentMap == "d1_c5":
                    d1_c5_unlocked = True
            else:
                returnValue = True
        elif rgb != [0, 0, 0]:
            returnValue = True
    except:
        print()
    return returnValue

# Removes the event listeners for the Sense Hat joystick
def disable_controls():
    sense.stick.direction_down = None
    sense.stick.direction_left = None
    sense.stick.direction_right = None
    sense.stick.direction_up = None
    sense.stick.direction_any = None
    sense.stick.direction_middle = None

# Sets the event listeners for the Sense Hat joystick
def enable_controls():
    sense.stick.direction_down = pushed_down
    sense.stick.direction_left = pushed_left
    sense.stick.direction_right = pushed_right
    sense.stick.direction_up = pushed_up
    sense.stick.direction_any = pushed_any
    sense.stick.direction_middle = pushed_middle

def draw_doors():
    if currentMap == "d1_c5":
        if d1_c5_unlocked == False:
            sense.set_pixel(0, 3, BRN)
            sense.set_pixel(0, 4, BRN)

def draw_keys():
    if currentMap == "d1_c5":
        if d1_c5_key == False:
            sense.set_pixel(1, 2, SLV)
    elif currentMap == "d1_d4":
        if d1_d4_floor == True and d1_d4_key == False:
            sense.set_pixel(6, 1, SLV)

# Sets pixel to green based on Link's coordinates
def draw_link():
    if hideLink == False:
        sense.set_pixel(linkXPosition, linkYPosition, GRN)

# Sets pixels based on the current map
def draw_map():
    # Get the map variable using the map name
    sense.load_image("legendOfZelda/img/" + currentMap + ".bmp")
    # Add item(s)
    draw_doors()
    draw_keys()
    if currentMap == "d1_d4":
        # Floor Switch
        if d1_d4_floor == False and d1_d4_key == False:
            sense.set_pixel(4, 3, BRN)
        if d1_d4_floor == True and d1_d4_key == False:
            sense.set_pixel(6, 2, SLV)
    if currentMap == "d1_e4":
        # Map
        if d1_map == False:
            sense.set_pixel(6, 3, GLD)
    if currentMap == "d1_b5" and d1_compass == False:
        # Compass
        sense.set_pixel(3, 3, GLD)

def player_thread():
    global playerThread
    playerThread = threading.Timer(0.1, player_thread)
    playerThread.start()
    draw_link()

def pushed_any():
    check_doorway()

def pushed_down(event):
    global linkYPosition
    if event.action != ACTION_RELEASED:
        # Get the next potential pixel position
        potentialYPosition = linkYPosition + 1
        # If nothing in in the potential position
        if check_pixel(linkXPosition, potentialYPosition) == False:
            # Remove the current position
            sense.set_pixel(linkXPosition, linkYPosition, 0, 0, 0)
            # Set the new position
            linkYPosition = clamp(linkYPosition + 1)
        
def pushed_left(event):
    global linkXPosition
    if event.action != ACTION_RELEASED:
        # Get the next potential pixel position
        potentialXPosition = linkXPosition - 1
        # If we can draw in the potential position
        if check_pixel(potentialXPosition, linkYPosition) == False:
            # Remove the current position
            sense.set_pixel(linkXPosition, linkYPosition, 0, 0, 0)
            # Set the new position
            linkXPosition = clamp(linkXPosition - 1)

def pushed_middle(event):
    restart()

def pushed_right(event):
    global linkXPosition
    if event.action != ACTION_RELEASED:
        # Get the next potential pixel position
        potentialXPosition = linkXPosition + 1
        # If nothing in in the potential position
        if check_pixel(potentialXPosition, linkYPosition) == False:
            # Remove the current position
            sense.set_pixel(linkXPosition, linkYPosition, 0, 0, 0)
            # Set the new position
            linkXPosition = clamp(linkXPosition + 1)
        
def pushed_up(event):
    global linkYPosition
    if event.action != ACTION_RELEASED:
        # Get the next potential pixel position
        potentialYPosition = linkYPosition - 1
        # If nothing in in the potential position
        if check_pixel(linkXPosition, potentialYPosition) == False:
            # Remove the current position
            sense.set_pixel(linkXPosition, linkYPosition, 0, 0, 0)
            # Set the new position
            linkYPosition = clamp(linkYPosition - 1)

def show_compass():
    global hideLink
    sense.clear()
    sense.set_pixels(compass)
    hideLink = True
    disable_controls()
    time.sleep(1.5)
    hideLink = False
    enable_controls()
    draw_map()

def show_map():
    global hideLink
    sense.clear()
    sense.set_pixels(dungeon_map)
    hideLink = True
    disable_controls()
    time.sleep(1.5)
    hideLink = False
    enable_controls()
    draw_map()

def show_small_key():
    global hideLink
    sense.clear()
    sense.set_pixels(small_key)
    hideLink = True
    disable_controls()
    time.sleep(1.5)
    hideLink = False
    enable_controls()
    draw_map()

def restart():
    global playerThread, currentMap, linkXPosition, linkYPosition, hideLink, smallKeys
    global d1_d4_floor, d1_d4_key, d1_c5_key, d1_c5_unlocked, d1_compass, d1_map
    playerThread = None
    currentMap = "d1_d5"
    linkXPosition = 3
    linkYPosition = 6
    hideLink = False
    smallKeys = 0
    d1_d4_floor = False
    d1_d4_key = False
    d1_c5_key = False
    d1_c5_unlocked = False
    d1_compass = False
    d1_map = False
    start()

def start():
    sense.clear()
    enable_controls()
    draw_map()
    player_thread()

start()
