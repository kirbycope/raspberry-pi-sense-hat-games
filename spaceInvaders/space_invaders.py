from sense_hat import SenseHat, ACTION_PRESSED, ACTION_RELEASED
sense = SenseHat()
import threading

# Worker threads
invaderThread = None
playerThread = None

# Laser Cannon
laserCannonXPosition = 3
laserCannonYPosition = 7

# projectile position
projectileXPosition = -1
projectileYPosition = -1

# Invader movement
invaderDirection = "right"
invaderPosition = 1

# Yellow invader (octopus)
octopusXPosition = 2
octopusHealth = 3

# Blue invaders (crab)
crab1XPosition = 1
crab1Health = 2
crab2XPosition = 3
crab2Health = 2

# Pink invaders (squid)
squid1XPosition = 0
squid1Health = 1
squid2XPosition = 2
squid2Health = 1
squid3XPosition = 4
squid3Health = 1

def clamp(value, min_value=0, max_value=7):
    return min(max_value, max(min_value, value))

def draw_invaders():
    # Yellow invader (octopus)
    if octopusHealth > 0:
        sense.set_pixel(octopusXPosition, 0, 255, 255, 0)
    # Blue invaders (crab)
    if crab1Health > 0:
        sense.set_pixel(crab1XPosition, 1, 0, 0, 255)
    if crab2Health > 0:
        sense.set_pixel(crab2XPosition, 1, 0, 0, 255)
    # Pink invaders (squid)
    if squid1Health > 0:
        sense.set_pixel(squid1XPosition, 2, 255, 0, 255)
    if squid2Health > 0:
        sense.set_pixel(squid2XPosition, 2, 255, 0, 255)
    if squid3Health > 0:
        sense.set_pixel(squid3XPosition, 2, 255, 0, 255)

def draw_projectile():
    if projectileYPosition > -1 and projectileXPosition > -1:
        sense.set_pixel(projectileXPosition, projectileYPosition, 255, 0, 0)
    else:
        reset_projectile()

def game_over():
    if squid1Health + squid2Health + squid3Health + crab1Health + crab2Health + octopusHealth == 0:
        invaderThread.cancel()
        playerThread.cancel()
        sense.show_letter("W")
        # Setup reset
        sense.stick.direction_left = None
        sense.stick.direction_right = None
        sense.stick.direction_middle = start

def invader_thread():
    global invaderThread
    invaderThread = threading.Timer(0.25, invader_thread)
    invaderThread.start()
    move_invaders()
    draw_invaders()

def move_invaders():
    global invaderDirection, invaderPosition, squid1XPosition, squid2XPosition, squid3XPosition, crab1XPosition, crab2XPosition, octopusXPosition
    # Clear the previous position of the Invader(s)
    sense.set_pixel(squid1XPosition, 2, 0, 0, 0)
    sense.set_pixel(squid2XPosition, 2, 0, 0, 0)
    sense.set_pixel(squid3XPosition, 2, 0, 0, 0)
    sense.set_pixel(crab1XPosition, 1, 0, 0, 0)
    sense.set_pixel(crab2XPosition, 1, 0, 0, 0)
    sense.set_pixel(octopusXPosition, 0, 0, 0, 0)
    # Set the new position of the Invader(s) based on thier direction
    if invaderPosition == 4:
        invaderDirection = "left"
    if invaderPosition == 1:
        invaderDirection = "right"
    if invaderDirection == "right":
        invaderPosition = invaderPosition + 1
        squid1XPosition = squid1XPosition + 1
        squid2XPosition = squid2XPosition + 1
        squid3XPosition = squid3XPosition + 1
        crab1XPosition = crab1XPosition + 1
        crab2XPosition = crab2XPosition + 1
        octopusXPosition = octopusXPosition + 1
    elif invaderDirection == "left":
        invaderPosition = invaderPosition - 1
        squid1XPosition = squid1XPosition - 1
        squid2XPosition = squid2XPosition - 1
        squid3XPosition = squid3XPosition - 1
        crab1XPosition = crab1XPosition - 1
        crab2XPosition = crab2XPosition - 1
        octopusXPosition = octopusXPosition - 1

