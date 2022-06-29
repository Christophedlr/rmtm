#!/usr/bin/env python3
import getpass
import os.path

import config
import json

from os.path import exists as file_exists
from rmtm import Rmtm

templates: list = []
filenames: list = []


def choose_file(manager: Rmtm):
    template: dict = {}
    file = input("Template file no extension): ")

    if file_exists(file + ".png") and file_exists(file + ".svg"):
        name = input("Name: ")

        templates.append(manager.add_entry(name, os.path.basename(file), ["Life/organize"]))
        filenames.append(file)
        choose_file(manager)
    elif file == "":
        return
    else:
        print("File not found")
        choose_file()


manager = Rmtm()
print("ReMarkable Template Manager V" + config.VERSION_STRING)
print()
choose_file(manager)
print()

hostname = input("ReMarkable Hostname: ")
password = getpass.getpass("ReMarkable root password: ")
template_json = input("Location to writing templates.json: ")

print("Connecting to ReMarkable...")
manager.open(hostname, "root", password)

print("Downloading templates.json")
manager.get_file("/usr/share/remarkable/templates/templates.json", template_json+"/templates.json")

print("Parsing templates.json")

with open(template_json+"/templates.json", "r") as f:
    data = json.load(f)
f.close()

for template in templates:
    data["templates"].append(template)

with open(template_json+"/templates.json", "w") as f:
    json.dump(data, f, indent=2)
f.close()

for filename in filenames:
    print("Uploading " + filename)
    manager.put_file(filename+".png", "/usr/share/remarkable/templates/" + os.path.basename(filename)+".png")
    manager.put_file(filename+".svg", "/usr/share/remarkable/templates/" + os.path.basename(filename)+".svg")

print("Uploading templates.json")
manager.put_file(template_json+"/templates.json", "/usr/share/remarkable/templates/templates.json")

print("Rebooting ReMarkable")
manager.reboot_command()
