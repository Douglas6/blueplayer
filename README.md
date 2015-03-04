BluePlayer
==========

A Raspberry Pi Bluetooth audio player for 16x20 LCDs
Copyright (c) 2015, Douglas Otwell
Distributed under the MIT license http://opensource.org/licenses/MIT

Requirements
------------

*    BlueZ 5 (tested with BlueZ 5.23)
*    PulsaAudio 5 (tested with PulseAudio 5.0)
*    Adafruit 16x2 character LCD display and Python libraries
     (Adafruit_CharLCDPlate.py and Adafruit_I2C.py)

Installation
------------

    git clone https://github.com/douglas6/blueplayer.git
    cd blueplayer

Usage
-----

You'll need to run BluePlayer as the root user:

    sudo python blueplayer.py

Select button: Make the Raspberry Pi discoverable (to accept pairing requests)
Left button: Previous track
Right button: Next track
Down button: Toggle pause/play
