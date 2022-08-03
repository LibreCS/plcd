#from ctypes import sizeof
#from lib2to3.pygram import python_grammar_no_print_statement
import os
import re
#import sys
import socket
import datetime
import time

__version__ = "0.1.6"

# =========== CONFIGURATION ===========================================
# set monitoring frequency (pings/min)
UP_PING_FREQ = 5
# set monitoring frequency when down (pings/min)
DOWN_PING_FREQ = 3
# print downtime interval (min)
DOWN_PRINT_INT = 20
# number of lines in 'plc-ports.dat'
PLC_PORT_DEFINITIONS = 50
# maxium acceptable port for input and sniffing
PORT_SCAN_MAX = 50000
# CI testing host IP
TEST_IP = "185.199.109.153"
# =====================================================================
# initial array definitions
portName = [str("")]*PLC_PORT_DEFINITIONS
portNum = [int(0)]*PLC_PORT_DEFINITIONS

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

    addressInMsg = "\nEnter PLC plant IP address: "
    hostUsrIn = input(addressInMsg)
    # get user input for host address
    while True:
        try:
            if hostValid(hostUsrIn):
                break
        except EOFError:
            hostUsrIn = TEST_IP
            break
        
    if hostValid(hostUsrIn):
        print(bcolors.ORANGE + "\nScanning...\n" + bcolors.ENDC)
        portIndex = portSniff(hostUsrIn, portNum)
        if portIndex != "error:sniff":
            print("\nController type " + bcolors.BOLD +
                str(portName[portIndex]) + bcolors.ENDC + " found on TCP port " + str(portNum[portIndex]) + "Connecting...")
            return str(hostUsrIn) + ":" + str(portNum[portIndex])

    portError = bcolors.RED + "Error: No open ports found on host. Wait for response (w), or enter a new host (n)? " + bcolors.ENDC
    retry_response = input(portError)
    if retry_response.casefold() == "w".casefold():
        print(bcolors.ORANGE + "\nWaiting for host...\n" + bcolors.ENDC)
        while True:
            portIndex = portSniff(hostUsrIn, portNum)
            if portIndex != "error:sniff": break

        print("\nController type " + bcolors.BOLD + str(portName[portIndex]) + bcolors.ENDC + " found on TCP port " + str(portNum[portIndex]) + "Connecting...")
        return str(hostUsrIn) + ":" + str(portNum[portIndex])
    return "error"


def hostValid(hostUsrIn):
    # parse IP address for each quartet
    hostParse = hostUsrIn.split(".")

    # check for 4 quartet length
    if len(hostParse) == 4:

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
    if int(port) > 0 & int(port) < PORT_SCAN_MAX:
        return True
    else:
        return False


def ping(host, port):
    # to ping a particular IP
    try:
        socket.setdefaulttimeout(0.1)

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


def portSniff(inputAddress, portNum):
    # status variable definitions
    sniffStatus = [False]*PLC_PORT_DEFINITIONS

    # sniffing all given ports
    for portIndex in range(0, PLC_PORT_DEFINITIONS):
        if ping(str(inputAddress), int(portNum[portIndex])):
            sniffStatus[portIndex] = True
            return portIndex
        else:
            time.sleep(0.01)

    return "error:sniff"


def calculate_time(start, stop):
    difference = stop - start
    seconds = float(str(difference.total_seconds()))
    return str(datetime.timedelta(seconds=seconds)).split(".")[0]


def portIngest():
    # define ingest list of strings
    line = [str("")]*PLC_PORT_DEFINITIONS
    # opening PLC ports static datafile
    fileDir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(fileDir, 'plc-ports.dat')) as f:
        # iterate over the lines of definitions
        for i in range(0, PLC_PORT_DEFINITIONS):
            # read line to ingest list
            line[i] = f.readline()
            # split line to name and number
            portName[i], portNum[i] = line[i].split(":", 1)
        f.close()


def first_check(host, port):

    if ping(host, port):
        # if ping returns true
        live = "\nPLC connection acquired ... Monitoring...\n"
        print(live)
        connection_acquired_time = datetime.datetime.now()
        acquiring_message = "Connection acquired for " + host + " at: " + \
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
    print(bcolors.HEADER + "           __         __\n    ____  / /________/ /\n   / __ \/ / ___/ __  / \n  / /_/ / / /__/ /_/ /  \n / .___/_/\___/\__,_/   \n/_/                     \n" + bcolors.ENDC)
    # title & print
    welcomeMsg = bcolors.HEADER + bcolors.BOLD + \
        "Developed by LibreCS, licensed under GNU GPLv3. Learn more and contribute at https://github.com/LibreCS/plcd" + bcolors.ENDC
    print(welcomeMsg + "\n\n")

    # ingest 'plc-ports'.dat
    portIngest()

    # monitoring configuration & loop
    netLocationPLC = configure()
    while netLocationPLC == "error":
        netLocationPLC = configure()

    # parsing configuration output for host and port
    hostParse, portParse = netLocationPLC.split(":", 1)
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

                time.sleep(60 / DOWN_PING_FREQ)

                if (((i / DOWN_PING_FREQ) % DOWN_PRINT_INT) == 0):
                    downtimeMsg = str(int(i / DOWN_PING_FREQ)) + " .. offline"
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
            time.sleep(60 / UP_PING_FREQ)

        else:
            # if false: fail message
            down_time = datetime.datetime.now()
            fail_msg = host + " disconnected at: " + \
                str(down_time).split(".")[0]
            print(fail_msg)

            with open(FILE, "a") as file:
                # writes into the log file
                file.write(fail_msg + "\n")

            while not ping(host, port):

                # infinite loop until ping returns
                time.sleep(1)

            up_time = datetime.datetime.now()

            # after loop breaks, connection restored
            uptime_message = host + " connected again: " + \
                str(up_time).split(".")[0]

            down_time = calculate_time(down_time, up_time)
            unavailablity_time = "PLC connection was unavailable for: " + down_time

            print(uptime_message)
            print(unavailablity_time)

            with open(FILE, "a") as file:

                # log entry for restoration time and downtime
                file.write(uptime_message + "\n")
                file.write(unavailablity_time + "\n")


main()
