"""
Similarity Detector Module
Handles perceptual hash calculation and image similarity detection
"""
from PIL import Image
import imagehash
import os
from pathlib import Path
from typing import List, Tuple


class SimilarityDetector:
    def __init__(self, threshold: float = 0.999):
        self.threshold = threshold  # Similarity threshold (0.9 = 90%)

    def calculate_phash(self, image: Image.Image) -> imagehash.ImageHash:
        """
        Calculate the perceptual hash of an image
        
        Args:
            image: Input PIL Image
            
        Returns:
            Perceptual hash of the image
        """
        # Convert to grayscale for more consistent hashing
        gray_image = image.convert('L')
        # Calculate perceptual hash
        phash = imagehash.average_hash(gray_image)
        return phash

    def compare_images(self, hash1: ImageHash, hash2: ImageHash) -> float:
        """
        Compare two image hashes and return similarity ratio
        
        Args:
            hash1: First image hash
            hash2: Second image hash
            
        Returns:
            Similarity ratio between 0 and 1
        """
        # Calculate the hamming distance between hashes
        distance = hash1 - hash2
        # Convert to similarity ratio (0-1 scale)
        # Max possible distance for 64-bit hash is 64
        similarity = 1 - (distance / 64.0)
        return max(similarity, 0)  # Ensure non-negative value

    def find_similar_images(self, image_path: str, comparison_dir: str) -> List[str]:
        """
        Find similar images in a directory compared to a reference image
        Only compares with the most recent image in the directory

        Args:
            image_path: Path to the reference image
            comparison_dir: Directory to search for similar images

        Returns:
            List of paths to similar images
        """
        ref_image = Image.open(image_path)
        ref_phash = self.calculate_phash(ref_image)

        similar_images = []

        # Get the most recent image in the directory (excluding the reference image)
        image_files = list(Path(comparison_dir).glob("*.png"))
        image_files = [f for f in image_files if str(f) != image_path]
        
        # Sort by modification time, most recent first
        image_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Only compare with the most recent image (if it exists)
        if image_files:
            most_recent_file = image_files[0]
            try:
                comp_image = Image.open(most_recent_file)
                comp_phash = self.calculate_phash(comp_image)

                similarity = self.compare_images(ref_phash, comp_phash)

                if similarity >= self.threshold:
                    similar_images.append(str(most_recent_file))
            except Exception:
                # Skip file if it can't be opened as an image
                pass

        return similar_images

    # def has_similar_image(self, image_path: str, comparison_dir: str) -> bool:
    #     """
    #     Check if there's already a similar image in the directory
        
    #     Args:
    #         image_path: Path to the reference image
    #         comparison_dir: Directory to search for similar images
            
    #     Returns:
    #         True if a similar image exists, False otherwise
    #     """
    #     return len(self.find_similar_images(image_path, comparison_dir)) > 0