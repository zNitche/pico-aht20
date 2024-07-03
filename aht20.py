# Inspired by
# https://github.com/adafruit/Adafruit_CircuitPython_AHTx0/blob/main/adafruit_ahtx0.py
import time


class AHT20:
    def __init__(self, i2c, address=0x38):
        self.address = address
        self.i2c = i2c

        self.reset()
        self.__calibrate()

    def is_device_accessible(self):
        return True if self.address in self.i2c.scan() else False

    def reset(self):
        self.i2c.writeto(self.address, bytearray([0xBA]))
        time.sleep_ms(50)

    def __calibrate(self):
        self.i2c.writeto(self.address, bytearray([0xBE, 0x08, 0]))
        time.sleep_ms(50)

    def __parse_humidity(self, raw_values: bytearray) -> float:
        humidity = ((raw_values[1] << 12) | (raw_values[2] << 4) | (raw_values[3] >> 4))
        humidity = (humidity * 100) / 0x100000

        return humidity

    def __parse_temperature(self, raw_values: bytearray) -> float:
        temp = ((raw_values[3] & 0xF) << 16) | (raw_values[4] << 8) | raw_values[5]
        temp = ((temp * 200.0) / 0x100000) - 50

        return temp

    def __read_raw_data(self) -> bytearray:
        self.i2c.writeto(self.address, bytearray([0xAC, 0x33, 0]))
        time.sleep_ms(50)

        return self.i2c.readfrom(self.address, 6)

    def get_readings(self) -> tuple[float, float]:
        raw_data = self.__read_raw_data()

        temperature = self.__parse_temperature(raw_data)
        humidity = self.__parse_humidity(raw_data)

        return temperature, humidity
