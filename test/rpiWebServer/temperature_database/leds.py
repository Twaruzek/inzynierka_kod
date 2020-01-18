import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 120)
pixels.fill((120, 0, 0))   