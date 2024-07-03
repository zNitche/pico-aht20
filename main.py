import machine
import aht20


def main():
    i2c = machine.I2C(1, sda=machine.Pin(2), scl=machine.Pin(3))
    sensor = aht20.AHT20(i2c)

    if sensor.is_device_accessible():
        print(sensor.get_readings())


if __name__ == '__main__':
    main()
