#include <iostream>
#include <thread>
#include <chrono>
#include <atomic>
#include <csignal>
#include "window_manager.h"
#include "image_processor.h"
#include "similarity_detector.h"
#include "utils.h"

class AutoShot {
public:
    AutoShot(const std::wstring& windowTitle, int width, int height, int interval = 2)
        : windowTitle(windowTitle), width(width), height(height), interval(interval),
          running(false) {}
    
    ~AutoShot() {
        stopCaptureLoop();
    }
    
    bool setupWindow() {
        HWND hwnd = windowManager.findWindow(L"", windowTitle);
        if (!hwnd) {
            std::wcout << L"Window '" << windowTitle << L"' not found." << std::endl;
            return false;
        }
        
        std::wcout << L"Found window: " << windowTitle << L" (Handle: " 
                  << reinterpret_cast<void*>(hwnd) << L")" << std::endl;
        
        bool success = windowManager.resizeWindow(hwnd, width, height);
        if (success) {
            std::wcout << L"Resized window to " << width << L"x" << height << std::endl;
        } else {
            std::wcout << L"Failed to resize window" << std::endl;
        }
        
        this->hwnd = hwnd;
        return success;
    }
    
    bool captureScreenshot() {
        if (!hwnd) {
            std::wcout << L"No valid window handle to capture." << std::endl;
            return false;
        }
        
        cv::Mat screenshot = imageProcessor.captureWindow(hwnd);
        if (screenshot.empty()) {
            std::cout << "Failed to capture screenshot" << std::endl;
            return false;
        }
        
        // Crop to top half
        cv::Mat croppedImage = imageProcessor.cropTopHalf(screenshot);
        
        // Generate unique filename
        std::string filename = imageProcessor.createUniqueFilename();
        
        // Save the cropped image
        bool saved = imageProcessor.saveImage(croppedImage, filename);
        if (saved) {
            std::cout << "Screenshot saved: " << filename << std::endl;
            
            // Check for similar images and remove duplicates
            removeDuplicates(outputDir + "/" + filename);
            
            return true;
        } else {
            std::cout << "Failed to save screenshot: " << filename << std::endl;
            return false;
        }
    }
    
    void singleCaptureCycle() {
        if (!hwnd) {
            std::wcout << L"Window handle is invalid." << std::endl;
            return;
        }
        
        captureScreenshot();
    }
    
    void startCaptureLoop() {
        if (running) {
            std::cout << "Capture loop is already running" << std::endl;
            return;
        }
        
        running = true;
        captureThread = std::thread([this]() {
            while (running) {
                singleCaptureCycle();
                std::this_thread::sleep_for(std::chrono::seconds(interval));
            }
        });
        
        std::cout << "Started capture loop" << std::endl;
    }
    
    void stopCaptureLoop() {
        if (!running) return;
        
        running = false;
        if (captureThread.joinable()) {
            captureThread.join();
        }
        std::cout << "Stopped capture loop" << std::endl;
    }
    
    void runOnce() {
        std::wcout << L"Setting up window '" << windowTitle << L"' to " 
                  << width << L"x" << height << std::endl;
        
        if (!setupWindow()) {
            return;
        }
        
        std::cout << "Performing single capture cycle..." << std::endl;
        singleCaptureCycle();
    }
    
    void removeDuplicates(const std::string& newImagePath) {
        std::vector<std::string> similarImages = similarityDetector.findSimilarImages(
            newImagePath, outputDir
        );
        
        for (const std::string& simImg : similarImages) {
            if (simImg != newImagePath) {
                if (std::filesystem::remove(simImg)) {
                    std::cout << "Removed duplicate image: " << simImg << std::endl;
                } else {
                    std::cout << "Could not remove duplicate image: " << simImg << std::endl;
                }
            }
        }
    }
    
    // Function to get pixel color from screenshot coordinates
    bool getPixelAtScreenshotCoords(int screenshotX, int screenshotY, COLORREF& color) {
        if (!hwnd) {
            std::cout << "No valid window handle." << std::endl;
            return false;
        }
        
        // Get the client rectangle to calculate screen coordinates
        Rect clientRect = windowManager.getClientRect(hwnd);
        
        // Calculate screen coordinates
        int screenX = clientRect.left + screenshotX;
        int screenY = clientRect.top + screenshotY;
        
        // Get the pixel color at screen coordinates
        color = Utils::getPixelColor(screenX, screenY);
        return true;
    }
    
