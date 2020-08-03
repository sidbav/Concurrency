import os
import threading
import time

chopping = True

def veg_chopper():
    name = threading.current_thread().getName()
    veg_count = 0
    while chopping:
        print(name, 'chopped a veg')
        veg_count += 1
    print(name, 'chopped', veg_count, 'vegs')

if __name__ == '__main__':
    threading.Thread(target=veg_chopper, name="Sid").start()
    threading.Thread(target=veg_chopper, name="Bob").start()

    time.sleep(1)
    chopping = False

