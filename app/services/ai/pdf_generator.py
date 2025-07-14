"""
PDF generation service.
This module handles conversion of images to PDF files.
"""

import os
import img2pdf
from typing import List

class PDFGenerator:
    """Service for generating PDFs from images."""
    
    def convert_images_to_pdf(self, directory_name: str, output_pdf: str):
        """
        Convert a series of images into a single PDF file.
        
        Args:
            directory_name: Directory containing the images
            output_pdf: Name of the output PDF file
        """
        # Get the current directory of the Python file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create the full path by joining the current directory and the input directory name
        image_directory = os.path.join(current_dir, '..', '..', '..', directory_name)
        
        # Get all image files from the directory
        if not os.path.exists(image_directory):
            print(f"Directory {image_directory} does not exist. Operation failed.")
            return
        
        image_files = [
            f for f in os.listdir(image_directory) 
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
        ]
        print(image_files)
        
        # Sort the files based on filename in ascending order
        image_files.sort(key=lambda x: int(x.split('_')[1]) if x.startswith('page_') and x.split('_')[1].isdigit() else float('inf'))
        
        # Create full paths for the image files
        image_paths = [os.path.join(image_directory, img) for img in image_files]
        
        # Convert images to PDF
        with open(output_pdf, "wb") as f:
            f.write(img2pdf.convert(image_paths))
        
        print(f"PDF created successfully: {output_pdf}")
    
    def convert_images_to_pdf_from_list(self, image_paths: List[str], output_pdf: str):
        """
        Convert a list of image paths into a single PDF file.
        
        Args:
            image_paths: List of image file paths
            output_pdf: Name of the output PDF file
        """
        # Convert images to PDF
        with open(output_pdf, "wb") as f:
            f.write(img2pdf.convert(image_paths))
        
        print(f"PDF created successfully: {output_pdf}")
    
    def validate_image_files(self, image_paths: List[str]) -> bool:
        """
        Validate that all image files exist and are readable.
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            True if all files are valid, False otherwise
        """
        for path in image_paths:
            if not os.path.exists(path):
                print(f"Image file does not exist: {path}")
                return False
            if not path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                print(f"Invalid image format: {path}")
                return False
        return True 