    bool isRunning() const {
        return running;
    }

private:
    std::wstring windowTitle;
    int width, height;
    int interval;
    HWND hwnd = nullptr;
    
    WindowManager windowManager;
    ImageProcessor imageProcessor;
    SimilarityDetector similarityDetector;
    
    std::string outputDir = "chat_shot";
    std::atomic<bool> running;
    std::thread captureThread;
};

// Global variable for signal handling
static std::atomic<bool> shouldStop{false};

void signalHandler(int signal) {
    shouldStop = true;
}

int main(int argc, char* argv[]) {
    // Register signal handler for graceful shutdown
    std::signal(SIGINT, signalHandler);
    
    // Default values
    std::wstring windowTitle = L"";
    int width = 800;
    int height = 600;
    int interval = 2;
    bool onceMode = false;
    bool queryPixel = false;
    int pixelX = 0, pixelY = 0;
    
    // Parse command line arguments
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        
        if (arg == "--title" && i + 1 < argc) {
            windowTitle = Utils::stringToWideString(argv[++i]);
        } else if (arg == "--width" && i + 1 < argc) {
            width = std::stoi(argv[++i]);
        } else if (arg == "--height" && i + 1 < argc) {
            height = std::stoi(argv[++i]);
        } else if (arg == "--interval" && i + 1 < argc) {
            interval = std::stoi(argv[++i]);
        } else if (arg == "--once") {
            onceMode = true;
        } else if (arg == "--query-pixel" && i + 2 < argc) {
            queryPixel = true;
            pixelX = std::stoi(argv[++i]);
            pixelY = std::stoi(argv[++i]);
        } else if (arg == "--help") {
            std::cout << "Usage: " << argv[0] << " [options]\n";
            std::cout << "Options:\n";
            std::cout << "  --title TITLE        Title of the window to capture\n";
            std::cout << "  --width WIDTH        Target width for the window\n";
            std::cout << "  --height HEIGHT      Target height for the window\n";
            std::cout << "  --interval INTERVAL  Time interval between screenshots in seconds (default: 2)\n";
            std::cout << "  --once               Run only once instead of continuously\n";
            std::cout << "  --query-pixel X Y    Query the RGB color of a pixel at the given screenshot coordinates\n";
            std::cout << "  --help               Show this help message\n";
            return 0;
        }
    }
    
    // Validate required arguments
    if (windowTitle.empty()) {
        std::cout << "Error: --title is required\n";
        return 1;
    }
    
    // Create AutoShot instance
    AutoShot autoshot(windowTitle, width, height, interval);
    
    if (queryPixel) {
        // Setup window first
        if (!autoshot.setupWindow()) {
            std::cout << "Failed to setup window for pixel query." << std::endl;
            return 1;
        }
        
        // Query pixel color
        COLORREF color;
        if (autoshot.getPixelAtScreenshotCoords(pixelX, pixelY, color)) {
            int r = GetRValue(color);
            int g = GetGValue(color);
            int b = GetBValue(color);
            std::cout << "Pixel at (" << pixelX << ", " << pixelY 
                      << ") corresponds to screen pixel with RGB(" 
                      << r << ", " << g << ", " << b << ")" << std::endl;
        } else {
            std::cout << "Could not get pixel color at (" << pixelX << ", " << pixelY << ")" << std::endl;
        }
    } else if (onceMode) {
        autoshot.runOnce();
    } else {
        std::wcout << L"Starting continuous capture of '" << windowTitle 
                  << L"' every " << interval << L"s..." << std::endl;
        
        autoshot.startCaptureLoop();
        
        // Keep the main thread alive
        while (autoshot.isRunning() && !shouldStop) {
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
        
        std::cout << "\nStopping..." << std::endl;
        autoshot.stopCaptureLoop();
    }
    
    return 0;
}