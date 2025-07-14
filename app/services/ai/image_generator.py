"""
Image generation service.
This module handles image generation, text-to-image conversion, and image manipulation.
"""

import os
import random
import requests
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ImageGenerator:
    """Service for generating and manipulating images."""
    
    def __init__(self, using_dalle=False):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"), 
            base_url=os.getenv("OPENAI_ENDPOINT")
        )
        self.using_dalle = using_dalle
        
        # Font configuration
        self.cover_text_font_size = 72
        self.page_text_font_size = 48
        self.font_to_use = [
            "Optima.ttc",
            "Futura.ttc", 
            "GillSans.ttc",
            "HelveticaNeue.ttc",
            "MarkerFelt.ttc",
            "Georgia.ttf"
        ]
    
    def get_random_font(self) -> str:
        """Get a random font from the available fonts."""
        font_name = random.choice(self.font_to_use)
        font_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'fonts', font_name)
        return font_path
    
    def parse_resolution(self, resolution_string: str) -> tuple:
        """Parse resolution string to width and height."""
        try:
            if resolution_string is None:
                # Default resolution if none provided
                return 800, 1280
            width, height = map(int, resolution_string.lower().split('x'))
            return width, height
        except (ValueError, AttributeError):
            # If parsing fails, return default resolution
            print(f"Warning: Could not parse resolution '{resolution_string}', using default 800x1280")
            return 800, 1280
    
    def generate_dalle_image(self, image_description: str, character_features: str, is_page: bool = False):
        """Generate image using DALL-E 3."""
        if is_page:
            picture_prompt = f"""Create a children's storybook illustration with the following scene: {image_description}\n\nCharacter descriptions: {character_features}\n\nStyle: Children's storybook illustration, colorful, friendly, cartoon style, no text or words in the image, suitable for children."""
        else:
            picture_prompt = f"""Create a children's storybook cover illustration with the following scene: {image_description}\n\nCharacter descriptions: {character_features}\n\nStyle: Children's storybook cover, colorful, friendly, cartoon style, no text or words in the image, suitable for children."""
        
        print(f"\n--->DEBUG DALL-E Prompt: {picture_prompt}")
        
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=picture_prompt,
                size="1024x1024",  # DALL-E 3 supports: 1024x1024, 1792x1024, 1024x1792
                quality="standard",  # "standard" or "hd"
                n=1,
                style="vivid"  # "vivid" or "natural"
            )
            print(f"--->DEBUG DALL-E Response: {response}")
            return response
        except Exception as e:
            print(f"Error generating DALL-E image: {e}")
            raise
    
    def generate_image(self, image_description: str, character_features: str, is_page: bool, seed: Optional[int] = None):
        """Generate image using Ideogram API."""
        if is_page:
            picture_prompt = f"""Generate a picture for a page in a children's story book using the following prompt: \n
            {image_description}\n
            Below you will find a description of each characters that you may need to use for the picture based on the above description. \n
            {character_features} \n

            Make sure the image is in a style appropriate for a children's story book.\n
            Do not create this image as a coverpage.\n
            Ensure to use the seed and create and image where all the characters are still the same age and look similar to the seed picture.\n
                
            IMPORTANT: Do not have add any text to the image!\n
            """
        else:
            picture_prompt = f"""Generate a picture for a children's story book using the following prompt:\n
            {image_description}\n
            Below you will find a description of each characters that you may need to use for the cover picture based on the above description.\n
            {character_features}\n

            Make sure the image is in a style appropriate for a children's story book.\n
                
            IMPORTANT: Do not have add any text to the image!\n
            """
        
        print("\n--->DEBUG: ", picture_prompt)
        print("\n--->INPUT SEED: ", seed)
        
        generation_endpoint = os.getenv("IDEOGRAM_ENDPOINT") + "/generate"
        print("\n--->DEBUG: Generation endpoint: ", generation_endpoint)
        
        headers = {
            "Api-Key": f'{os.getenv("IDEOGRAM_API_KEY")}',
            "Content-Type": "application/json"
        }
        
        if seed is not None:
            payload = {
                "image_request": {
                    "prompt": f"{picture_prompt}",
                    "negative_prompt": "not text, no words, no typography, no letters",
                    "aspect_ratio": "ASPECT_10_16",
                    "model": "V_2",
                    "magic_prompt_option": "OFF",
                    "style_type": "DESIGN",
                    "seed": seed
                }
            }
        else:
            payload = {
                "image_request": {
                    "prompt": f"{picture_prompt}",
                    "negative_prompt": "not text, no words, no typography, no letters",
                    "aspect_ratio": "ASPECT_10_16",
                    "model": "V_2",
                    "style_type": "DESIGN",
                    "magic_prompt_option": "OFF"
                }
            }
        
        print(f"--->DEBUG: Ideogram Payload: {payload}")
        response = requests.post(generation_endpoint, headers=headers, json=payload)
        return response
    
    def get_image_seed(self, response: dict) -> Optional[int]:
        """Extract seed from image generation response."""
        try:
            data_item = response['data'][0]
            seed = int(data_item['seed'])
            return seed
        except (KeyError, IndexError, ValueError):
            print("No seed found in the response.")
            return None
    
    def get_image_url(self, response: dict) -> Optional[str]:
        """Extract image URL from response."""
        try:
            print(f"DEBUG: Full response structure: {response}")
            if 'data' in response and isinstance(response['data'], list) and len(response['data']) > 0:
                image_data = response['data'][0]
                print(f"DEBUG: Image data: {image_data}")
                if 'url' in image_data:
                    return image_data['url']
                elif 'image_url' in image_data:
                    return image_data['image_url']
            return None
        except Exception as e:
            print(f"Error extracting image URL: {e}")
            return None
    
    def get_dalle_image_url(self, response) -> str:
        """Extract image URL from DALL-E response."""
        try:
            print(f"==> Debug DALL-E response type: {type(response)}")
            print(f"==> Debug DALL-E response: {response}")
            
            # Check if response is a string (JSON) instead of an object
            if isinstance(response, str):
                print("ERROR: Response is a string, not an object!")
                import json
                response_dict = json.loads(response)
                return response_dict['data'][0]['url']
            
            # Normal DALL-E object response
            if hasattr(response, 'data') and len(response.data) > 0:
                return response.data[0].url
            else:
                print("ERROR: DALL-E response doesn't have expected structure")
                return None
                
        except Exception as e:
            print(f"Error extracting DALL-E image URL: {e}")
            print(f"Response type: {type(response)}")
            print(f"Response content: {response}")
            raise
    
    def get_image_resolution(self, response: dict) -> Optional[str]:
        """Extract resolution from response."""
        try:
            # For Ideogram API, the resolution is typically in the request, not response
            # Return a default resolution if not found
            if 'data' in response and isinstance(response['data'], list) and len(response['data']) > 0:
                image_data = response['data'][0]
                if 'resolution' in image_data:
                    return image_data['resolution']
            
            # If no resolution found, return default
            return "800x1280"
        except Exception as e:
            print(f"Error extracting resolution: {e}")
            return "800x1280"
    
    def download_image_from_response(self, response, filename: str):
        """Download image from response and save to file."""
        try:
            # Ensure the images folder exists
            images_folder = "images"
            if not os.path.exists(images_folder):
                os.makedirs(images_folder)

            print(f"DEBUG: Response type: {type(response)}")
            print(f"DEBUG: Using DALL-E: {self.using_dalle}")

            if self.using_dalle:
                image_url = self.get_dalle_image_url(response)
            else:
                image_url = self.get_image_url(response.json())
            
            if image_url:
                print(f"---> DEBUG: Image URL: {image_url}")
                self.download_file(image_url, filename, images_folder)
            else:
                print("Image URL not found in the response.")
                
        except Exception as e:
            print(f"Error in download_image_from_response: {e}")
            print(f"Response type: {type(response)}")
            print(f"Response content: {response}")
            raise
    
    def download_file(self, url: str, filename: str, folder: str):
        """Download file from URL and save to folder."""
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        response = requests.get(url)
        if response.status_code == 200:
            file_path = os.path.join(folder, filename)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {filename} to {folder}")
        else:
            print(f"Failed to download {filename}")
    
    def generate_image_from_page_text(self, page_text: str, resolution: str, filename: str, 
                                    folder_name: str, is_cover: bool = False, font_to_use: Optional[str] = None):
        """Generate image from page text."""
        width, height = self.parse_resolution(resolution)
        if font_to_use is None:
            font_to_use = self.get_random_font()
        
        # Create blank image
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        if is_cover:
            font_size = self.cover_text_font_size
        else:
            font_size = self.page_text_font_size
        
        # Define text and font
        text = page_text
        print("Using font:")
        print(font_to_use)
        large_font = ImageFont.truetype(font_to_use, font_size)
        
        # Split text into lines and wrap long lines
        lines = []
        for line in text.split('\n'):
            words = line.split()
            if not words:
                continue
            current_line = words[0]
            for word in words[1:]:
                test_line = current_line + " " + word
                line_width = draw.textbbox((0, 0), test_line, font=large_font)[2] - draw.textbbox((0, 0), test_line, font=large_font)[0]
                if line_width <= width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            lines.append(current_line)
        
        # Calculate total height of all lines
        line_heights = [draw.textbbox((0, 0), line, font=large_font)[3] - draw.textbbox((0, 0), line, font=large_font)[1] for line in lines]
        total_height = sum(line_heights)
        
        # Calculate starting y position to center all lines vertically
        y = (height - total_height) / 2
        
        # Draw each line centered horizontally
        for i, line in enumerate(lines):
            line_width = draw.textbbox((0, 0), line, font=large_font)[2] - draw.textbbox((0, 0), line, font=large_font)[0]
            x = (width - line_width) / 2
            draw.text((x, y), line, font=large_font, fill="black")
            y += line_heights[i]
        
        # Save the image
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        image_path = os.path.join(folder_name, filename)
        image.save(image_path)
    
    def merge_images_horizontally(self, images_folder: str, image1_path: str, image2_path: str, output_filename: str) -> bool:
        """Merge two images horizontally."""
        if not os.path.exists(images_folder):
            print(f"Error: Folder '{images_folder}' does not exist.")
            return False
        
        if not os.path.isfile(os.path.join(images_folder, image1_path)):
            print(f"Error: File '{image1_path}' does not exist in '{images_folder}'.")
            return False
        if not os.path.isfile(os.path.join(images_folder, image2_path)):
            print(f"Error: File '{image2_path}' does not exist in '{images_folder}'.")
            return False
        
        # Open images
        img1 = Image.open(os.path.join(images_folder, image1_path))
        img2 = Image.open(os.path.join(images_folder, image2_path))
        
        # Get heights
        height1 = img1.height
        height2 = img2.height
        max_height = max(height1, height2)
        
        # Create new image
        new_img = Image.new('RGB', (img1.width + img2.width, max_height))
        
        # Paste images
        new_img.paste(img1, (0, 0))
        new_img.paste(img2, (img1.width, 0))
        
        # Save merged image
        output_path = os.path.join(images_folder, output_filename)
        new_img.save(output_path)
        
        print(f"Merged image saved as {output_path}")
        return True 