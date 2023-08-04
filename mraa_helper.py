import mraa
import sys
from time import sleep

class MRAA_Helper():

    #Static Variable Definitions for MRAA
    OUTPUT = mraa.DIR_OUT
    INPUT = mraa.DIR_IN

    HIGH = 1
    LOW = 0


    def __init__(self):
        self.pin = -1


    def mraa_init(self,pin_num,pin_dir):
        try:
            self.mraa_pin = mraa.Gpio(pin_num)
            self.mraa_pin.dir(pin_dir)
        except:
            print("Error While initializing pin")

    def read_pin(self):
        try:
            return self.mraa_pin.read()
        except:
            print("Error while reading pin")


    def write_pin(self,value):
        try:
            self.mraa_pin.write(value)

        except:
            print("Error writing value to pin")

    def close_pin(self):
        self.mraa_pin.close()

    def uart_init(self,port,baud_rate=9600,data_bits=8,stop_bit=1,parity_bit=mraa.UART_PARITY_NONE):

        try:
            # serial port
            self.port = port
            # initialise UART
            self.uart = mraa.Uart(port)
            self.uart.setBaudRate(baud_rate)
            self.uart.setMode(data_bits, parity_bit, stop_bit)
            self.uart.setFlowcontrol(False, False)

            return self.uart
        except:
            print("Error opening port for UART communication")


    def data_available(self):
        try:
            return self.uart.dataAvailable()
        except:
            print("Error in UART")

    def read_uart_data(self,data_length=1):
        try:
            return self.uart.readStr(data_length)

        except:
            print("Error reading the data from UART")

    def write_uart_data(self,data):
        try:
            # send data through UART
            self.uart.write(bytearray(data, 'utf-8'))

        except:
            print("Error writing to UART")


    def spi_init(self):
        pass

    def read_spi_data(self):
        pass

    def write_spi_data(self):
        pass

    def i2c_init(self,twi = 0,address=0x00):
        try:
            self.i2c = mraa.I2c(twi)
            if address:
                self.i2c.address(address)
            return self.i2c
        except Exception:
            raise Exception

    def read_i2c_data(self,address):
        try:
            return self.i2c.readReg(address)
        except Exception:
            raise Exception

    def write_i2c_data(self,address,data_byte):
        try:
            self.i2c.writeReg(address,data_byte)
        except Exception:
            raise Exception

    def aio_init(self):
        pass

    def read_analog_data(self):
        pass

    def pwm_init(self):
        pass

    def pwm_write(self):
        pass


    def delay(millis):
        sleep(millis/1000.0)

    def usleep(micros):
        delay(micros/1000.0)










