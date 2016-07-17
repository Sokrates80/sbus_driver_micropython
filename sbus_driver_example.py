"""
The MIT License (MIT)
Copyright (c) 2016 Fabrizio Scimia, fabrizio.scimia@gmail.com
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
"""

import pyb
from receiver.sbus_receiver import SBUSReceiver


def update_rx_data(timRx):
    global update_rx
    update_rx = True


def status_led(tim1):
    global updateLed
    updateLed = True
    led.toggle()

updateLed = False
update_rx = False
led = pyb.LED(4)

# Init the SBUS driver on UART port 3
sbus = SBUSReceiver(3)

# Init Rx Timing at 300us (Frsky specific)
timRx = pyb.Timer(2)
timRx.init(freq=2778)
timRx.callback(update_rx_data)

# Init Timer for status led (1 sec interval)
tim1 = pyb.Timer(1)
tim1.init(freq=1)
tim1.callback(status_led)

while True:

    if update_rx:
        sbus.get_new_data()
        update_rx = False

    if updateLed:
        # Print SBUS information every 1 sec
        print(sbus.get_rx_channels())
        updateLed = False
