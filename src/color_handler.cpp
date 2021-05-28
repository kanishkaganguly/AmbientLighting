#include "../include/color_handler.hpp"

void ColorHandler::takeScreenshot() {
  ColorHandler::screen(ColorHandler::img);
  return;
}

void ColorHandler::displayScreenshot() {
  cv::imshow("img", ColorHandler::img);
  return;
}

std::array<int, 3> ColorHandler::getDominantColors() {
  cv::Mat reshaped_img;
  ColorHandler::img.convertTo(reshaped_img, CV_32F);
  reshaped_img = reshaped_img.reshape(1, reshaped_img.total());

  cv::Mat labels, centers;
  cv::kmeans(reshaped_img, 8, labels,
             cv::TermCriteria(CV_TERMCRIT_ITER, 10, 1.0), 3,
             cv::KMEANS_PP_CENTERS, centers);

  for (int i = 0; i < 3; i++) {
    dominant_color_rgb[i] = centers.at<float>(i);
  }

  // Convert to HSV
  ColorHandler::rgb_pixel.at<cv::Vec3b>(0, 0) = cv::Vec3b(
      ColorHandler::dominant_color_rgb[2], ColorHandler::dominant_color_rgb[1],
      ColorHandler::dominant_color_rgb[0]);
  cv::cvtColor(ColorHandler::rgb_pixel, ColorHandler::hsv_pixel,
               cv::COLOR_RGB2HSV);

  // Rescale HSV to (360,100,100) from (179, 255, 255)
  cv::Vec3b cv_hsv = hsv_pixel.at<cv::Vec3b>(0, 0);
  cv_hsv.val[0] = (cv_hsv.val[0] / 180.0) * 360.0;
  cv_hsv.val[1] = (cv_hsv.val[1] / 255.0) * 100.0;
  cv_hsv.val[2] = (cv_hsv.val[2] / 255.0) * 100.0;
  hsv_pixel.at<cv::Vec3b>(0, 0) = cv_hsv;

  // Convert to HSV vector
  for (int i = 0; i < 3; i++) {
    ColorHandler::dominant_color_hsv[i] = (int)cv_hsv.val[i];
  }

  return ColorHandler::dominant_color_hsv;
}

PYBIND11_MODULE(libcolor_handler, m) {
  py::class_<ColorHandler>(m, "ColorHandler")
      .def(py::init<const int &, const int &>())
      .def("take_screenshot", &ColorHandler::takeScreenshot,
           "Take a screenshot")
      .def("show_screenshot", &ColorHandler::displayScreenshot,
           "Show the screenshot")
      .def("get_dominant_hsv", &ColorHandler::getDominantColors,
           "Compute dominant colors in HSV");
}