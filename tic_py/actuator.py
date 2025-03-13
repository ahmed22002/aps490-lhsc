# Uses ticcmd to send and receive data from the Tic over USB.
#
# NOTE: The Tic's control mode must be "Serial / I2C / USB"
# in order to set the target position over USB.

import subprocess
import yaml
import time
import random
import sys, signal


# Flags
VERBOSE = 0
RELATIVE_POSITIONING = 1



def signal_handler(sig, frame):
    done()
    sys.exit(0)

def ticcmd(*args):
    return subprocess.check_output(['ticcmd'] + list(args))

def get_curr_position():
    status = yaml.safe_load(ticcmd('-s', '--full'))
    position = status['Current position']
    if VERBOSE: print("Current position is {}.".format(position))
    return int(position)

def get_cur_velocity():
    status = yaml.safe_load(ticcmd('-s', '--full'))
    velocity = status['Current velocity']
    if VERBOSE: print("Current velocity is {}.".format(velocity))
    return int(velocity)

def set_position(position):
    if VERBOSE: print("Setting target position to {}.".format(position))
    ticcmd('--position', str(position))

def set_position_relative(position):
    if VERBOSE: print("Setting realtive position to {}.".format(position))
    ticcmd('--position-relative', str(position))

def position_uncertain():
    status = yaml.safe_load(ticcmd('-s', '--full'))
    uncertain = status['Position uncertain']
    if VERBOSE: print("Position uncertain is {}.".format(uncertain))
    return 1 if str(uncertain) == 'Yes' else 0
    
def set_max_speed(speed, units='mm'):
    if units == 'mm': speed = int(speed * 5500000)
    if units == 'steps': speed = int(speed * 10000)
    if VERBOSE: print("Setting max speed temporarily to {}.".format(speed))
    ticcmd('--max-speed', str(speed))

def set_velocity(velocity, units='mm'):
    if units == 'mm': velocity = int(velocity * 5500000)
    if units == 'steps': velocity = int(velocity * 10000)
    if VERBOSE: print("Setting target velocity to {}.".format(velocity))
    ticcmd('--velocity', str(velocity))

def setup():
    ticcmd('--reset')
    set_velocity(10)
    ticcmd('--resume')
    time.sleep(4)
    ticcmd("--deenergize")
    ticcmd("--halt-and-set-position", '27500')

    ticcmd('--deenergize')
    set_velocity(-15)
    ticcmd('--resume')
    time.sleep(4)
    ticcmd("--deenergize")
    ticcmd("--halt-and-set-position", '0')
    set_velocity(0)
    ticcmd('--resume')

def done():
    ticcmd('--reset')
    ticcmd('--resume')
    set_velocity(-15)
    time.sleep(4)
    ticcmd('--deenergize')

signal.signal(signal.SIGINT, signal_handler)
setup()
if RELATIVE_POSITIONING:
    for i in range(1000):
        speed = random.randrange(5, 15)
        relative_position = random.randrange(3437, 10313)
        set_max_speed(speed)
        curr_position = get_curr_position()
        
        if(curr_position < 27500/2):
            set_position_relative(relative_position)
            while(get_curr_position() < curr_position + relative_position): continue

        else:
            set_position_relative(relative_position * -1)
            while(get_curr_position() > curr_position - relative_position): continue
        
        if position_uncertain():
            print("Error: Position Uncertain! Exiting the program\n")
            done()
            sys.exit(1)    

else:
    for i in range(1000):
        velocity = random.randrange(5, 15)
        curr_position = get_curr_position()
       
        if(curr_position < 27500/2):
            target_position = random.randrange(curr_position, 22222)
            set_velocity(velocity)
            while(get_curr_position() < target_position): continue

        else:
            target_position = random.randrange(4444, curr_position)
            set_velocity(velocity * -1)
            while(get_curr_position() > target_position): continue
        
        if position_uncertain():
            print("Error: Position Uncertain! Exiting the program\n")
            done()
            sys.exit(1)    

done()
