#!/usr/bin/env python3
import csv
import argparse
import logging
import time

from rpi_rf import RFDevice

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s',)

parser = argparse.ArgumentParser(description='Sends a decimal code to the target device')

parser.add_argument('-g', dest='gpio', type=int, default=17,
                    help="GPIO pin (Default: 17)")
parser.add_argument('-p', dest='protocol', type=int, default=1, help="Protocol. Default: 1")
parser.add_argument('-t', dest='pulselength', type=int, default=350, help="Pulse length, Default: 350")
parser.add_argument('-c', dest='code', type=int, default=0, help="Decimal code to send") 
parser.add_argument('-f', dest='logFile', type=str, help="File from program sends the codes")
args = parser.parse_args()


def sendSignal(code, protocol, pulselength):
    rfdevice = RFDevice(args.gpio)
    rfdevice.enable_tx()
    logging.info(str(code) +
                 " [protocol: " + str(protocol) +
                 ", pulselength: " + str(pulselength) + "]")

    rfdevice.tx_code(int(code), int(protocol), int(pulselength))
    rfdevice.cleanup()
    time.sleep(1)

if args.protocol:
    protocol = args.protocol
else:
    protocol = "default"
if args.pulselength:
    pulselength = args.pulselength
else:
    pulselength = "default"
if args.logFile:
    logFile = args.logFile
    with open(logFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            code = row[0]
            pulselength = row[1]
            protocol = row[2]
            if line_count == 0:
                if code == "CODE" and pulselength == "PULSELENGTH" and protocol == "PROTOCOL":
                    line_count += 1
                else:
                    print("Wrong file type.")
            if line_count >= 0 and row[0] != "CODE":
                sendSignal(code, protocol, pulselength)
                line_count += 1
else:
    sendSignal(args.code, args.protocol, args.pulselength)
        

