#ifndef IMAGE_PROCESSOR_H
#define IMAGE_PROCESSOR_H

#include <opencv2/opencv.hpp>
#include <string>
#include <vector>

class ImageProcessor {
public:
    ImageProcessor(const std::string& outputDir = "chat_shot");
    
    cv::Mat captureWindow(HWND hwnd);
    cv::Mat cropTopHalf(const cv::Mat& image);
    bool saveImage(const cv::Mat& image, const std::string& filename);
    std::string createUniqueFilename(const std::string& prefix = "screenshot", 
                                   const std::string& extension = ".png");
    std::vector<std::string> getImageFiles();
    
private:
    std::string outputDir;
};

#endif // IMAGE_PROCESSOR_H