#pragma once
// @formatter:off
#include <opencv2/opencv.hpp>
// @formatter:off
#include <opencv2/highgui/highgui_c.h>
// @formatter:on
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <algorithm>
#include <cmath>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>

namespace py = pybind11;

class Screenshot {
private:
  Display *display;
  Window root;
  int x, y, width, height;
  XImage *img{nullptr};

public:
  Screenshot(int x, int y, int width, int height)
      : x(x), y(y), width(width), height(height) {
    display = XOpenDisplay(nullptr);
    root = DefaultRootWindow(display);
  }

  void operator()(cv::Mat &cvImg) {
    if (img != nullptr)
      XDestroyImage(img);
    img = XGetImage(display, root, x, y, width, height, AllPlanes, ZPixmap);
    cvImg = cv::Mat(height, width, CV_8UC4, img->data);
  }

  ~Screenshot() {
    if (img != nullptr)
      XDestroyImage(img);
    XCloseDisplay(display);
  }
};

class ColorHandler {
public:
  ColorHandler(const int &w, const int &h)
      : screen(0, 0, w, h), width(w), height(h),
        img(cv::Mat::zeros(w, h, CV_8UC3)),
        rgb_pixel(1, 1, CV_8UC3, cv::Scalar(0, 0, 0)),
        hsv_pixel(1, 1, CV_8UC3, cv::Scalar(0, 0, 0)){};

  void takeScreenshot();
  void displayScreenshot();
  std::array<int, 3> getDominantColors();

private:
  cv::Mat img, rgb_pixel, hsv_pixel;
  Screenshot screen;
  std::array<float, 3> dominant_color_rgb;
  std::array<int, 3> dominant_color_hsv;
  const int &width;
  const int &height;
};