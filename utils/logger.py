import logging
import sys

def configure_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


if __name__ == "__main__":
    logger = configure_logger("test_logger")
    
    logger.debug("Mensagem de DEBUG")
    logger.info("Mensagem de INFO")
    logger.warning("Mensagem de WARNING")
    logger.error("Mensagem de ERROR")
    logger.critical("Mensagem de CRITICAL")

