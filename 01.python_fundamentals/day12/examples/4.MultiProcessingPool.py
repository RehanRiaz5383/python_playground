import math
import sys
import time
import multiprocessing


sys.set_int_max_str_digits(1000000)


def calculate_factorial(n):
    return math.factorial(n)

#with multithreading it took 0.03 seconds
#with process pool executor it took 0.12 seconds
#with multiprocessing.pool it took 0.5 seconds
#took 0.57 seconds directly without multiprocessing
numbers = [50000, 10000, 20000, 80000, 40000]

if __name__ == "__main__":
    t = time.time()
    with multiprocessing.Pool(processes=5) as pool:
        results = pool.map(calculate_factorial, numbers)
    for number, result in zip(numbers, results):
        print(f"Factorial of {number} has {len(str(result))} digits.")
    print(f"Total time taken: {time.time() - t:.2f} seconds")