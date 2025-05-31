from src.logger import logging

logging.debug("This is a debug message.")
logging.info("This is an info message.")
logging.warning("This is a warning message.")
logging.error("This is an error message.")
logging.critical("This is a critical message.")
#logging.exception("This is an exception message with traceback.", exc_info=True)


try:
    a=1+'z'
    print(a)
except Exception as e:
    logging.exception(f"An exception occurred:")