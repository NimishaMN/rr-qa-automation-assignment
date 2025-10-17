from loguru import logger as log
import sys

# Configure loguru once:
log.remove()
log.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO")
