import logging
from dota2gsipy.server import GSIServer

logging.basicConfig(level=logging.INFO)

server = GSIServer(("192.168.1.1", 3030),"TOKENHERE")
server.start_server()