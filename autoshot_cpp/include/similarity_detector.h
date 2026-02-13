#ifndef SIMILARITY_DETECTOR_H
#define SIMILARITY_DETECTOR_H

#include <opencv2/opencv.hpp>
#include <string>
#include <vector>

class SimilarityDetector {
public:
    SimilarityDetector(double threshold = 0.9);
    
    double calculatePHash(const cv::Mat& image1, const cv::Mat& image2);
    bool compareImages(const cv::Mat& image1, const cv::Mat& image2);
    std::vector<std::string> findSimilarImages(const std::string& imagePath, 
                                              const std::string& comparisonDir);
    bool hasSimilarImage(const std::string& imagePath, const std::string& comparisonDir);
    
private:
    double threshold;
    
    // Helper function to compute perceptual hash
    cv::Mat computeDctHash(const cv::Mat& image);
    double calculateHammingDistance(const cv::Mat& hash1, const cv::Mat& hash2);
};

#endif // SIMILARITY_DETECTOR_H