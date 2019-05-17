#!/usr/bin/env python3

import fileinput
import fire
import sh

def do_all(host="ceph01-ti.msk.inn.ru"):
    for disk in list_disks(host):
        print(parse_hdparm(host, disk))

def list_disks(host="ceph01-ti.msk.inn.ru"):
    out = sh.ssh(host, "ls -1 /dev/sd*")
    for disk in out.splitlines():
        if '0' <= disk[-1] <= '9':
            continue
        yield disk

def parse_hdparm(host="ceph01-ti.msk.inn.ru", diskname="/dev/sda"):
    out = sh.ssh(host, "sudo hdparm -I "+diskname)
    result = dict()
    result[diskname] = dict()
    pd = None
    fields = set(("Model Number", "Serial Number", "device size with M = 1000*1000"))
    rename_keys = {"device size with M = 1000*1000": "Size"}

    for line in out.splitlines():
        line = line.strip()
        if ": " in line:
            (key, value) = line.split(": ")
            if key not in fields:
                continue
            result[diskname][rename_keys.get(key, key)] = value.strip()
            # print(">", key, "<>", value, "<")

    return result

def main():
    # parse_ctrl_list()
    # parse_disk_list()
    fire.Fire()

if __name__ == "__main__":
    main()
