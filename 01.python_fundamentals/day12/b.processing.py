import multiprocessing
import time

def print_numbers():
    for i in range(5):
        print(i)
        time.sleep(2)
    
def print_letters():
    for letter in ['A', 'B', 'C', 'D', 'E']:
        print(letter)
        time.sleep(2)


if __name__ == "__main__":
    t = time.time()   
    process1 = multiprocessing.Process(target=print_numbers)
    process2 = multiprocessing.Process(target=print_letters)

    process1.start()
    process2.start()

    process1.join()
    process2.join()

    print("Time taken with multiprocessing: ", time.time() - t)