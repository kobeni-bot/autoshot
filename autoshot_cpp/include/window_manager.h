#ifndef WINDOW_MANAGER_H
#define WINDOW_MANAGER_H

#include <windows.h>
#include <string>
#include <vector>

struct Rect {
    int left;
    int top;
    int right;
    int bottom;
    
    int width() const { return right - left; }
    int height() const { return bottom - top; }
};

class WindowManager {
public:
    WindowManager();
    ~WindowManager();

    HWND findWindow(const std::wstring& className = L"", const std::wstring& windowName = L"");
    bool resizeWindow(HWND hwnd, int width, int height);
    bool moveWindowToPosition(HWND hwnd, int x, int y, int width, int height);
    Rect getWindowRect(HWND hwnd);
    Rect getClientRect(HWND hwnd);
    bool hideWindow(HWND hwnd);
    bool showWindow(HWND hwnd);

private:
    HMODULE hUser32;
    HMODULE hGdi32;
};

#endif // WINDOW_MANAGER_H