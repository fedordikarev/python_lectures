#!/usr/bin/env python3

import fileinput

def parse_ctrl_list():
    for line in fileinput.input():
        if " in Slot " not in line:
            continue
        (model, rest_line) = line.split(" in Slot ", 2)
        slot = rest_line.split()[0]
        print(slot, model)

def main():
    parse_ctrl_list()

if __name__ == "__main__":
    main()
