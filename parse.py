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
    result = dict()
    pd = None
    fields = set(("Size", "Disk Name", "Model", "Serial Number"))
    for line in fileinput.input("-"):
        line = line.strip()
        if "physicaldrive" in line:
            (_, pd) = line.split()
            result[pd] = dict()
            continue
        if ":" in line:
            (key, value) = line.split(": ")
            if key not in fields:
                continue
            result[pd][key] = value
            # print(">", key, "<>", value, "<")

    result_by_name = dict()
    for (location, data) in result.items():
        print(data)
        name = data['Disk Name']
        data["Location"] = location
        data.pop('Disk Name')
        result_by_name[name] = data

    return result_by_name

def main():
    # parse_ctrl_list()
    # parse_disk_list()
    fire.Fire()

if __name__ == "__main__":
    main()
