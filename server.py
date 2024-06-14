import socket
import time
import logging

logger = logging.getLogger("server_log")
logger.setLevel(logging.DEBUG)

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s]: - %(message)s")
sh.setFormatter(formatter)
logger.addHandler(sh)

host = socket.gethostbyname(socket.gethostname())
port = 7777

print(host)

clients = list()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

running = True
time.sleep(1)
logger.info("Server started")
flag = False

while running:
    try:
        data, addr = s.recvfrom(1024)
        if addr not in clients:
            clients.append(addr)

        info = f"{addr[0]}:{addr[1]} | "
        logger.info(f"{info}{data.decode("utf-8")}")

        for client in clients:
            if client != addr:
                s.sendto(data, client)
        flag = False

    except Exception as exc:
        if not flag:
            logger.error(exc)
        else:
            logger.critical(exc)
            logger.info("Server stopped due to critical error")
            running = False
        flag = True

s.close()
