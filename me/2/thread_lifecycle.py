import time
import threading

class ChefSid(threading.Thread):
    def init(self):
        super().__init__()

    def run(self):
      print("Sid has started and is waiting for the sauage to thaw")
      time.sleep(3)
      print("Sid is done cutting the sauage")


if __name__ == '__main__':
    print("Bob has started and is requesting for Sid's help")
    sid = ChefSid()
    print('  sid alive?:', sid.is_alive())

    print("Bob tells sid to start")
    sid.start()
    print('  sid alive?:', sid.is_alive())

    print('Bob continues cooking soup.')
    time.sleep(0.5)
    print('  sid alive?:', sid.is_alive())

    print('Bob patiently waits for sid to finish and join...')
    sid.join()
    print('  sid alive?:', sid.is_alive())

    print('Bob and Sid are both done!')