#!/home/kganguly/Documents/Projects/AmbientLights/venv/bin/python3

from pyHS100 import SmartBulb, Discover
import numpy as np
import time
import libcolor_handler as img_proc


class Bulby:
    def __init__(self):
        self.bulb = None

    def init_bulb(self, alias="DeskLamp"):
        for dev in Discover.discover().values():
            if isinstance(dev, SmartBulb) and dev.alias == alias:
                self.bulb = dev
                return True
        return False

    def start_bulb(self):
        if self.bulb.state == "OFF":
            self.bulb.turn_on()

    def stop_bulb(self):
        if self.bulb.state == "ON":
            self.bulb.turn_off()

    def get_bulb_state(self):
        if self.bulb.state == "ON":
            return True
        if self.bulb.state == "OFF":
            return False

    def get_bulb_name(self):
        return self.bulb.alias

    def set_bulb_color(self, hsv):
        if self.bulb.is_color:
            self.bulb.hsv = tuple(hsv)

    def get_bulb_color(self, hsv):
        if self.bulb.is_color:
            return self.bulb.hsv

    def set_bulb_brightness(self, brightness):
        if self.bulb.is_dimmable:
            self.bulb.brightness = brightness

    def get_bulb_brightness(self):
        if self.bulb.is_dimmable:
            return self.bulb.brightness


def main():
    color_cap = img_proc.ColorHandler(1920, 1080)
    bulb_manager = Bulby()

    bulb_manager.init_bulb()
    bulb_manager.start_bulb()

    try:
        while True:
            start = time.time()
            color_cap.take_screenshot()
            print(f"Capture: {time.time()-start}")

            start = time.time()
            bulb_color = color_cap.get_dominant_hsv()
            print(bulb_color)
            print(f"GetColor: {time.time()-start}")

            start = time.time()
            bulb_manager.set_bulb_color(bulb_color)
            print(f"SetColor: {time.time()-start}")

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Done")


if __name__ == "__main__":
    main()
