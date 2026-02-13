"""
Main Module
Orchestrates the entire screenshot and similarity detection workflow
"""
import time
import os
from pathlib import Path
from typing import Optional
import threading

from .window_manager import WindowManager
from .image_processor import ImageProcessor
from .similarity_detector import SimilarityDetector


class AutoShot:
    def __init__(self, window_title: str, width: int, height: int, interval: int = 2):
        """
        Initialize the AutoShot tool
        
        Args:
            window_title: Title of the window to capture
            width: Target width for the window
            height: Target height for the window
            interval: Time interval between screenshots in seconds (default 2)
        """
        self.window_title = window_title
        self.width = width
        self.height = height
        self.interval = interval
        
        self.window_manager = WindowManager()
        self.image_processor = ImageProcessor()
        self.similarity_detector = SimilarityDetector
        
        self.running = False
        self.capture_thread = None

    def setup_window(self) -> bool:
        """
        Find and resize the target window
        
        Returns:
            True if successful, False otherwise
        """
        hwnd = self.window_manager.find_window(window_name=self.window_title)
        if hwnd is None:
            print(f"Window '{self.window_title}' not found.")
            return False
            
        print(f"Found window: {self.window_title} (Handle: {hwnd})")
        
        # Resize the window
        success = self.window_manager.resize_window(hwnd, self.width, self.height)
        if success:
            print(f"Resized window to {self.width}x{self.height}")
        else:
            print("Failed to resize window")
            
        return success

    def capture_screenshot(self, hwnd: int) -> Optional[str]:
        """
        Capture a screenshot of the specified window and save it
        
        Args:
            hwnd: Window handle to capture
            
        Returns:
            Path to saved image or None if failed
        """
        try:
            # Import here to avoid circular dependencies
            from PIL import ImageGrab
            
            # Get client rectangle (the actual content area without borders/title bar)
            rect = self.window_manager.get_client_rect(hwnd)
            if rect is None:
                print("Could not get window client rectangle, falling back to window rectangle")
                # Fallback to window rectangle if client rectangle fails
                rect = self.window_manager.get_window_rect(hwnd)
                if rect is None:
                    print("Could not get window rectangle")
                    return None
                
            # Take screenshot of the client area
            left, top, right, bottom = rect
            bbox = (left, top, right, bottom)
            screenshot = ImageGrab.grab(bbox=bbox)
            
            # Crop to top half
            cropped_image = self.image_processor.crop_top_half(screenshot)
            
            # Generate unique filename
            filename = self.image_processor.create_unique_filename()
            
            # Save the cropped image
            saved_path = self.image_processor.save_image(cropped_image, filename)
            print(f"Screenshot saved: {saved_path}")
            
            return saved_path
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None

    def remove_duplicates(self, new_image_path: str):
        """
        Remove duplicate images based on similarity
        
        Args:
            new_image_path: Path to the newly captured image
        """
        # Find similar images
        similar_images = self.similarity_detector.find_similar_images(
            new_image_path, 
            str(self.image_processor.output_dir)
        )
        
        # Remove similar images (keeping only the newest one)
        for sim_img in similar_images:
            if sim_img != new_image_path:
                try:
                    os.remove(sim_img)
                    print(f"Removed duplicate image: {sim_img}")
                except OSError as e:
                    print(f"Could not remove duplicate image {sim_img}: {e}")

    def get_pixel_at_screenshot_coords(self, hwnd: int, screenshot_x: int, screenshot_y: int) -> Optional[tuple]:
        """
        Get the pixel color at specific coordinates in the screenshot
        
        Args:
            hwnd: Window handle
            screenshot_x: X coordinate in the screenshot
            screenshot_y: Y coordinate in the screenshot
            
        Returns:
            Tuple of (R, G, B) values or None if failed
        """
        # Use client area by default for more accurate results
        return self.window_manager.get_pixel_from_screenshot_coords(
            hwnd, screenshot_x, screenshot_y, use_client_area=True
        )

    def single_capture_cycle(self):
        """
        Perform a single capture cycle: capture, process, deduplicate
        """
        # Find the window
        hwnd = self.window_manager.find_window(window_name=self.window_title)
        if hwnd is None:
            print(f"Window '{self.window_title}' not found.")
            return False

        # Capture screenshot
        image_path = self.capture_screenshot(hwnd)
        if image_path is None:
            print("Capture failed")
            return False

        # Check if there are other images in the directory
        image_files = list(Path(self.image_processor.output_dir).glob("*.png"))

        if len(image_files) > 1:  # More than just the newly added one
            # Remove duplicates
            self.remove_duplicates(image_path)

        return True

    def start_capture_loop(self):
        """
        Start the continuous capture loop in a separate thread
        """
        if self.running:
            print("Capture loop is already running")
            return
            
        self.running = True
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()
        print("Started capture loop")

    def stop_capture_loop(self):
        """
        Stop the continuous capture loop
        """
        self.running = False
        if self.capture_thread:
            self.capture_thread.join(timeout=5)  # Wait up to 5 seconds for thread to finish
        print("Stopped capture loop")

    def _capture_loop(self):
        """
        Internal capture loop that runs in a separate thread
        """
        while self.running:
            self.single_capture_cycle()
            time.sleep(self.interval)

    def run_once(self):
        """
        Run a single capture cycle and exit
        """
        print(f"Setting up window '{self.window_title}' to {self.width}x{self.height}")
        if not self.setup_window():
            return
            
        print("Performing single capture cycle...")
        self.single_capture_cycle()


def main():
    """
    Main entry point for the application
    """
    import argparse

    parser = argparse.ArgumentParser(description="AutoShot - Automatic Window Screenshot Tool")
    parser.add_argument("--title", required=True, help="Title of the window to capture")
    parser.add_argument("--width", type=int, required=True, help="Target width for the window")
    parser.add_argument("--height", type=int, required=True, help="Target height for the window")
    parser.add_argument("--interval", type=int, default=2, help="Time interval between screenshots in seconds (default: 2)")
    parser.add_argument("--once", action="store_true", help="Run only once instead of continuously")
    parser.add_argument("--query-pixel", nargs=2, type=int, metavar=('X', 'Y'),
                        help="Query the RGB color of a pixel at the given screenshot coordinates (X Y)")

    args = parser.parse_args()

    autoshot = AutoShot(args.title, args.width, args.height, args.interval)

    if args.query_pixel:
        # Query pixel functionality
        hwnd = autoshot.window_manager.find_window(window_name=args.title)
        if hwnd is None:
            print(f"Window '{args.title}' not found.")
            return
            
        x, y = args.query_pixel
        rgb_color = autoshot.get_pixel_at_screenshot_coords(hwnd, x, y)
        
        if rgb_color:
            r, g, b = rgb_color
            print(f"Pixel at ({x}, {y}) in screenshot corresponds to screen pixel with RGB({r}, {g}, {b})")
        else:
            print(f"Could not get pixel color at ({x}, {y}) in screenshot")
    elif args.once:
        autoshot.run_once()
    else:
        print(f"Starting continuous capture of '{args.title}' every {args.interval}s...")
        autoshot.start_capture_loop()

        try:
            # Keep the main thread alive
            while autoshot.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping...")
            autoshot.stop_capture_loop()


if __name__ == "__main__":
    main()