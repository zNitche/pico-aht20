import machine
import aht20


def main():
    i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
    sensor = aht20.AHT20(i2c)

    if sensor.is_device_accessible():
        print(sensor.get_temperature())
        print(sensor.get_relative_humidity())


if __name__ == '__main__':
    main()
