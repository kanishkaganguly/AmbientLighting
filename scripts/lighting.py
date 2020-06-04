from pyHS100 import SmartBulb, Discover
import pyscreenshot as ImageGrab
from sklearn.utils.random import sample_without_replacement
from sklearn.cluster import KMeans
from colorsys import rgb_to_hsv
import cv2
import numpy as np
import time
from collections import Counter


class ColorCapture:
    def __init__(self):
        self.clusters = 5

    def show_image(self, img):
        cv2.imshow("Test", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def get_hsv(self, rgb):
        scaling_factors = (360, 100, 100)
        hsv = list(rgb_to_hsv(r=rgb[0]/255, g=rgb[1]/255, b=rgb[2]/255))
        for i in range(len(scaling_factors)):
            hsv[i] *= scaling_factors[i]

        # print(f"RGB: {rgb}, HSV: {hsv}")
        return hsv

    def pixel_sampler(self, img, sample_percent):
        dim = img.shape[0]
        samples = sample_without_replacement(
            n_population=dim, n_samples=int(dim * sample_percent))
        sample_pixels = img[samples]
        return sample_pixels

    def get_screen_patch(self):
        patch_w, patch_h = 50, 50
        screen_w, screen_h = 1920, 1080
        screen_center_x, screen_center_y = int(screen_w / 2), int(screen_h / 2)
        patch_centers = [(screen_center_x, screen_center_y), (int(screen_center_x - 200), int(
            screen_center_y / 2)), (int(screen_center_x / 2 + 200), int(screen_center_y / 2))]
        total_img = np.zeros((100, 300, 3), dtype=np.uint8)

        for idx, patch in enumerate(patch_centers):
            start = (idx) * (patch_h + patch_w)
            end = start + (patch_w + patch_h)
            top_left = patch[0] - patch_w, patch[1] - patch_h
            bottom_right = patch[0] + patch_w, patch[1] + patch_h
            screenshot = ImageGrab.grab(
                bbox=(*top_left, *bottom_right), backend="mss", childprocess=False)
            screenshot_cv = np.array(screenshot)
            total_img[:100, start:end, :] = screenshot_cv
        total_img = total_img.reshape(
            (total_img.shape[0] * total_img.shape[1], 3))
        crop = self.pixel_sampler(total_img, 0.05)
        return crop

    def get_dominant_hsv(self, img):
        """
        See https://adamspannbauer.github.io/2018/03/02/app-icon-dominant-colors/
        """
        kmeans = KMeans(n_clusters=self.clusters)
        labels = kmeans.fit_predict(img)
        label_counts = Counter(labels)
        dominant_color = kmeans.cluster_centers_[
            label_counts.most_common(1)[0][0]]
        dominant_rgb = [int(i) for i in dominant_color]
        dominant_hsv = self.get_hsv(dominant_rgb)
        return list(map(int, dominant_hsv))


class Bulby:
    def __init__(self):
        self.bulb = None

    def init_bulb(self, alias="DeskLamp"):
        for dev in Discover.discover().values():
            if isinstance(dev, SmartBulb) and dev.alias == alias:
                self.bulb = dev

    def start_bulb(self):
        if self.bulb.state == "OFF":
            self.bulb.turn_on()

    def set_bulb_color(self, hsv):
        if self.bulb.is_color:
            self.bulb.hsv = tuple(hsv)


def main():
    color_cap = ColorCapture()
    bulb_manager = Bulby()

    bulb_manager.init_bulb()
    bulb_manager.start_bulb()

    try:
        while True:
            img = color_cap.get_screen_patch()
            bulb_color = color_cap.get_dominant_hsv(img)
            bulb_manager.set_bulb_color(bulb_color)
            time.sleep(5)
    except KeyboardInterrupt:
        print("Done")


if __name__ == "__main__":
    main()
