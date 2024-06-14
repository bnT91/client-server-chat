import time
import socket
import threading
import logging

key = 8194

shutdown = False
join = False

logger = logging.getLogger("client_log")
logger.setLevel(logging.DEBUG)

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s]: - %(message)s")
sh.setFormatter(formatter)
logger.addHandler(sh)


def receive(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)

            # Decrypting message
            decrypted_message = ""
            now_decrypting = False

            for sym in data.decode("utf-8"):
                if sym == ":":
                    now_decrypting = True
                elif not now_decrypting or sym == " ":
                    decrypted_message += sym
                else:
                    decrypted_message += chr(ord(sym)*key)
            print(decrypted_message)

            time.sleep(0.3)

        except Exception as exc:
            logger.error(exc)


host = socket.gethostbyname(socket.gethostname())
port = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

server_host = ("192.168.1.67", 7777)

username = input("Your name: ")

receiveing_thread = threading.Thread(target=receive, args=s)
receiveing_thread.start()

while not shutdown:
    if not join:
        s.sendto(f"{username} joined chat. Hello!".encode("utf-8"), server_host)
        join = True
    else:
        message = input()

        # Encrypting message
        encrypted_message = ""
        for sym in message:
            encrypted_message += chr(ord(sym)*key)
        message = encrypted_message

        if message:
            s.sendto(f"{username}: {message}", server_host)

        time.sleep(0.3)

        try:
            pass
        except Exception as exc:
            logger.critical(exc)

receiveing_thread.join()
