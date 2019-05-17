#!/usr/bin/env python3

import fileinput
import fire
import sh

def do_all(host="ceph01-ti.msk.inn.ru"):
    for slot in parse_ctrl_list(host):
        print(parse_disk_list(host, slot))

def parse_ctrl_list(host="ceph01-ti.msk.inn.ru"):
    out = sh.ssh(host, "sudo hpssacli ctrl all show")
    result = dict()
    for line in out.splitlines():
        if " in Slot " not in line:
            continue
        (model, rest_line) = line.split(" in Slot ", 2)
        slot = rest_line.split()[0]
        result[slot] = model
        # print(slot, model)

    return result

def parse_disk_list(host="ceph01-ti.msk.inn.ru", slot=0):
    out = sh.ssh(host, "sudo hpssacli ctrl slot={} pd all show detail".format(slot))
    result = dict()
    pd = None
    fields = set(("Size", "Disk Name", "Model", "Serial Number"))
    for line in out.splitlines():
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
