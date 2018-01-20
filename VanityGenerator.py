"""
    Generates addresses matching your specific requirements
    Time taken largely dependent on the length of the string you want
    > python3 VanityGenerator.py -c Win
"""

from KeyPair import KeyPair
import argparse
import time
import logging

def generate_address(contains=None, caseSensitive=False):
    logging.basicConfig(filename='finds.log', level=logging.DEBUG)
    logging.info("Starting search now")

    count = 0
    start = time.time()

    if not caseSensitive:
        contains = None if contains == None else contains.lower()

    while True:
        KP = KeyPair()

        addr = KP.GetAddress()
        count += 1

        new_addr = addr

        if not caseSensitive:
            new_addr = addr.lower()

        if count % 10000 == 0:
            print("C: {} T: {}".format(count, time.time()-start))

        if contains and contains not in addr:
            continue

        print("{},{}".format(addr, KP.WIF))
        logging.debug("{},{}".format(addr, KP.WIF))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("substring", type=str,
                        help="finds addresses that contain your desired substring")
    parser.add_argument("-c", "--case", default=0, action='count',
                        help="case sensitivity. Default is false")
    args = parser.parse_args()

    generate_address(contains=args.substring, caseSensitive=(args.case!=0))
