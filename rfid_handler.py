import json
from mraa_helper import MRAA_Helper
from rtc_handler import RTC_Handler
from threading import Thread
from db_handler import DB_Handler


class RFID_Handler:

    ACCESS = "access"
    READ = "read"
    # MODE = READ

    def __init__(self, uart):
        with open('mode.txt', 'r') as f:
            self.mode = f.read().strip()
        self.uart = uart
        self.uart.mraa_init(61, MRAA_Helper.OUTPUT)
        self.uart.write_pin(MRAA_Helper.HIGH)
        self.rtc = RTC_Handler(1, 0x68)

    def change_mode(self, mode=ACCESS):
        print("Mode changed to {}".format(mode))
        if mode != self.mode:
            self.mode = mode

    def get_mode(self):
        with open('mode.txt', 'r') as f:
            self.mode = f.read().strip()
            return self.mode

    def read_access_keys(self, path="data.json"):
        try:
            with open(path, 'r') as f:
                self.data = json.load(f)
                self.access_keys = self.data["data"]["access-keys"]
                for key in self.access_keys:
                    print(DB_Handler().get_last_access_time(key))
                return self.access_keys
        except Exception:
            raise Exception

    def add_access_keys(self, key, path="data.json"):
        try:
            with open(path, 'w+') as f:
                self.data["data"]["access-keys"].append(key)
                self.access_keys = self.data["data"]["access-keys"]
                print(json.dumps(self.data))
                f.write(json.dumps(self.data, sort_keys=True, indent=4))
                f.close()
                return self.access_keys
        except Exception:
            raise Exception

    def run_access_procedure(self, access_key):
        self.log_info(access_key, "Access Granted")

        t = Thread(target=self.run_on_off_procedure)
        t.setDaemon(True)
        t.start()

    def run_on_off_procedure(self):
        self.uart.write_pin(MRAA_Helper.HIGH)
        self.uart.write_pin(MRAA_Helper.LOW)
        MRAA_Helper.delay(5000)
        self.uart.write_pin(MRAA_Helper.HIGH)

    def log_info(self, access_key, access_control):
        # print(self.rtc.read_datetime())
        with open('log.txt', "a") as f:
            # print(self.rtc.read_datetime())
            f.write("{} - {} ({})\n".format(self.rtc.read_datetime(),
                    access_key, access_control))


def run_rfid_process():

    try:
        mraa_uart = MRAA_Helper()
        rfid = RFID_Handler(mraa_uart)
        access_keys = rfid.read_access_keys("data.json")
        mraa_uart.uart_init("/dev/ttyS3")
        print(mraa_uart)
        data = []

        while (True):

            while mraa_uart.data_available():
                data.append(mraa_uart.read_uart_data())

            if len(data) > 0:

                rfid_uid = "".join(data)

                if rfid.get_mode() == RFID_Handler.ACCESS:

                    if rfid_uid in access_keys:
                        print("Access Granted")
                        rfid.run_access_procedure(rfid_uid)
                    else:
                        rfid.log_info(rfid_uid, "Access Denied")
                        print("Access Denied")

                elif rfid.get_mode() == RFID_Handler.READ:
                    print(rfid_uid)
                    if rfid_uid not in access_keys:
                        rfid.add_access_keys(rfid_uid)

                data = []

    except:
        raise Exception
