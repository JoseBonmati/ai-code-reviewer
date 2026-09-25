import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def calculate_factorial(n: int) -> int:
    """
    Calculates the factorial of a non-negative integer.
    
    Args:
        n (int): The non-negative integer to calculate the factorial for.
        
    Returns:
        int: The factorial of n.
        
    Raises:
        ValueError: If n is a negative number.
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")
        
    if n < 0:
        logger.error("Attempted to calculate factorial of a negative number: %d", n)
        raise ValueError("Factorial is not defined for negative numbers.")
    
    if n in (0, 1):
        return 1
        
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result

if __name__ == "__main__":
    try:
        VALUE = 5
        logger.info("Factorial of %d is: %d", VALUE, calculate_factorial(VALUE))
    except (ValueError, TypeError) as error:
        logger.exception("An error occurred during calculation: %s", error)