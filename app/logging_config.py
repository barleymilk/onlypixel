import logging
import sys

mylogger = logging.getLogger("mylogger")

formatter = logging.Formatter('[%(levelname)s] %(message)s')

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

mylogger.addHandler(handler)
mylogger.setLevel(logging.DEBUG)