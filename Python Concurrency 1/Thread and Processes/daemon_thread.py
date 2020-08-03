import threading
import time

def kitchen_cleaner():
    while True:
        print("Bob cleaned the kicthen")
        time.sleep(1)

if __name__ == '__main__':
    bob = threading.Thread(target=kitchen_cleaner)
    bob.daemon = True
    bob.start()

    print("sid is cooking")
    time.sleep(0.5)
    print("sid is cooking")
    time.sleep(0.5)
    print("sid is cooking")
    time.sleep(0.5)
    print("Sid done")
