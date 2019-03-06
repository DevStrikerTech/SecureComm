#!/usr/bin/env python3

import argparse
import logging

from rpi_rf import RFDevice

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s',)

parser.add_argument('-g', dest='gpio', type=int, default=27,
                    help="GPIO pin (Default: 17)")
parser.add_argument('-p', dest'protocol', type=, default=, help="Protocol. Default:")
parser.add_argument('-t', dest'pulselength', type=, default=, help="Pulse length")

rfdevice = RFDevice(args.gpio)
rfdevice.enable_tx()


if args.protocol:
    protocol = args.protocol
else:
    protocol = "default"
if args.pulselength:
    pulselength = args.pulselength
else:
    pulselength = "default"
logging.info(str(args.code) +
             " [protocol: " + str(protocol) +
             ", pulselength: " + str(pulselength) + "]")

rfdevice.tx_code(args.code, args.protocol, args.pulselength)
rfdevice.cleanup()
