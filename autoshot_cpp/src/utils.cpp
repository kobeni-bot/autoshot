#include "utils.h"
#include <iostream>
#include <sstream>
#include <iomanip>
#include <chrono>
#include <filesystem>
#include <shellapi.h>

namespace Utils {
    std::wstring stringToWideString(const std::string& str) {
        if (str.empty()) return std::wstring();
        
        int size_needed = MultiByteToWideChar(CP_UTF8, 0, &str[0], (int)str.size(), NULL, 0);
        std::wstring wstrTo(size_needed, 0);
        MultiByteToWideChar(CP_UTF8, 0, &str[0], (int)str.size(), &wstrTo[0], size_needed);
        return wstrTo;
    }

    std::string wideStringToString(const std::wstring& wstr) {
        if (wstr.empty()) return std::string();
        
        int size_needed = WideCharToMultiByte(CP_UTF8, 0, &wstr[0], (int)wstr.size(), NULL, 0, NULL, NULL);
        std::string strTo(size_needed, 0);
        WideCharToMultiByte(CP_UTF8, 0, &wstr[0], (int)wstr.size(), &strTo[0], size_needed, NULL, NULL);
        return strTo;
    }

    std::vector<std::string> getFileList(const std::string& directory, const std::string& extension) {
        std::vector<std::string> files;
        
        try {
            for (const auto& entry : std::filesystem::directory_iterator(directory)) {
                if (entry.is_regular_file()) {
                    std::string filename = entry.path().filename().string();
                    std::string ext = entry.path().extension().string();
                    
                    // Case-insensitive extension comparison
                    std::transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
                    std::string lowerExt = extension;
                    std::transform(lowerExt.begin(), lowerExt.end(), lowerExt.begin(), ::tolower);
                    
                    if (ext == lowerExt) {
                        files.push_back(entry.path().filename().string());
                    }
                }
            }
        } catch (const std::exception& e) {
            std::cerr << "Error reading directory: " << e.what() << std::endl;
        }
        
        return files;
    }

    bool fileExists(const std::string& filename) {
        return std::filesystem::exists(filename);
    }

    std::string getTimestamp() {
        auto now = std::chrono::system_clock::now();
        auto time_t = std::chrono::system_clock::to_time_t(now);
        auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(
            now.time_since_epoch()) % 1000;

        std::stringstream ss;
        ss << std::put_time(std::localtime(&time_t), "%Y%m%d_%H%M%S");
        ss << "." << std::setfill('0') << std::setw(3) << ms.count();
        
        return ss.str();
    }

    COLORREF getPixelColor(int x, int y) {
        HDC hdc = GetDC(NULL);
        COLORREF color = GetPixel(hdc, x, y);
        ReleaseDC(NULL, hdc);
        return color;
    }

    void sleepMillis(int milliseconds) {
        Sleep(milliseconds);
    }
}