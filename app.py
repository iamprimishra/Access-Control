
from threading import Thread


from request_handler import run_server_process
from rfid_handler import RFID_Handler,run_rfid_process

if __name__ == "__main__":


    t1 = Thread(target = run_server_process)
    t2 = Thread(target = run_rfid_process)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()

    while(True):
        pass