def move_projectile():
    global projectileXPosition, projectileYPosition, squid1Health, squid2Health, squid3Health, crab1Health, crab2Health, octopusHealth
    # If there is a projectile on the playfield
    if projectileYPosition > -1 and projectileXPosition > -1:
        # Clear the last projectile position
        sense.set_pixel(projectileXPosition, projectileYPosition, 0, 0, 0)
        # Set the new projectile positiom
        projectileYPosition = projectileYPosition - 1
        # Did we hit any Squids?
        if projectileYPosition == 2:
            # Squid 1
            if projectileXPosition == squid1XPosition and squid1Health > 0:
                # Subtract 1 health point
                squid1Health = squid1Health - 1
                # Was the target eliminated?
                if squid1Health == 0:
                    # Remove the invader from the playfield
                    sense.set_pixel(squid1XPosition, 2, 0, 0, 0)
                # Reset the projectile
                reset_projectile()
            # Squid 2
            elif projectileXPosition == squid2XPosition and squid2Health > 0:
                # Subtract 1 health point
                squid2Health = squid2Health - 1
                # Was the target eliminated?
                if squid2Health == 0:
                    # Remove the invader from the playfield
                    sense.set_pixel(squid2XPosition, 2, 0, 0, 0)
                # Reset the projectile
                reset_projectile()
            # Squid 3
            elif projectileXPosition == squid3XPosition and squid3Health > 0:
                # Subtract 1 health point
                squid3Health = squid3Health - 1
                # Was the target eliminated?
                if squid3Health == 0:
                    # Remove the invader from the playfield
                    sense.set_pixel(squid3XPosition, 2, 0, 0, 0)
                # Reset the projectile
                reset_projectile()
        # Did we hit any Crabs?
        elif projectileYPosition == 1:
            # Crab 1
            if projectileXPosition == crab1XPosition and crab1Health > 0:
                # Subtract 1 health point
                crab1Health = crab1Health - 1
                # Was the target eliminated?
                if crab1Health == 0:
                    # Remove the invader from the playfield
                    sense.set_pixel(crab1XPosition, 1, 0, 0, 0)
                # Reset the projectile
                reset_projectile()
            # Crab 2
            elif projectileXPosition == crab2XPosition and crab2Health > 0:
                # Subtract 1 health point
                crab2Health = crab2Health - 1
                # Was the target eliminated?
                if crab2Health == 0:
                    # Remove the invader from the playfield
                    sense.set_pixel(crab2XPosition, 1, 0, 0, 0)
                # Reset the projectile
                reset_projectile()
        # Did we hit the Octopus?
        elif projectileYPosition == 0:
            # Octopus
            if projectileXPosition == octopusXPosition and octopusHealth > 0:
                # Subtract 1 health point
                octopusHealth = octopusHealth - 1
                # Was the target eliminated?
                if octopusHealth == 0:
                    # Remove the invader from the playfield
                    sense.set_pixel(octopusXPosition, 0, 0, 0, 0)
                # Reset the projectile
                reset_projectile()

def player_thread():
    global playerThread
    playerThread = threading.Timer(0.1, player_thread)
    playerThread.start()
    move_projectile()
    draw_projectile()
    game_over()

def pushed_left(event):
    global laserCannonXPosition
    if event.action != ACTION_RELEASED:
        sense.set_pixel(laserCannonXPosition, laserCannonYPosition, 0, 0, 0)
        laserCannonXPosition = clamp(laserCannonXPosition - 1)
        sense.set_pixel(laserCannonXPosition, laserCannonYPosition, 0, 255, 0)

def pushed_middle(event):
    global projectileXPosition, projectileYPosition
    # Only fire if no other projectile is on the playfield
    if event.action == ACTION_PRESSED and projectileXPosition == -1:
        projectileXPosition = laserCannonXPosition
        projectileYPosition = clamp(laserCannonYPosition - 1)
        sense.set_pixel(projectileXPosition, projectileYPosition, 255, 0, 0)

def pushed_right(event):
    global laserCannonXPosition
    if event.action != ACTION_RELEASED:
        sense.set_pixel(laserCannonXPosition, laserCannonYPosition, 0, 0, 0)
        laserCannonXPosition = clamp(laserCannonXPosition + 1)
        sense.set_pixel(laserCannonXPosition, laserCannonYPosition, 0, 255, 0)

def reset_projectile():
    global projectileXPosition, projectileYPosition
    projectileXPosition = -1
    projectileYPosition = -1

def setup_controls():
    # Fire
    sense.stick.direction_middle = pushed_middle
    # Move
    sense.stick.direction_left = pushed_left
    sense.stick.direction_right = pushed_right

def start():
    global squid1Health, squid2Health, squid3Health, crab1Health, crab2Health, octopusHealth
    squid1Health = 1
    squid2Health = 1
    squid3Health = 1
    crab1Health = 2
    crab2Health = 2
    octopusHealth = 3
    sense.clear()
    setup_controls()
    sense.set_pixel(laserCannonXPosition, laserCannonYPosition, 0, 255, 0)
    invader_thread()
    player_thread()

start()
