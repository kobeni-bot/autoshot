#include "window_manager.h"
#include <iostream>

WindowManager::WindowManager() {
    hUser32 = GetModuleHandle(L"user32.dll");
    hGdi32 = GetModuleHandle(L"gdi32.dll");
}

WindowManager::~WindowManager() {
    // Cleanup if needed
}

HWND WindowManager::findWindow(const std::wstring& className, const std::wstring& windowName) {
    return FindWindowW(className.c_str(), windowName.c_str());
}

bool WindowManager::resizeWindow(HWND hwnd, int width, int height) {
    return SetWindowPos(hwnd, NULL, 0, 0, width, height, 
                       SWP_NOMOVE | SWP_NOZORDER) == TRUE;
}

bool WindowManager::moveWindowToPosition(HWND hwnd, int x, int y, int width, int height) {
    return SetWindowPos(hwnd, NULL, x, y, width, height, SWP_NOZORDER) == TRUE;
}

Rect WindowManager::getWindowRect(HWND hwnd) {
    RECT rect;
    GetWindowRect(hwnd, &rect);
    return {rect.left, rect.top, rect.right, rect.bottom};
}

Rect WindowManager::getClientRect(HWND hwnd) {
    RECT windowRect = getWindowRect(hwnd);
    RECT rect;
    GetClientRect(hwnd, &rect);
    
    // Convert client rect to screen coordinates
    POINT topLeft = {rect.left, rect.top};
    POINT bottomRight = {rect.right, rect.bottom};
    ClientToScreen(hwnd, &topLeft);
    ClientToScreen(hwnd, &bottomRight);
    
    return {topLeft.x, topLeft.y, bottomRight.x, bottomRight.y};
}

bool WindowManager::hideWindow(HWND hwnd) {
    return ShowWindow(hwnd, SW_HIDE) == TRUE;
}

bool WindowManager::showWindow(HWND hwnd) {
    return ShowWindow(hwnd, SW_SHOW) == TRUE;
}