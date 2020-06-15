from sense_hat import SenseHat, ACTION_PRESSED, ACTION_RELEASED
sense = SenseHat()
import threading
import time
from pixel_art import *
import legend_of_zelda_maps
from legend_of_zelda_items import *

# Globals
playerThread = None
currentMap = None
linkXPosition = 3
linkYPosition = 6
hideLink = False
smallKeys = 0
d1_rd5_floor = False
d1_rd5_key = False
d1_rc6_key = False
d1_rc6_unlocked = False
d1_compass = False
d1_map = False

def check_doorway():
    global currentMap, linkXPosition, linkYPosition
    if currentMap == "d1_rc5":
        # Right doorway
        if linkXPosition == 7:
            # Middle
            if linkYPosition == 3 or linkYPosition == 4:
                # Set new map
                currentMap = "d1_rd5"
                # Draw the new map
                draw_map()
                # Move Link (Link will be drawn in the next playerThread cycle)
                linkXPosition = 1
    if currentMap == "d1_rd5":
        # Botton doorway
        if linkYPosition == 7:
           # Middle
           if linkXPosition == 3 or linkXPosition == 4:
                # Set new map
                currentMap = "d1_rd6"
                # Draw the new map
                draw_map()
                # Move Link (Link will be drawn in the next playerThread cycle)
                linkYPosition = 1
        # Left doorway
        if linkXPosition == 0:
            # Middle          
            if linkYPosition == 3 or linkYPosition == 4:
                # Set new map
                currentMap = "d1_rc5"
                # Draw the new map
                draw_map()
                # Move Link (Link will be drawn in the next playerThread cycle)
                linkXPosition = 6
        # Right doorway
        if linkXPosition == 7:
            # Middle
            if linkYPosition == 3 or linkYPosition == 4:
                # Set new map
                currentMap = "d1_re5"
                # Draw the new map
                draw_map()
                # Move Link (Link will be drawn in the next playerThread cycle)
                linkXPosition = 1               
    elif currentMap == "d1_re5":
        # Left doorway
        if linkXPosition == 0:
            # Middle          
            if linkYPosition == 3 or linkYPosition == 4:
                # Set new map
                currentMap = "d1_rd5"
                # Draw the new map
                draw_map()
                # Move Link (Link will be drawn in the next playerThread cycle)
                linkXPosition = 6
    elif currentMap == "d1_rd6":
        # Left doorway
        if linkXPosition == 0:
            # Middle          
            if linkYPosition == 3 or linkYPosition == 4:
                # Set new map
                currentMap = "d1_rc6"
                # Draw the new map
                draw_map()
                # Move Link (Link will be drawn in the next playerThread cycle)
                linkXPosition = 6
        # Top doorway
        if linkYPosition == 0:
            # Middle
            if linkXPosition == 3 or linkXPosition == 4:
                # Set new map
                currentMap = "d1_rd5"
                # Draw the new map
                draw_map()
                # Move Link (Link will be drawn in the next playerThread cycle)
                linkYPosition = 6
    elif currentMap == "d1_rc6":
        # Right doorway
        if linkXPosition == 7:
            # Middle
            if linkYPosition == 3 or linkYPosition == 4:
                # Set new map
                currentMap = "d1_rd6"
                # Draw the new map
                draw_map()
                # Move Link (Link will be drawn in the next playerThread cycle)
                linkXPosition = 1
        # Left doorway
        elif linkXPosition == 0:
            # Middle
            if linkYPosition == 3 or linkYPosition == 4:
                # Set new map
                currentMap = "d1_rb6"
                # Draw the new map
                draw_map()
                # Move Link (Link will be drawn in the next playerThread cycle)
                linkXPosition = 6
    elif currentMap == "d1_rb6":
        # Right doorway
        if linkXPosition == 7:
            # Middle
            if linkYPosition == 3 or linkYPosition == 4:
                # Set new map
                currentMap = "d1_rc6"
                # Draw the new map
                draw_map()
                # Move Link (Link will be drawn in the next playerThread cycle)
                linkXPosition = 1

# Returns true if there is a RGB value assigned to the given pixel
def check_pixel(x, y):
    global smallKeys, hideLink
    global d1_rd5_floor, d1_rd5_key, d1_rc6_key, d1_rc6_unlocked, d1_compass, d1_map
    returnValue = False
    try:
        rgb = sense.get_pixel(x, y)
        # Check for key pickup
        if rgb == [192, 192, 192]:
            smallKeys = smallKeys + 1
            show_small_key()
            if currentMap == "d1_rd5":
                d1_rd5_key = True
            if currentMap == "d1_rc6":
                d1_rc6_key = True
            returnValue = False
        # Check for item chest
        elif rgb == [128, 128, 0]:
            if currentMap == "d1_re5":
                d1_map = True
                show_map()
            elif currentMap == "d1_rb6":
                d1_compass = True
                show_compass()
        # Check for locked door or floor switch
        elif rgb == [144, 72, 0]:
            if currentMap == "d1_rd5":
                d1_rd5_floor = True
                sense.set_pixel(6, 2, 192, 192, 192)
            if smallKeys > 0:
                smallKeys = smallKeys - 1
                if currentMap == "d1_rd5":
                    d1_rd5_floor == True
                if currentMap == "d1_rc6":
                    d1_rc6_unlocked = True
                returnValue = False
        elif rgb != [0, 0, 0]:
            returnValue = True
    except:
        print()
    return returnValue

def clamp(value, min_value=0, max_value=7):
    return min(max_value, max(min_value, value))

def draw_link():
    if hideLink == False:
        sense.set_pixel(linkXPosition, linkYPosition, 0, 255, 0)

def draw_map():
    # Get the map variable using the map name
    result = getattr(legend_of_zelda_maps, currentMap)
    # Draw the map (Link will be drawn in the next playerThread cycle)
    sense.set_pixels(result)
    # Add item(s)
    if currentMap == "d1_rd5":
        # Floor Switch
        if d1_rd5_floor == False and d1_rd5_key == False:
            sense.set_pixel(4, 3, BRN)
        if d1_rd5_floor == True and d1_rd5_key == False:
            sense.set_pixel(6, 2, SLV)
    if currentMap == "d1_re5":
        # Map
        if d1_map == False:
            sense.set_pixel(6, 3, GLD)
    if currentMap == "d1_rc6":
        # Small Key
        if d1_rc6_key == False:
            sense.set_pixel(2, 3, SLV)
        # Locked Doors
        if d1_rc6_unlocked == False:
            sense.set_pixel(0, 3, BRN)
            sense.set_pixel(0, 4, BRN)
    if currentMap == "d1_rb6" and d1_compass == False:
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

def setup_controls():
    # Move
    sense.stick.direction_down = pushed_down
    sense.stick.direction_left = pushed_left
    sense.stick.direction_right = pushed_right
    sense.stick.direction_up = pushed_up
    sense.stick.direction_any = pushed_any

def show_compass():
    global hideLink
    sense.clear()
    sense.set_pixels(compass)
    hideLink = True;
    time.sleep(1.5)
    hideLink = False;
    draw_map()

def show_map():
    global hideLink
    sense.clear()
    sense.set_pixels(map)
    hideLink = True;
    time.sleep(1.5)
    hideLink = False;
    draw_map()

def show_small_key():
    global hideLink
    sense.clear()
    sense.set_pixels(small_key)
    hideLink = True;
    time.sleep(1.5)
    hideLink = False;
    draw_map()

def start():
    global currentMap
    sense.clear()
    setup_controls()
    currentMap = "d1_rd6"
    draw_map()
    player_thread()

start()