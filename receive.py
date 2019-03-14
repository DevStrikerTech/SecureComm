#!/usr/bin/env python3

import argparse
import signal
import sys
import time
import logging

from rpi_rf import RFDevice

rfdevice = None

# pylint: disable=unused-argument
def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)

parser = argparse.ArgumentParser(description='Receive a decimal code from the target device')
parser.add_argument('-g', dest='gpio', type=int, default=27,
                    help="GPIO pin (Default: 27)")
args = parser.parse_args()
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

signal.signal(signal.SIGINT, exithandler)
rfdevice = RFDevice(args.gpio)
rfdevice.enable_rx()
timestamp = None
logFile = open("log.txt", "w+")
logFile.write("CODE,PULSELENGTH,PROTOCOL\n")
if args.gpio:
    gpio = args.gpio
else:
    gpio = "default"
logging.info("Listening for codes on GPIO " + str(gpio))
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        logF = open("log.txt", "a")
        logging.info("CODE: " + str(rfdevice.rx_code) +
                     " [pulselength " + str(rfdevice.rx_pulselength) +
                     ", protocol " + str(rfdevice.rx_proto) + "]")
        logF.write(str(rfdevice.rx_code) +","+ str(rfdevice.rx_pulselength) +","+ str(rfdevice.rx_proto) +"\n")
    time.sleep(0.01)
rfdevice.cleanup()
logF.close()
