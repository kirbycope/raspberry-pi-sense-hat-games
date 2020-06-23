import threading
import time

from sense_hat import ACTION_PRESSED, ACTION_RELEASED, SenseHat

from pixel_art import BRN, GLD, GRN, NUL, SLV

sense = SenseHat()

playerThread = None
currentMap = "d1_d5"
linkXPosition = 3
linkYPosition = 6

smallKeys = 0
d1_d4_floor = False
d1_d4_key = False
d1_c5_key = False
d1_compass = False
d1_map = False

def clamp(value, min_value=0, max_value=7):
    return min(max_value, max(min_value, value))

def check_doorway():
    global currentMap, linkXPosition, linkYPosition
    # Exit Tail Cave
    if currentMap == "d1_d5" and linkYPosition == 7:
        # Set new map
        currentMap = "ki_d14"
        # Draw the new map
        draw_map()
        # Move Link
        linkYPosition = 1
        # Draw Link
        draw_link()
    # Enter Tail Cave
    elif currentMap == "ki_d14" and linkYPosition == 0:
        # Set new map
        currentMap = "d1_d5"
        # Draw the new map
        draw_map()
        # Move Link
        linkYPosition = 6
        # Draw Link
        draw_link()
    else:
        dungeon = currentMap[0:2]
        column = currentMap[3]
        row = currentMap[4:]
        # Top doorway
        if linkYPosition == 0:
            # Set new map
            row = int(row) - 1
            currentMap = dungeon + "_" + column + str(row)
            # Draw the new map
            draw_map()
            # Move Link
            linkYPosition = 6
            # Draw Link
            draw_link()
        # Botton doorway
        if linkYPosition == 7:
            # Set new map
            row = int(row) + 1
            currentMap = dungeon + "_" + column + str(row)
            # Draw the new map
            draw_map()
            # Move Link
            linkYPosition = 1
            # Draw Link
            draw_link()
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
            # Move Link
            linkXPosition = 1
            # Draw Link
            draw_link()
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
            # Move Link
            linkXPosition = 6
            # Draw Link
            draw_link()

# Returns True if there is a colored pixel in the given x, y coordinates.
def check_pixel(x, y):
    global currentMap, linkXPosition, linkYPosition, smallKeys
    global d1_d4_floor, d1_d4_key, d1_c5_key, d1_compass, d1_map
    # Get the RGB value of the given pixel
    rgb = sense.get_pixel(clamp(x), clamp(y))
    # Check for key pickup
    if rgb == SLV:
        smallKeys = smallKeys + 1
        if currentMap == "d1_d4":
            d1_d4_key = True
        if currentMap == "d1_c5":
            d1_c5_key = True
        show_item("loz_small_key")
    # Check for item chest
    elif rgb == GLD:
        # Dungeon map
        if currentMap == "d1_e4":
            d1_map = True
            show_item("loz_dungeon_map")
        # Compass
        elif currentMap == "d1_b5":
            d1_compass = True
            show_item("loz_compass")
    # Check for locked door, floor switch, or stairs
    elif rgb == BRN or rgb == [144, 72, 0]:
        # Floors
        if currentMap == "d1_d4":
            # Set the floor to "switched"
            d1_d4_floor = True
            if d1_d4_key == False:
                sense.set_pixel(4, 3, NUL)
                draw_keys()
        # Stairs
        elif currentMap == "d1_b1":
            currentMap = "d1_a4"
            # Draw the new map
            draw_map()
            # Move Link
            linkXPosition = 4
            linkYPosition = 4
            # Draw Link
            draw_link()
            return True
        # Stairs
        elif currentMap == "d1_a4":
            currentMap = "d1_b1"
            # Draw the new map
            draw_map()
            # Move Link
            linkXPosition = 6
            linkYPosition = 2
            # Draw Link
            draw_link()
            return True
        else:
            # Doors
            if smallKeys > 0:
                smallKeys = smallKeys - 1
                # todo: set the unlocked var for the door
            else:
                return True
    elif rgb != NUL:
        return True
    return False

# Removes the event listeners for the Sense Hat joystick
def disable_controls():
    sense.stick.direction_down = None
    sense.stick.direction_left = None
    sense.stick.direction_right = None
    sense.stick.direction_up = None
    sense.stick.direction_middle = None

# Sets the event listeners for the Sense Hat joystick
def enable_controls():
    sense.stick.direction_down = pushed_down
    sense.stick.direction_left = pushed_left
    sense.stick.direction_right = pushed_right
    sense.stick.direction_up = pushed_up
    sense.stick.direction_middle = pushed_middle

def draw_doors():
    if currentMap == "d1_c2":
        sense.set_pixel(3, 0, BRN)
        sense.set_pixel(4, 0, BRN)
    if currentMap == "d1_e3":
        sense.set_pixel(7, 3, BRN)
        sense.set_pixel(7, 4, BRN)

def draw_floor_switches():
    if currentMap == "d1_d4":
        # Floor Switch
        if d1_d4_floor == False:
            sense.set_pixel(4, 3, BRN)
        if d1_d4_floor == True and d1_d4_key == False:
            sense.set_pixel(6, 2, SLV)

