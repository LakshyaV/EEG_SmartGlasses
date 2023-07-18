import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import displayio
import analogio
import time
import eegcode

i2c = busio.I2C(board.GP1, board.GP0)
adc = analogio.AnalogIn(board.A0)
result = eegcode.text

display_width = 96
display_height = 16

display = SSD1306_I2C(display_width, display_height, i2c, addr=0x3C)

def main():
    display.fill(0)

    try:
        font = bitmap_font.load_font("/fonts/arial-12.bdf")
    except FileNotFoundError:
        raise RuntimeError("Font not found. Please add the font file to the CIRCUITPY drive")

    group = displayio.Group()

    text_area = label.Label(font, text=str(result), color=0xFFFFFF, x=0, y=0)
    group.append(text_area)

    display.show(group)

    print('displaying')
    print(adc.value)
    time.sleep(0.1)

while True:
    main()
