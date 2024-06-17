import socket
import logging
import sys
import time

logger = logging.getLogger("server_log")
logger.setLevel(logging.DEBUG)

sh = logging.FileHandler("logs/server.log")
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

logger.info("Server started")

while True:
    try:
        data, addr = s.recvfrom(1024)
        if addr not in clients:
            clients.append(addr)

        if data.decode("utf-8")[-2] == "e" and ":" not in data.decode("utf-8"):
            clients.remove(addr)

        info = f"{addr[0]}-{addr[1]} | "
        print(f"{info}{data.decode("utf-8")}")

        for client in clients:
            if client != addr:
                s.sendto(data, client)

        time.sleep(0.2)
    except KeyboardInterrupt:
        s.close()
        sys.exit()
    except socket.timeout:
        pass
    except Exception as exc:
        logger.critical(exc)
        logger.info("Server stopped due to critical error")
        break

s.close()
