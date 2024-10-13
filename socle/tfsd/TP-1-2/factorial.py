def factorial(n):
    """
    Function to calculate the factorial of a number
    """
    # Great now that this works, let's see what the program does when it faces a negative value (forbidden)
    # It also crashes
    # Let's fix this using copilot
    # TODO: throw an error when we have a negative value
    if n < 0:
        raise ValueError('Negative values are not allowed')
    if n == 0:
        return 1
    fact =  n * factorial (n - 1)
    return fact

    # It finally works!

if __name__ == "__main__":
    number = int(input("Enter a number: "))
    result = factorial(number)
    print(f"The factorial of {number} is {result}")