def draw_keys():
    if currentMap == "d1_c5":
        if d1_c5_key == False:
            sense.set_pixel(2, 2, SLV)
    elif currentMap == "d1_d4":
        if d1_d4_floor == True and d1_d4_key == False:
            sense.set_pixel(6, 2, SLV)

# Sets pixel to green based on Link's coordinates
def draw_link():
    sense.set_pixel(linkXPosition, linkYPosition, GRN)

# Sets pixels based on the current map
def draw_map():
    try:
        # Get the map variable using the map name
        sense.load_image("legendOfZelda/img/" + currentMap + ".bmp")
    except:
        restart()
    # Add item(s)
    draw_doors()
    draw_floor_switches()
    draw_keys()
    draw_stairs()
    if currentMap == "d1_e4":
        # Map
        if d1_map == False:
            sense.set_pixel(6, 3, GLD)
    if currentMap == "d1_b5" and d1_compass == False:
        # Compass
        sense.set_pixel(3, 3, GLD)

def draw_stairs():
    if currentMap == "d1_b1":
        sense.set_pixel(6, 1, BRN)
    elif currentMap == "d1_a4":
        sense.set_pixel(4, 5, BRN)

def player_thread():
    global playerThread
    playerThread = threading.Timer(0.1, player_thread)
    playerThread.start()

def pushed_down(event):
    global linkYPosition
    if event.action != ACTION_RELEASED:
        # Get the next potential pixel position
        potentialYPosition = linkYPosition + 1
        # If we are at the edge of the map, then we must be at a doorway
        if potentialYPosition > 7:
            check_doorway()
        # If nothing is in the potential position
        elif check_pixel(linkXPosition, potentialYPosition) == False:
            # Remove the current position
            sense.set_pixel(linkXPosition, linkYPosition, NUL)
            # Set the new position
            linkYPosition = clamp(linkYPosition + 1)
            # Draw link at the new position (this does happen in the player thread but the event listener on the joystick can fire multiple times before draws)
            draw_link()

def pushed_left(event):
    global linkXPosition
    if event.action != ACTION_RELEASED:
        # Get the next potential pixel position
        potentialXPosition = linkXPosition - 1
        # If we are at the edge of the map, then we must be at a doorway
        if potentialXPosition < 0:
            check_doorway()
        # If we can draw in the potential position
        elif check_pixel(potentialXPosition, linkYPosition) == False:
            # Remove the current position
            sense.set_pixel(linkXPosition, linkYPosition, NUL)
            # Set the new position
            linkXPosition = clamp(linkXPosition - 1)
            # Draw link at the new position (this does happen in the player thread but the event listener on the joystick can fire multiple times before draws)
            draw_link()

def pushed_middle(event):
    #restart()
    print()

def pushed_right(event):
    global linkXPosition
    if event.action != ACTION_RELEASED:
        # Get the next potential pixel position
        potentialXPosition = linkXPosition + 1
        # If we are at the edge of the map, then we must be at a doorway
        if potentialXPosition > 7:
            check_doorway()
        # If nothing is in the potential position
        if check_pixel(potentialXPosition, linkYPosition) == False:
            # Remove the current position
            sense.set_pixel(linkXPosition, linkYPosition, NUL)
            # Set the new position
            linkXPosition = clamp(linkXPosition + 1)
            # Draw link at the new position (this does happen in the player thread but the event listener on the joystick can fire multiple times before draws)
            draw_link()

def pushed_up(event):
    global linkYPosition
    if event.action != ACTION_RELEASED:
        # Get the next potential pixel position
        potentialYPosition = linkYPosition - 1
        # If we are at the edge of the map, then we must be at a doorway
        if potentialYPosition < 0:
            check_doorway()
        # If nothing is in the potential position
        elif check_pixel(linkXPosition, potentialYPosition) == False:
            # Remove the current position
            sense.set_pixel(linkXPosition, linkYPosition, NUL)
            # Set the new position
            linkYPosition = clamp(linkYPosition - 1)
            # Draw link at the new position (this does happen in the player thread but the event listener on the joystick can fire multiple times before draws)
            draw_link()

def show_item(itemName):
    disable_controls()
    sense.clear()
    sense.load_image("legendOfZelda/img/" + itemName + ".bmp")
    time.sleep(1.5)
    draw_map()
    draw_link()
    enable_controls()

def restart():
    global playerThread, currentMap, linkXPosition, linkYPosition, hideLink, smallKeys
    global d1_d4_floor, d1_d4_key, d1_c5_key, d1_compass, d1_map
    playerThread = None
    currentMap = "d1_d5"
    linkXPosition = 3
    linkYPosition = 6
    hideLink = False
    smallKeys = 0
    d1_d4_floor = False
    d1_d4_key = False
    d1_c5_key = False
    d1_compass = False
    d1_map = False
    start()

def start():
    show_item("loz_link")
    sense.clear()
    sense.low_light = True
    enable_controls()
    draw_map()
    draw_link()
    player_thread()

start()
