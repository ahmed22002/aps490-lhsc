# Uses ticcmd to send and receive data from the Tic over USB.
#
# NOTE: The Tic's control mode must be "Serial / I2C / USB"
# in order to set the target position over USB.

import math
import subprocess
import yaml
import time
import random
import sys, signal

# constants
RATIO = 44/11.5


# Flags
VERBOSE = 0

device_id = 0

def sleep(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()

def signal_handler(sig, frame):
    global device_id

    done(device_id)
    
    sys.exit(0)

def ticcmd(*args):
    return subprocess.check_output(['ticcmd'] + list(args))

def get_curr_position(device_id):
    status = yaml.safe_load(ticcmd('-d', device_id, '-s', '--full'))
    position = status['Current position']
    if VERBOSE: print("Current position is {}.".format(position))
    return int(position)

def get_cur_velocity(device_id):
    status = yaml.safe_load(ticcmd('-d', device_id, '-s', '--full'))
    velocity = status['Current velocity']
    if VERBOSE: print("Current velocity is {}.".format(velocity))
    return int(velocity)

def set_position(device_id, position):
    if VERBOSE: print("Setting target position to {}.".format(position))
    ticcmd('-d', device_id, '--position', str(int((position))))

def set_position_relative(device_id, position):
    if VERBOSE: print("Setting realtive position to {}.".format(position))
    ticcmd('-d', device_id, '--position-relative', str(position))

def position_uncertain(device_id):
    status = yaml.safe_load(ticcmd('-d', device_id, '-s', '--full'))
    uncertain = status['Position uncertain']
    if VERBOSE: print("Position uncertain is {}.".format(uncertain))
    return 1 if str(uncertain) == 'Yes' else 0
    
def set_max_speed(device_id, speed, units='mm'):
    if units == 'mm': speed = int(speed * 5500000)
    if units == 'steps': speed = int(speed * 10000)
    if VERBOSE: print("Setting max speed temporarily to {}.".format(speed))
    ticcmd('-d', device_id, '--max-speed', str(speed))

def set_velocity(device_id, velocity, units='mm'):
    if units == 'mm': velocity = int(velocity * 5500000)
    if units == 'steps': velocity = int(velocity * 10000)
    if VERBOSE: print("Setting target velocity to {}.".format(velocity))
    ticcmd('-d', device_id, '--velocity', str(velocity))

def setup(device_id):
    ticcmd('-d', device_id, '--reset')
    set_velocity(device_id, 10)
    ticcmd('-d', device_id, '--resume')
    sleep(2.5)
    ticcmd('-d', device_id, "--deenergize")
    ticcmd('-d', device_id, "--halt-and-set-position", '27500')

    ticcmd('-d', device_id, '--deenergize')
    set_velocity(device_id, -10)
    ticcmd('-d', device_id, '--resume')
    sleep(2.5)
    ticcmd('-d', device_id, "--deenergize")
    ticcmd('-d', device_id, "--halt-and-set-position", '0')
    set_velocity(device_id, 0)
    ticcmd('-d', device_id, '--resume')

def done(device_id):
    ticcmd('-d', device_id, '--reset')
    ticcmd('-d', device_id, '--resume')
    set_velocity(device_id, -5)
    sleep(3)
    ticcmd('-d', device_id, '--deenergize')

f = open('cmd_timings.txt', 'w')


cmd_out = ticcmd('--list').decode()
cmd_out = cmd_out.split()
device_id = cmd_out[0][0:-1]


signal.signal(signal.SIGINT, signal_handler)

set_velocity(device_id, -5)
ticcmd('-d', device_id, '--resume')
sleep(3)
ticcmd('-d', device_id, '--deenergize')
set_velocity(device_id, 0)
ticcmd('-d', device_id, '--resume')

time_start = time.perf_counter()
for i in range(10):
    set_velocity(device_id, 5)
    # f.write(str(time.perf_counter() - time_start)+'\n')
    sleep(3)
    # time_start = time.perf_counter()
    set_velocity(device_id, -5)
    # f.write(str(time.perf_counter() - time_start)+'\n')
    sleep(3)
f.write(str(time.perf_counter() - time_start)+'\n')
f.close()
done(device_id)