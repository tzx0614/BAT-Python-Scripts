#! python3
""" Creates '.bat' files for the '.py' files in the current directory. """
# In order to run the python script in the windows command prompt.

import logging
import os

logging.basicConfig(level=logging.DEBUG)

# Sets 'BASE_DIR' to be the current directory.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.info(f"Directory: {BASE_DIR}")

for item in os.listdir(BASE_DIR):
    item_path = os.path.join(BASE_DIR, item)

    # Conditions if the item is a '.py' file.
    is_file = os.path.isfile(item_path)
    py_extension = item.endswith(".py")
    is_python_file = is_file and py_extension

    # Condition if it's the file
    is_file_itself = item == "create_bat_files.py"

    if is_python_file and not is_file_itself:
        file_basename, file_extension = os.path.splitext(item)
        bat_file_name = f"{file_basename}.bat"
        logging.info(f"Creating {bat_file_name}")
        with open(bat_file_name, "w") as bat_file:
            bat_file.write(f"@py.exe \"{item_path}\" %*\n")
            bat_file.write("pause")
