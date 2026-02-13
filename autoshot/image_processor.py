"""
Image Processor Module
Handles image operations like cropping and saving
"""
from PIL import Image
import os
from pathlib import Path
from typing import Tuple
import time


class ImageProcessor:
    def __init__(self, output_dir: str = "chat_shot"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def crop_top_half(self, image: Image.Image) -> Image.Image:
        """
        Crop the top half of an image
        
        Args:
            image: Input PIL Image
            
        Returns:
            Cropped PIL Image
        """
        width, height = image.size
        # Calculate the rectangle for the top half
        left = 0
        top = 0
        right = width
        bottom = height // 2
        
        return image.crop((left, top, right, bottom))

    def save_image(self, image: Image.Image, filename: str) -> str:
        """
        Save an image to the output directory
        
        Args:
            image: PIL Image to save
            filename: Name of the file to save as
            
        Returns:
            Full path of saved image
        """
        filepath = self.output_dir / filename
        image.save(filepath)
        return str(filepath)

    def create_unique_filename(self, prefix: str = "screenshot", extension: str = ".png") -> str:
        """
        Create a unique filename based on timestamp
        
        Args:
            prefix: Filename prefix
            extension: File extension
            
        Returns:
            Unique filename
        """
        timestamp = int(time.time() * 1000)  # Millisecond precision
        return f"{prefix}_{timestamp}{extension}"