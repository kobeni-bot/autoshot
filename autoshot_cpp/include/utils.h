#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <vector>
#include <windows.h>

namespace Utils {
    // String conversion utilities
    std::wstring stringToWideString(const std::string& str);
    std::string wideStringToString(const std::wstring& wstr);
    
    // File utilities
    std::vector<std::string> getFileList(const std::string& directory, const std::string& extension = ".png");
    bool fileExists(const std::string& filename);
    std::string getTimestamp();
    
    // Pixel utilities
    COLORREF getPixelColor(int x, int y);
    void sleepMillis(int milliseconds);
}

#endif // UTILS_H