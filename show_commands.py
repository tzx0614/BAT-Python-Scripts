#! python
""" Shows the available commands that can run self-made python scripts. """

import itertools
import logging
import os

logging.basicConfig(level=logging.DEBUG)

# Sets 'BASE_DIR' to be the current directory.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

counter = itertools.count(start=1)
is_bat_existing = False

print("Commands Available: ")
for item in os.listdir(BASE_DIR):
    item_path = os.path.join(BASE_DIR, item)

    # Conditions if it is a .bat file.
    is_file = os.path.isfile(item_path)
    is_bat_extension = item.endswith(".bat")
    is_bat_file = is_file and is_bat_extension

    has_underscore = "_" in item

    if is_bat_file and not has_underscore:
        is_bat_existing = True
        bat_file_name, bat_file_extension = os.path.splitext(item)
        print(f"{next(counter)}. {bat_file_name}")

if not is_bat_existing:
    print("None.")