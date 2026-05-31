import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("nyaya_ai")


def log_info(module: str, message: str) -> None:
    logger.info(f"[{module}] {message}")


def log_error(module: str, message: str, error: str = "") -> None:
    logger.error(f"[{module}] {message}: {error}")


def log_warning(module: str, message: str) -> None:
    logger.warning(f"[{module}] {message}")