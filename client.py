import time
import socket
import threading
import logging
import sys

key = 3

shutdown = False
join = False

logger = logging.getLogger("client_log")
logger.setLevel(logging.DEBUG)

sh = logging.FileHandler("logs/client.log")
sh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s]: - %(message)s")
sh.setFormatter(formatter)
logger.addHandler(sh)

host = "0.0.0.0"
port = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(True)
s.settimeout(0.2)

server_host = ("192.168.1.67", 7777)


def receive(name, sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)

            # # Decrypting message
            # decrypted_message = ""
            # now_decrypting = False
            #
            # for sym in data.decode("utf-8"):
            #     if sym == ":":
            #         now_decrypting = True
            #     elif not now_decrypting or sym == " ":
            #         decrypted_message += sym
            #     else:
            #         decrypted_message += chr(ord(sym)*key)
            # print(decrypted_message)

            print(data.decode("utf-8"))

            time.sleep(0.2)
        except KeyboardInterrupt:
            s.sendto(f"{username} left chat. Goodbye!".encode("utf-8"), server_host)
            receiveing_thread.join()
            s.close()
            sys.exit()
        except socket.timeout:
            pass
        except Exception as exc:
            logger.error(exc)
            break


username = input("Your name: ")

receiveing_thread = threading.Thread(target=receive, args=("RecvThread", s))
receiveing_thread.start()

while not shutdown:
    try:
        if not join:
            s.sendto(f"{username} joined chat. Hello!".encode("utf-8"), server_host)
            join = True
        else:
            message = input()

            if message.lower() in ["q", "quit"]:
                s.sendto(f"{username} left chat. Goodbye!".encode("utf-8"), server_host)
                shutdown = True
                s.close()
                receiveing_thread.join()
                sys.exit()

            # # Encrypting message
            # encrypted_message = ""
            # for sym in message:
            #     encrypted_message += chr(ord(sym)*key)
            # message = encrypted_message

            s.sendto(f"{username}: {message}".encode("utf-8"), server_host)

            time.sleep(0.3)

    except KeyboardInterrupt:
        s.sendto(f"{username} left chat. Goodbye!".encode("utf-8"), server_host)
        shutdown = True
        s.close()
        receiveing_thread.join()
        sys.exit()
    except socket.timeout:
        pass
    except Exception as exc:
        s.sendto(f"{username} left chat. Goodbye!".encode("utf-8"), server_host)
        shutdown = True
        logger.critical(exc)
        s.close()
        receiveing_thread.join()
        sys.exit()
