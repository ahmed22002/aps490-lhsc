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

def sleep(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()

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
    ticcmd('--position', str(int((position))))

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
    time.sleep(2.5)
    ticcmd("--deenergize")
    ticcmd("--halt-and-set-position", '27500')

    ticcmd('--deenergize')
    set_velocity(-10)
    ticcmd('--resume')
    time.sleep(2.5)
    ticcmd("--deenergize")
    ticcmd("--halt-and-set-position", '0')
    set_velocity(0)
    ticcmd('--resume')

def done():
    ticcmd('--reset')
    ticcmd('--resume')
    set_velocity(-5)
    time.sleep(3)
    ticcmd('--deenergize')

signal.signal(signal.SIGINT, signal_handler)
set_velocity(-5)
ticcmd('--resume')
time.sleep(3)
ticcmd('--deenergize')
set_velocity(0)
ticcmd('--resume')

# f = open("input.qrm")
# lines = f.readlines()
# f.close()

# samples_to_skip = 1
# sleep_time = (1/1.5)*(samples_to_skip)
# velocity_list = []

# prev_val = float(lines[3])

# f = open('velocity_list.txt', 'w')
# biggest = 0
# for i in range(3+samples_to_skip, 26720, samples_to_skip):
#     velocity_small = float(10 * (float(lines[i]) - prev_val)/sleep_time)
#     velocity_big = velocity_small / RATIO
#     velocity_list.append(velocity_big)
#     f.write(f"{velocity_small}\n")
#     biggest = max(biggest, velocity_small)
#     prev_val = float(lines[i])
# print(biggest)
# f.close()

# starting_position_small = 1.2 + float(lines[3])
# starting_position_big = 10 * starting_position_small / RATIO

# set_velocity(3)
# sleep(starting_position_big/3)

# for velocity in velocity_list:
#     set_velocity(velocity)
#     sleep(sleep_time)


####################################

velocity_list = []
period = math.pi/2
for j in range(0, 180 * 10, 9):
    velocity_list.append(4*math.sin(4 * j/360 * math.pi))
    
for velocity in velocity_list:
        #time_start = time.perf_counter()
        set_velocity(velocity)
        #print(time.perf_counter() - time_start)
        if (velocity == 0): continue
        sleep(period/20)

####################################


# set_position(0)
# position_list = []
# period = math.pi/2
# f = open('velocity_list.txt', 'w')
# for j in range(0, 180 * 10, 9):
#     pos = (2*math.sin(4 * j/360 * math.pi - math.pi/2) + 2)
#     position_list.append(pos/0.0018)
#     f.write(f"{pos ,pos/0.0018}\n")
# f.close()

# for position in position_list:
#         #time_start = time.perf_counter()
#         set_position(position)
#         while(get_cur_velocity() > 0):
#             continue
#         #print(time.perf_counter() - time_start)
#         # if (math.sin(math.pi * j/180) == 0): continue

done()
# 4.2 0.9