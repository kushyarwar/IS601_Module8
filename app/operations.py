import logging

logger = logging.getLogger(__name__)


def add(a: float, b: float) -> float:
    result = a + b
    logger.info("add(%.4g, %.4g) = %.4g", a, b, result)
    return result


def subtract(a: float, b: float) -> float:
    result = a - b
    logger.info("subtract(%.4g, %.4g) = %.4g", a, b, result)
    return result


def multiply(a: float, b: float) -> float:
    result = a * b
    logger.info("multiply(%.4g, %.4g) = %.4g", a, b, result)
    return result


def divide(a: float, b: float) -> float:
    if b == 0:
        logger.error("divide(%.4g, %.4g) failed: division by zero", a, b)
        raise ValueError("Cannot divide by zero")
    result = a / b
    logger.info("divide(%.4g, %.4g) = %.4g", a, b, result)
    return result
