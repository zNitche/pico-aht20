# Inspired by
# https://github.com/adafruit/Adafruit_CircuitPython_AHTx0/blob/main/adafruit_ahtx0.py
import time


class AHT20:
    def __init__(self, i2c, address=0x38):
        self.address = address
        self.i2c = i2c

        self.__reset()

        if self.is_initialized():
            self.__initialize()

    def is_device_accessible(self):
        return True if self.address in self.i2c.scan() else False

    def is_initialized(self):
        buff = self.i2c.readfrom(self.address, 1)
        return buff[0] != 0x18

    def __reset(self):
        self.i2c.writeto(self.address, bytearray([0xBA]))
        time.sleep_ms(100)

    def __initialize(self):
        self.i2c.writeto(self.address, bytearray([0xBE, 0x08, 0]))
        time.sleep_ms(100)

    def __parse_humidity(self, raw_data: bytearray) -> float:
        # merge bytes
        # register is 20 bits long, fill to 20, to 12, take first 4 bits
        humidity = ((raw_data[1] << 12) | (raw_data[2] << 4) | (raw_data[3] >> 4))
        humidity = humidity / 1048576 * 100

        return humidity

    def __parse_temperature(self, raw_data: bytearray) -> float:
        # merge bytes
        # register is 20 bits long, take last 4 bits then fill to 20, fill to 16, take last register
        temp = ((raw_data[3] & 0xF) << 16) | (raw_data[4] << 8) | raw_data[5]
        temp = ((temp / 1048576) * 200.0) - 50

        return temp

    def __read_raw_data(self) -> bytearray:
        self.i2c.writeto(self.address, bytearray([0xAC, 0x33, 0]))
        time.sleep_ms(100)

        return self.i2c.readfrom(self.address, 6)

    def get_readings(self) -> tuple[float, float]:
        raw_data = self.__read_raw_data()

        temperature = self.__parse_temperature(raw_data)
        humidity = self.__parse_humidity(raw_data)

        return temperature, humidity
