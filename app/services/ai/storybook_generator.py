"""
Storybook generation service.
This module handles the generation of storybook illustrations and PDFs.
"""

import os
import random
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any
import requests
from openai import OpenAI
from dotenv import load_dotenv

from app.services.ai.image_generator import ImageGenerator
from app.services.ai.pdf_generator import PDFGenerator
from app.utils.helpers import sanitize_filename

load_dotenv()

class StorybookGenerator:
    """Service for generating storybook illustrations and PDFs."""
    
    def __init__(self):
        self.using_dalle = True  # Flag to use DALL-E
        self.image_generator = ImageGenerator(using_dalle=self.using_dalle)
        self.pdf_generator = PDFGenerator()
        
    def _format_character_features(self, characters: List[Dict[str, Any]]) -> str:
        """Format character features for image generation."""
        all_character_features = ""
        for character in characters:
            character_name = character.get('character_name', 'Unknown')
            features = character.get('character_features', '')
            all_character_features += f"Name of Character: {character_name}:\n\nFeatures of {character_name}: {features}:\n"
        return all_character_features
    
    def _get_resolution(self) -> str:
        """Get image resolution based on the image generation method."""
        if self.using_dalle:
            return "1024x1024"
        else:
            return "800X1280"
    
    async def generate_cover_page_async(self, cover_picture_description: str, 
                                      all_character_features: str, title: str, 
                                      resolution: str, random_number: int):
        """Generate cover page asynchronously."""
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            return await loop.run_in_executor(
                pool,
                self._generate_cover_page,
                cover_picture_description,
                all_character_features,
                title,
                resolution,
                random_number
            )
    
    def _generate_cover_page(self, cover_picture_description: str, 
                           all_character_features: str, title: str, 
                           resolution: str, random_number: int):
        """Generate cover page."""
        print(f"==> Generating cover page")
        
        # Generate cover image
        if self.using_dalle:
            response = self.image_generator.generate_dalle_image(
                cover_picture_description, all_character_features, False
            )
        else:
            response = self.image_generator.generate_image(
                cover_picture_description, all_character_features, False, random_number
            )
        
        # Download and process cover image
        self.image_generator.download_image_from_response(response, "page_0_image.png")
        
        # Set seed and resolution based on image generation method
        if self.using_dalle:
            seed = random_number  # For DALL-E, use the random number as seed
            resolution = "1024x1024"  # DALL-E 3 default resolution
            print(f"---> DEBUG: Using Seed: {seed} for DALL-E")
            print(f"--->DEBUG: Resolution: {resolution} for DALL-E")
        else:
            seed = random_number
            resolution = self.image_generator.get_image_resolution(response.json())
            print(f"---> DEBUG: Using Seed: {seed} from the cover image")
            print(f"--->DEBUG: Resolution: {resolution} from the cover image")
        
        # Generate cover text image
        self.image_generator.generate_image_from_page_text(
            title, resolution, "page_0_text_image.png", "images", is_cover=True
        )
        
        # Merge images
        if self.image_generator.merge_images_horizontally(
            "images", "page_0_image.png", "page_0_text_image.png", "page_0_combined_image.png"
        ):
            # Clean up individual images
            os.remove("images/page_0_image.png")
            os.remove("images/page_0_text_image.png")
            print("Deleted images/page_0_image.png and images/page_0_text_image.png")
            return True, seed, resolution
        else:
            print("Failed to merge images.")
            return False, None, None
    
    async def process_page_async(self, page: Dict[str, Any], all_character_features: str, 
                               resolution: str, page_font: str, seed: int):
        """Process a single page asynchronously."""
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            await loop.run_in_executor(
                pool, 
                self._process_page, 
                page, 
                all_character_features, 
                resolution, 
                page_font, 
                seed
            )
    
    def _process_page(self, page: Dict[str, Any], all_character_features: str, 
                     resolution: str, page_font: str, seed: int):
        """Process a single page."""
        page_num = page.get('page_num', 0)
        print(f"==> Processing page {page_num}")
        
        # Generate page image
        if self.using_dalle:
            response = self.image_generator.generate_dalle_image(
                page['page_picture_description'], all_character_features, True
            )
        else:
            response = self.image_generator.generate_image(
                page['page_picture_description'], all_character_features, True, seed
            )
        
        # Download and process page image
        self.image_generator.download_image_from_response(response, f"page_{page_num}_image.png")
        
        # Generate page text image
        self.image_generator.generate_image_from_page_text(
            page['page_text'], resolution, f"page_{page_num}_text_image.png", 
            "images", is_cover=False, font_to_use=page_font
        )
        
        # Merge images
        if self.image_generator.merge_images_horizontally(
            "images", f"page_{page_num}_image.png", f"page_{page_num}_text_image.png", 
            f"page_{page_num}_combined_image.png"
        ):
            # Clean up individual images
            os.remove(f"images/page_{page_num}_image.png")
            os.remove(f"images/page_{page_num}_text_image.png")
            print(f"Deleted images/page_{page_num}_image.png and images/page_{page_num}_text_image.png")
        else:
            print(f"Failed to merge images for page {page_num}.")
        
        print(f"==> Done processing page {page_num}")
    
    async def generate_storybook(self, title: str, characters: List[Dict[str, Any]], 
                               cover_picture_description: str, num_pages: int, 
                               pages: List[Dict[str, Any]]) -> str:
        """
        Generate a complete storybook with illustrations and PDF.
        
        Args:
            title: Story title
            characters: List of character descriptions
            cover_picture_description: Description for cover image
            num_pages: Number of pages
            pages: List of page data
            
        Returns:
            Name of the generated PDF file
        """
        start_time = time.time()
        print("Generating storybook illustration...")
        print(f"Title: {title}")
        print(f"Characters: {characters}")
        print(f"Cover picture description: {cover_picture_description}")
        print(f"Number of pages: {num_pages}")
        print(f"Pages: {pages}")
        
        # Format character features
        all_character_features = self._format_character_features(characters)
        
        # Get resolution and setup
        resolution = self._get_resolution()
        random_number = random.randint(1, 10000000)
        page_font = self.image_generator.get_random_font()
        seed = random_number
        
        # Generate all pages in parallel
        tasks = [
            self.generate_cover_page_async(
                cover_picture_description, all_character_features, title, resolution, random_number
            ),
            *[
                self.process_page_async(page, all_character_features, resolution, page_font, seed)
                for page in pages
            ]
        ]
        await asyncio.gather(*tasks)
        
        # Generate PDF in storybooks directory
        storybook_name = sanitize_filename(title) + ".pdf"
        storybooks_dir = "storybooks"
        os.makedirs(storybooks_dir, exist_ok=True)
        storybook_path = os.path.join(storybooks_dir, storybook_name)
        self.pdf_generator.convert_images_to_pdf("images", storybook_path)
        print(f"PDF created successfully: {storybook_name}")
        
        # Clean up images folder
        for file in os.listdir("images"):
            os.remove(os.path.join("images", file))
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for get_storybook_illustration: {execution_time:.2f} seconds")
        
        return storybook_name

# Global instance
storybook_generator = StorybookGenerator()

async def get_storybook_illustration(title: str, characters: List[Dict[str, Any]], 
                                   cover_picture_description: str, num_pages: int, 
                                   pages: List[Dict[str, Any]]) -> str:
    """
    Convenience function to generate storybook illustration.
    
    Args:
        title: Story title
        characters: List of character descriptions
        cover_picture_description: Description for cover image
        num_pages: Number of pages
        pages: List of page data
        
    Returns:
        Name of the generated PDF file
    """
    return await storybook_generator.generate_storybook(
        title, characters, cover_picture_description, num_pages, pages
    ) 