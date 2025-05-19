'''
bmp180 is a micropython module for the Bosch BMP180 sensor. It measures
temperature as well as pressure, with a high enough resolution to calculate
altitude.
Breakoutboard: http://www.adafruit.com/products/1603  
data-sheet: http://ae-bst.resource.bosch.com/media/products/dokumente/
bmp180/BST-BMP180-DS000-09.pdf

The MIT License (MIT)
Copyright (c) 2014 Sebastian Plamauer, oeplse@gmail.com
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Modificado para Raspberry Pi Pico W y compatibilidad con Thonny – 2025
'''

import time
import struct

class BMP180:
    def __init__(self, i2c, addr=0x77):
        self.i2c = i2c
        self.addr = addr
        time.sleep_ms(100)  # Espera tras inicializar I2C

        # Leer coeficientes de calibración (22 bytes desde 0xAA)
        raw = self.i2c.readfrom_mem(self.addr, 0xAA, 22)

        self.ac1 = self._short(raw, 0)
        self.ac2 = self._short(raw, 2)
        self.ac3 = self._short(raw, 4)
        self.ac4 = self._ushort(raw, 6)
        self.ac5 = self._ushort(raw, 8)
        self.ac6 = self._ushort(raw, 10)
        self.b1 = self._short(raw, 12)
        self.b2 = self._short(raw, 14)
        self.mb = self._short(raw, 16)
        self.mc = self._short(raw, 18)
        self.md = self._short(raw, 20)

        self.oversample = 0  # 0 a 3

    def _short(self, data, idx):
        return struct.unpack(">h", data[idx:idx+2])[0]

    def _ushort(self, data, idx):
        return struct.unpack(">H", data[idx:idx+2])[0]

    def read_raw_temp(self):
        self.i2c.writeto_mem(self.addr, 0xF4, b'\x2E')
        time.sleep_ms(5)
        raw = self.i2c.readfrom_mem(self.addr, 0xF6, 2)
        return (raw[0] << 8) | raw[1]

    def read_raw_pressure(self):
        self.i2c.writeto_mem(self.addr, 0xF4, bytes([0x34 + (self.oversample << 6)]))
        time.sleep_ms(2 + (3 << self.oversample))
        raw = self.i2c.readfrom_mem(self.addr, 0xF6, 3)
        return ((raw[0] << 16) + (raw[1] << 8) + raw[2]) >> (8 - self.oversample)

    def measure(self):
        UT = self.read_raw_temp()
        UP = self.read_raw_pressure()

        X1 = ((UT - self.ac6) * self.ac5) >> 15
        X2 = (self.mc << 11) // (X1 + self.md)
        B5 = X1 + X2
        self.temp = ((B5 + 8) >> 4) / 10

        B6 = B5 - 4000
        X1 = (self.b2 * (B6 * B6 >> 12)) >> 11
        X2 = (self.ac2 * B6) >> 11
        X3 = X1 + X2
        B3 = (((self.ac1 * 4 + X3) << self.oversample) + 2) >> 2

        X1 = (self.ac3 * B6) >> 13
        X2 = (self.b1 * ((B6 * B6) >> 12)) >> 16
        X3 = ((X1 + X2) + 2) >> 2
        B4 = (self.ac4 * (X3 + 32768)) >> 15
        B7 = (UP - B3) * (50000 >> self.oversample)

        if B7 < 0x80000000:
            p = (B7 << 1) // B4
        else:
            p = (B7 // B4) << 1

        X1 = (p >> 8) * (p >> 8)
        X1 = (X1 * 3038) >> 16
        X2 = (-7357 * p) >> 16
        self.pressure = p + ((X1 + X2 + 3791) >> 4)

        self.altitude = 44330 * (1 - (self.pressure / 101325) ** (1 / 5.255))

    @property
    def temperature(self):
        return self.temp

    @property
    def pressure_pa(self):
        return self.pressure

    @property
    def pressure_hpa(self):
        return self.pressure / 100

