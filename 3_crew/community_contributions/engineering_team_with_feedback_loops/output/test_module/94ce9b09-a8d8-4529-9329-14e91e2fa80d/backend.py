import itertools
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def compute_permutations(n):
    """
    Computes permutations of numbers from 0 to n-1.

    Args:
        n (int): The upper limit for permutation, must be between 0 and 10.

    Returns:
        list: A list of permutations of numbers from 0 to n-1.
    """
    if not isinstance(n, int):
        logging.error("Input must be an integer.")
        return None
    
    if n < 0 or n > 10:
        logging.error("Input must be between 0 and 10.")
        return None

    numbers = list(range(n))
    permutations = list(itertools.permutations(numbers))
    logging.info(f"Computed permutations for n={n}: {permutations}")
    return permutations

def main():
    """
    Main function to prompt user input and display permutations.
    """
    try:
        user_input = input("Enter a number between 0 and 10 to compute permutations: ")
        n = int(user_input)
        result = compute_permutations(n)
        
        if result is not None:
            print(f"Permutations of numbers 0 to {n-1}: {result}")
        
    except ValueError:
        logging.error("Invalid input. Please enter a valid integer.")
        print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    main()