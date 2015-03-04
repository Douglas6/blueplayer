#!/usr/bin/env python

"""Copyright (c) 2015, Douglas Otwell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from threading import Thread
import time
import string

from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

class Lcd(Adafruit_CharLCDPlate):
    LOOKALIKE = string.maketrans("""\xc0\xc1\xc2\xc3\xc4\xc5\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd9\xda\xdb\xdc\xdd\xde\xdf
                                     \xe0\xe1\xe2\xe3\xe4\xe5\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff""", 
                                  """AAAAAACEEEEIIIIDNOOOOOUUUUYBB
                                     aaaaaaeeeeiiiionoooooouuuuyby""")
    BUTTON_SELECT = 1
    BUTTON_RIGHT = 2
    BUTTON_DOWN = 4
    BUTTON_UP = 8
    BUTTON_LEFT = 16

    worker = None
    polling = True
    handler = None

    def begin(self, cols, rows, handler=None):
        super(Lcd, self).begin(cols, rows)
        self.handler = handler
        if self.handler:
            self.worker = Thread(target=self.getButtons)
            self.worker.start()

    def end(self):
        self.polling = False;
        self.clear()
        self.backlight(Lcd.OFF)
        self.stop()

    def writeLn(self, s, row):
        s = self.replaceDiacritics(s)

        self.setCursor(0, row)
        self.message(str(s[:40].ljust(40)))

    def replaceDiacritics(self, s):
       return s.encode("latin-1").translate(Lcd.LOOKALIKE)

    def getButtons(self):
        button_cache = 0;
        while self.polling:
            test = self.buttons()
            buttons = test - button_cache;
            button_cache = test if test > 0 else 0
            if buttons > 0:
                self.handler(buttons)
            time.sleep(0.1)

    def wrap(self, str):
        lines = [];
        while len(str) > self.numcols:
            idx = str[:self.numcols+1].rfind(" ")
            if idx > 0:
                lines.append(str[:idx])
                str = str[idx+1:].lstrip()
            else:
                lines.append(str[:self.numcols])
                str = str[self.numcols:].lstrip()

        lines.append(str)

        return  lines



if __name__ == "__main__":
    def handleNav(buttons):
        print(buttons)

    try:
        lcd = Lcd()
        lcd.begin(16, 2, handler=handleNav)

        while True:
            time.sleep(1)
    except: 
        lcd.end()



