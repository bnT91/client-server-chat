import socket
import logging
import sys
import time

logger = logging.getLogger("server_log")
logger.setLevel(logging.DEBUG)

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s]: - %(message)s")
sh.setFormatter(formatter)
logger.addHandler(sh)

host = socket.gethostbyname(socket.gethostname())
port = 7777

# print(host)

clients = list()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.settimeout(1)

running = True
logger.info("Server started")

while True:
    try:
        data, addr = s.recvfrom(1024)
        if addr not in clients:
            clients.append(addr)

        info = f"{addr[0]}:{addr[1]} | "
        logger.info(f"{info}{data.decode("utf-8")}")

        for client in clients:
            if client != addr:
                s.sendto(data, client)

        time.sleep(0.2)
    except KeyboardInterrupt:
        s.close()
        sys.exit()
    except TimeoutError:
        pass
    except Exception as exc:
        logger.critical(exc)
        logger.info("Server stopped due to critical error")
        running = False

