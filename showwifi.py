#! python3
# showwifi.py - shows wifi connected in computer

import subprocess

data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
for profileName in profiles:
    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profileName, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
        results = [password.split(":")[1][1:-1] for password in results if "Key Content" in password]
        try:
            print("{:<30}|  {:<}".format(profileName, results[0]))
        except IndexError:
            print("{:<30}|  {:<}".format(profileName, ""))
    except subprocess.CalledProcessError:
        print("{:<30}|  {:<}".format(profileName, "ENCODING ERROR"))
input("")
