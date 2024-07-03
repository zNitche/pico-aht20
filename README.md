### pico-aht20

MicroPython module for performing measurements (temperature, humidity) using AHT20 sensor.

#### Usage
```
import machine
import aht20


def main():
    i2c = machine.I2C(1, sda=machine.Pin(2), scl=machine.Pin(3))
    sensor = aht20.AHT20(i2c)

    if sensor.is_device_accessible():
        print(sensor.get_readings())


if __name__ == '__main__':
    main()
```

#### Resources
- [Inspiration](https://github.com/adafruit/Adafruit_CircuitPython_AHTx0)
- [Datasheet](https://cdn-learn.adafruit.com/assets/assets/000/123/394/original/Data_Sheet_AHT20.pdf)
