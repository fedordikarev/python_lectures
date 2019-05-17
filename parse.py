#!/usr/bin/env python3

import fileinput
import fire

def parse_ctrl_list():
    for line in fileinput.input("-"):
        if " in Slot " not in line:
            continue
        (model, rest_line) = line.split(" in Slot ", 2)
        slot = rest_line.split()[0]
        print(slot, model)

def parse_disk_list():
    for line in fileinput.input("-"):
        if "physicaldrive" in line:
            (_, location) = line.split()
            print(location)
    pass

def main():
    # parse_ctrl_list()
    # parse_disk_list()
    fire.Fire()

if __name__ == "__main__":
    main()
