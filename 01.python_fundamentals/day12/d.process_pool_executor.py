from concurrent.futures import ProcessPoolExecutor
import time


def square(number):
    time.sleep(2)
    return f"The square of {number} is {number * number}"
    
    
    
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5,6,7,8,9,10,12,13,15,18,20,21]
    
    t = time.time()
    
    with ProcessPoolExecutor(max_workers=10) as executor:
        results = executor.map(square, numbers)
        for result in results:
            print(result)
        
    print("Time taken with ProcessPoolExecutor: ", time.time() - t)