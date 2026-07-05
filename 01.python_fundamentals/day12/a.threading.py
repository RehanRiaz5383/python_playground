import threading
import time

def print_numbers():
    for i in range(5):
        print(i)
        time.sleep(2)
        
        
def print_letters():
    for letter in ['A', 'B', 'C', 'D', 'E']:
        print(letter)
        time.sleep(2)
        
        
        

t = time.time()   
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

thread1.start()
thread2.start()

thread1.join()
thread2.join()



print("Time taken with threading: ", time.time() - t)
