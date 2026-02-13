#include "image_processor.h"
#include "utils.h"
#include <filesystem>
#include <iostream>

ImageProcessor::ImageProcessor(const std::string& outputDir) : outputDir(outputDir) {
    // Create output directory if it doesn't exist
    std::filesystem::create_directories(outputDir);
}

cv::Mat ImageProcessor::captureWindow(HWND hwnd) {
    // Get window dimensions
    RECT windowRect;
    GetWindowRect(hwnd, &windowRect);
    
    int width = windowRect.right - windowRect.left;
    int height = windowRect.bottom - windowRect.top;
    
    // Get device context
    HDC hWindowDC = GetDC(hwnd);
    HDC hMemDC = CreateCompatibleDC(hWindowDC);
    
    // Create bitmap
    HBITMAP hBitmap = CreateCompatibleBitmap(hWindowDC, width, height);
    HGDIOBJ hOldBitmap = SelectObject(hMemDC, hBitmap);
    
    // Copy window content to bitmap
    PrintWindow(hwnd, hMemDC, PW_RENDERFULLCONTENT);
    BitBlt(hMemDC, 0, 0, width, height, hWindowDC, 0, 0, SRCCOPY);
    
    // Convert HBITMAP to cv::Mat
    BITMAP bmp;
    GetObject(hBitmap, sizeof(bmp), &bmp);
    
    BITMAPINFOHEADER bmi = {0};
    bmi.biSize = sizeof(BITMAPINFOHEADER);
    bmi.biWidth = bmp.bmWidth;
    bmi.biHeight = -bmp.bmHeight;  // Negative for top-down DIB
    bmi.biPlanes = 1;
    bmi.biBitCount = 32;
    bmi.biCompression = BI_RGB;
    
    cv::Mat mat(height, width, CV_8UC4);  // 4 channels for BGRA
    GetDIBits(hMemDC, hBitmap, 0, height, mat.data, (BITMAPINFO*)&bmi, DIB_RGB_COLORS);
    
    // Convert BGRA to BGR
    cv::cvtColor(mat, mat, cv::COLOR_BGRA2BGR);
    
    // Clean up
    SelectObject(hMemDC, hOldBitmap);
    DeleteObject(hBitmap);
    DeleteDC(hMemDC);
    ReleaseDC(hwnd, hWindowDC);
    
    return mat;
}

cv::Mat ImageProcessor::cropTopHalf(const cv::Mat& image) {
    int height = image.rows;
    int centerY = height / 2;
    
    // Create ROI for top half
    cv::Rect roi(0, 0, image.cols, centerY);
    return image(roi).clone();
}

bool ImageProcessor::saveImage(const cv::Mat& image, const std::string& filename) {
    std::string fullPath = outputDir + "/" + filename;
    return cv::imwrite(fullPath, image);
}

std::string ImageProcessor::createUniqueFilename(const std::string& prefix, const std::string& extension) {
    std::string timestamp = Utils::getTimestamp();
    return prefix + "_" + timestamp + extension;
}

std::vector<std::string> ImageProcessor::getImageFiles() {
    return Utils::getFileList(outputDir, ".png");
}