#include "similarity_detector.h"
#include "utils.h"
#include <filesystem>
#include <algorithm>
#include <cmath>

SimilarityDetector::SimilarityDetector(double threshold) : threshold(threshold) {}

double SimilarityDetector::calculatePHash(const cv::Mat& image1, const cv::Mat& image2) {
    cv::Mat hash1 = computeDctHash(image1);
    cv::Mat hash2 = computeDctHash(image2);
    
    return 1.0 - (calculateHammingDistance(hash1, hash2) / 64.0); // 64 bits in hash
}

bool SimilarityDetector::compareImages(const cv::Mat& image1, const cv::Mat& image2) {
    double similarity = calculatePHash(image1, image2);
    return similarity >= threshold;
}

std::vector<std::string> SimilarityDetector::findSimilarImages(const std::string& imagePath, 
                                                            const std::string& comparisonDir) {
    std::vector<std::string> similarImages;
    
    // Load the reference image
    cv::Mat refImage = cv::imread(imagePath);
    if (refImage.empty()) {
        return similarImages; // Return empty vector if image couldn't be loaded
    }
    
    // Get all PNG files in the comparison directory
    std::vector<std::string> imageFiles = Utils::getFileList(comparisonDir, ".png");
    
    // For efficiency, only compare with the most recent image
    if (!imageFiles.empty()) {
        // Sort by modification time to get the most recent file first
        std::sort(imageFiles.begin(), imageFiles.end(), [](const std::string& a, const std::string& b) {
            return std::filesystem::last_write_time(a) > std::filesystem::last_write_time(b);
        });
        
        // Compare only with the most recent image
        std::string recentImagePath = comparisonDir + "/" + imageFiles[0];
        if (imagePath != recentImagePath) {
            cv::Mat compImage = cv::imread(recentImagePath);
            if (!compImage.empty()) {
                if (compareImages(refImage, compImage)) {
                    similarImages.push_back(recentImagePath);
                }
            }
        }
    }
    
    return similarImages;
}

bool SimilarityDetector::hasSimilarImage(const std::string& imagePath, const std::string& comparisonDir) {
    return !findSimilarImages(imagePath, comparisonDir).empty();
}

cv::Mat SimilarityDetector::computeDctHash(const cv::Mat& image) {
    // Convert to grayscale
    cv::Mat gray;
    if (image.channels() == 1) {
        gray = image.clone();
    } else {
        cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);
    }
    
    // Resize to 32x32 for consistency
    cv::Mat resized;
    cv::resize(gray, resized, cv::Size(32, 32));
    
    // Convert to float
    cv::Mat floatImg;
    resized.convertTo(floatImg, CV_32F);
    
    // Apply DCT
    cv::Mat dctResult;
    cv::dct(floatImg, dctResult);
    
    // Get the 8x8 top-left corner (low frequencies)
    cv::Mat dctBlock = dctResult(cv::Rect(0, 0, 8, 8)).clone();
    
    // Calculate median value
    cv::Mat flat;
    dctBlock.reshape(1, 1).copyTo(flat);
    std::sort(flat.begin<float>(), flat.end<float>());
    float medianVal;
    int size = flat.rows * flat.cols;
    if (size % 2 == 0) {
        medianVal = (flat.at<float>(size/2 - 1) + flat.at<float>(size/2)) / 2.0f;
    } else {
        medianVal = flat.at<float>(size/2);
    }
    
    // Create binary hash
    cv::Mat hash = cv::Mat::zeros(1, 64, CV_8UC1);
    int idx = 0;
    for (int i = 0; i < 8; ++i) {
        for (int j = 0; j < 8; ++j) {
            hash.at<uchar>(0, idx++) = dctBlock.at<float>(i, j) > medianVal ? 1 : 0;
        }
    }
    
    return hash;
}

double SimilarityDetector::calculateHammingDistance(const cv::Mat& hash1, const cv::Mat& hash2) {
    if (hash1.cols != hash2.cols) {
        return -1; // Error: incompatible hash sizes
    }
    
    double distance = 0;
    for (int i = 0; i < hash1.cols; ++i) {
        if (hash1.at<uchar>(0, i) != hash2.at<uchar>(0, i)) {
            distance++;
        }
    }
    
    return distance;
}