import logging

logger = logging.getLogger('tcpserver')

print('running\n\n')

try:
    raise TypeError("Oups!")
except Exception:
    logger.error("Fatal error in my thing", exc_info=True)

print("\n\n...still alive tho")

