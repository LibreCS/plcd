from ctypes import sizeof
from lib2to3.pygram import python_grammar_no_print_statement
import os
import sys
import socket
import datetime
import time
 
 
#=========== CONFIGURATION ===========================================
 
# set monitoring frequency (pings/min)
UP_PING_FREQ = 5
# set monitoring frequency when down (pings/min)
DOWN_PING_FREQ = 3
# print downtime interval (min)
DOWN_PRINT_INT = 20
#=====================================================================
portName = [str(""), str("")]
portNum = [int(), int()]
 
# setting log file name & dir
FILE = os.path.join(os.getcwd(), "plc_uptime.log")
 
def configure():
 
    class bcolors:
        HEADER = '\033[95m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        ORANGE = '\033[93m'
        RED = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
 
 
    addressInMsg = "Enter PLC Plant Network Address (ex. 10.48.84.XXX): "
 
    portIngest()
 
    hostUsrIn = input(addressInMsg)
 
    if hostValid(hostUsrIn):
        port = portSniff(hostUsrIn, portNum, portName)
        print("\n"+portName[port]+" found on port "+portNum[port]+", connecting...")
        return str(hostUsrIn)+":"+str(portNum[port])
 
    else:
        print("\n")
        if not hostValid(hostUsrIn):
            print(bcolors.RED+"Error: PLC IP address invalid, try again"+bcolors.ENDC)
        if not portValid(portUsrIn):
            print(bcolors.RED+"Error: PLC network port invalid, try again"+bcolors.ENDC)
        print("\n")
 
        return "error"
 
def hostValid(hostUsrIn):
    # parse IP address for each quartet
    hostParse = hostUsrIn.split(".")
 
    # check for 4 quartet length
    if len(hostParse) == 4:
        # proceed
        # interate on array length
        for i in hostParse:
            # check for out of bounds IP quartet
            if int(i) > 255:
                return False
        # after quartet limits verified return true
        return True   
    else:
        return False
 
def portValid(portUsrIn):
    # locking port as int
    port = int(portUsrIn)
 
    # determining port in bounds
    if int(port) > 0 & int(port) < 100000:
        return True
    else:
        return False
 
def ping(host, port):
    # to ping a particular IP
    try:
        socket.setdefaulttimeout(5)
 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # AF_INET: address family
        # SOCK_STREAM: type for TCP
 
        server_address = (host, port)
        s.connect(server_address)
 
    except OSError as error:
        return False
        # after data interruption
 
    else:
        s.close()
        return True
 
def portSniff(inputAddress, portNum, portName):
    for i in portNum:
        if ping(inputAddress, i):
            return i
 
def calculate_time(start, stop):
    difference = stop - start
    seconds = float(str(difference.total_seconds()))
    return str(datetime.timedelta(seconds=seconds)).split(".")[0]
 
def portIngest():
    i = 0
    line = [str(), str()]
    # opening PLC ports static datafile
    with open('plc-ports.dat') as f:
        line[i] = f.readline()
        while line != '':
            portName[i], portNum[i] = line[i].split(":", 1)
            portName[int(portNum[i])] = portName[i]
        f.close()
 
 
def first_check(host, port):
 
    if ping(host, port):
        # if ping returns true
        live = "\nPLC connection acquired ... Monitoring...\n"
        print(live)
        connection_acquired_time = datetime.datetime.now()
        acquiring_message = "Connection acquired for "+host+" at: " + \
            str(connection_acquired_time).split(".")[0]
        print(acquiring_message)
 
        with open(FILE, "a") as file: 
            # writes into the log file
            file.write(live)
            file.write(acquiring_message)
        return True
 
    else:
        # if ping returns false
        not_live = "\nPLC connection not acquired ... Searching...\n"
        print(not_live)
 
        with open(FILE, "a") as file:
            # writes into the log file
            file.write(not_live)
        return False
 
def main():
 
    class bcolors:
        HEADER = '\033[95m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        ORANGE = '\033[93m'
        RED = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
 
    # plcd ASCII art
    print(bcolors.CYAN+"           __         __\n    ____  / /________/ /\n   / __ \/ / ___/ __  / \n  / /_/ / / /__/ /_/ /  \n / .___/_/\___/\__,_/   \n/_/                     \n"+bcolors.ENDC)
    # title & print
    welcomeMsg = bcolors.HEADER + bcolors.BOLD + "Developed by LibreCS, licensed under GNU GPLv3. Learn more and contribute at https://github.com/LibreCS/plcd" + bcolors.ENDC
    print(welcomeMsg+"\n\n")
 
    # monitoring configuration & loop
    netLocationPLC = configure()
    while netLocationPLC == "error":
        netLocationPLC = configure()
 
    # parsing configuration output for host and port 
    hostParse, portParse =  netLocationPLC.split(":", 1)
    host = str(hostParse)
    port = int(portParse)
 
    # main function to call functions
    monitor_start_time = datetime.datetime.now()
    monitoring_date_time = "Uptime monitoring started at: " + \
        str(monitor_start_time).split(".")[0]
 
    # call first check function, decide loop path
    if first_check(host, port):
        # if true
        print(monitoring_date_time)
        # monitoring will only start after connection acquired
 
    else:
        # if false
        i = 0
        while True:
            # infinite loop to see if the connection is acquired
            if not ping(host, port):
                # if connection not acquired
                # uptime tests every defined interval
 
                time.sleep(60/DOWN_PING_FREQ)
 
                if (((i/DOWN_PING_FREQ) % DOWN_PRINT_INT) == 0):
                    downtimeMsg = str(int(i/DOWN_PING_FREQ)) + " .. offline"
                    print(downtimeMsg)
 
                i += 1
 
            else:
                # if connection is acquired
                first_check(host, port)
                print(monitoring_date_time)
                break
 
    with open(FILE, "a") as file:
        file.write("\n")
        file.write(monitoring_date_time + "\n")
 
    while True:
 
        # infinite loop, monitoring connection
        if ping(host, port):
 
            # if ping received, continue at defined interval
            time.sleep(60/UP_PING_FREQ)
 
        else:
            # if false: fail message
            down_time = datetime.datetime.now()
            fail_msg = host + " disconnected at: " + str(down_time).split(".")[0]
            print(fail_msg)
 
            with open(FILE, "a") as file:
                # writes into the log file
                file.write(fail_msg + "\n")
 
            while not ping(host, port):
 
                # infinite loop until ping returns
                time.sleep(1)
 
            up_time = datetime.datetime.now()
 
            # after loop breaks, connection restored
            uptime_message = host + " connected again: " + str(up_time).split(".")[0]
 
            down_time = calculate_time(down_time, up_time)
            unavailablity_time = "PLC connection was unavailable for: " + down_time
 
            print(uptime_message)
            print(unavailablity_time)
 
            with open(FILE, "a") as file:
 
                # log entry for restoration time and downtime
                file.write(uptime_message + "\n")
                file.write(unavailablity_time + "\n")
 
main()