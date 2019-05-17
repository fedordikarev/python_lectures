#!/usr/bin/env python3

import fileinput
import fire
import sh
import tqdm

def do_all(host="ceph01-ti.msk.inn.ru"):
    for disk in tqdm.tqdm(list(list_disks(host))):
        yield parse_smart_disk(host, disk)

def list_disks(host="ceph01-ti.msk.inn.ru"):
    out = sh.ssh(host, "ls -1 /dev/sd*")
    for disk in out.splitlines():
        if '0' <= disk[-1] <= '9':
            continue
        yield disk

def parse_smart_disk(host="ceph01-ti.msk.inn.ru", disk="/dev/sda"):
    try:
        out = sh.ssh(host, "sudo smartctl -i "+disk)
        return parse_smartctl(out)
    except:
        return {}

def parse_smartctl(data):
    result = dict()
    map_headers = { "Vendor": "Vendor",
                    "Product": "Model",
                    "Device Model": "Model",
                    "Serial Number": "Serial",
                    "Serial number": "Serial",
                    "User Capacity": "Size",
                    "Rotation Rate": "Rotation Rate" }
    headers = set(map_headers.keys())

    for line in data.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.lstrip()
        if key in headers:
            # print(key)
            result[map_headers[key]] = value.strip()

    if "Vendor" in result:
        result["Model"] = result.pop("Vendor") + " " + result["Model"]

    if "Size" in result:
        size = result["Size"]
        # match = re.search(r"\[([^\]]+)]", size)
        # if match:
            # result["Size"] = match.group(1)

        result["Size"] = size[size.find("[")+1:size.find("]")]

    return result

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
