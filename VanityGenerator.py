from KeyPair import KeyPair
import time

def generate_address(contains=None, startsWith=None, endsWith=None, caseSensitive=True):
    count = 0
    start = time.time()

    if not caseSensitive:
        contains = None if contains == None else contains.lower()
        startsWith = None if startsWith == None else startsWith.lower()
        endsWith = None if endsWith == None else endsWith.lower()

    while True:
        KP = KeyPair()

        addr = KP.GetAddress()
        count += 1

        new_addr = addr

        if not caseSensitive:
            new_addr = addr.lower()

        if count % 1000 == 0:
            print("C: {} T: {}".format(count, time.time()-start))

        if contains and contains not in addr:
            continue

        if startsWith and addr[0:len(startsWith)] != startsWith:
            continue

        if endsWith and addr[-len(endsWith):] != endsWith:
            continue

        print("{},{}".format(addr, KP.Export()))

generate_address(contains="Wing", caseSensitive=False)
