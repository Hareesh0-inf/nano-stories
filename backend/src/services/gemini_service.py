import os
from dotenv import load_dotenv
from typing import Optional, List
from google import genai
from google.genai import types
import uuid
from pathlib import Path
import base64
from io import BytesIO
from PIL import Image

class GeminiService:
    """Service for handling Gemini API interactions for image generation"""

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        print(f"🔍 Gemini Service: API key loaded, length: {len(self.api_key) if self.api_key else 0}")
        if not self.api_key or self.api_key == "your_actual_google_api_key_here" or len(self.api_key.strip()) < 20:
            print("⚠️  Gemini Service: Using mock mode (invalid API key)")
            self.client = None
            self.model = "gemini-2.0-flash-exp"
        else:
            try:
                self.client = genai.Client(api_key=self.api_key)
                self.model = "gemini-2.0-flash-exp"
                print("✅ Gemini Service: Client initialized successfully")
            except Exception as e:
                print(f"❌ Gemini Service: Failed to initialize client: {e}")
                self.client = None

        # Ensure uploads directories exist
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure all necessary directories exist"""
        directories = [
            "uploads/characters",
            "uploads/products",
            "uploads/backgrounds",
            "uploads/final",
            "uploads/mock-images"
        ]
        for dir_path in directories:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

    def _save_image_locally(self, image_data: bytes, image_type: str, filename: str = None) -> str:
        """
        Save image data locally and return the URL

        Args:
            image_data: Binary image data
            image_type: Type of image ('character', 'product', 'background', 'final')
            filename: Optional filename, will generate UUID if not provided

        Returns:
            Local URL path to the saved image
        """
        if filename is None:
            filename = f"{uuid.uuid4()}.png"

        # Ensure filename has extension
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            filename += '.png'

        # Create directory path
        dir_path = f"uploads/{image_type}s"
        if image_type == "final":
            dir_path = "uploads/final"  # Use "final" without 's' for consistency
        Path(dir_path).mkdir(parents=True, exist_ok=True)

        # Full file path
        file_path = Path(dir_path) / filename

        # Save image
        with open(file_path, "wb") as f:
            f.write(image_data)

        # Return URL path
        url_path = f"/uploads/{image_type}s/{filename}"
        if image_type == "final":
            url_path = f"/uploads/final/{filename}"  # Use "final" without 's' for consistency
        return url_path

    def generate_character_image(self, details: str, personality: str) -> Optional[str]:
        """
        Generate a character image based on details and personality

        Args:
            details: Character description
            personality: Character personality traits

        Returns:
            URL of generated image or None if failed
        """
        # Check if we have a valid API key
        if not self.api_key or self.api_key == "your_actual_google_api_key_here":
            print("ℹ️  Using mock image generation (no valid API key configured)")
            # Return a mock image URL for testing purposes
            return "/uploads/mock-images/placeholder.png"

        prompt = f"Create a photorealistic image of a character: {details}. Personality: {personality}. Professional appearance suitable for brand storytelling."

        try:
            # Generate image with Gemini
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['Text', 'Image']
                )
            )

            # Extract and save the generated image
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    # Convert inline data to bytes
                    image_data = part.inline_data.data

                    # Save locally and return URL
                    filename = f"character_{uuid.uuid4()}.png"
                    local_url = self._save_image_locally(image_data, "character", filename)
                    print(f"✅ Character image saved locally: {local_url}")
                    return local_url

            # If no image data found, return placeholder
            print("⚠️  No image data in response, using placeholder")
            return "/uploads/mock-images/placeholder.png"

        except Exception as e:
            print(f"Error generating character image: {e}")
            return "/uploads/mock-images/placeholder.png"

    def generate_product_image(self, name: str, description: str) -> Optional[str]:
        """
        Generate a product image based on name and description

        Args:
            name: Product name
            description: Product description

        Returns:
            URL of generated image or None if failed
        """
        # Check if we have a valid API key
        if not self.api_key or self.api_key == "your_actual_google_api_key_here" or len(self.api_key.strip()) < 20 or self.client is None:
            print("ℹ️  Using mock product image generation (no valid API key or client)")
            # Return a mock image URL for testing purposes
            return f"/uploads/mock-images/placeholder.png"

        prompt = f"Create a photorealistic image of the product: {name}. Description: {description}. High-quality product photography suitable for brand storytelling."

        try:
            # Generate image with Gemini
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['Text', 'Image']
                )
            )

            # Extract and save the generated image
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    # Convert inline data to bytes
                    image_data = part.inline_data.data

                    # Save locally and return URL
                    filename = f"product_{uuid.uuid4()}.png"
                    local_url = self._save_image_locally(image_data, "product", filename)
                    print(f"✅ Product image saved locally: {local_url}")
                    return local_url

            # If no image data found, return placeholder
            print("⚠️  No image data in response, using placeholder")
            return "/uploads/mock-images/placeholder.png"

        except Exception as e:
            print(f"Error generating product image: {e}")
            return "/uploads/mock-images/placeholder.png"

    def generate_background_image(self, scene_details: str, lighting: str) -> Optional[str]:
        """
        Generate a background image based on scene and lighting details

        Args:
            scene_details: Description of the scene
            lighting: Lighting conditions

        Returns:
            URL of generated image or None if failed
        """
        # Check if we have a valid API key
        if not self.api_key or self.api_key == "your_actual_google_api_key_here" or len(self.api_key.strip()) < 20 or self.client is None:
            print("ℹ️  Using mock background image generation (no valid API key or client)")
            # Return a mock image URL for testing purposes
            return "/'upload's/mock-images/placeholder.png"

        prompt = f"Create a photorealistic background image: {scene_details}. Lighting: {lighting}. Suitable for brand storytelling and professional presentation."

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['Text', 'Image']
                )
            )

            # Extract and save the generated image
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    # Convert inline data to bytes
                    image_data = part.inline_data.data

                    # Save locally and return URL
                    filename = f"background_{uuid.uuid4()}.png"
                    local_url = self._save_image_locally(image_data, "background", filename)
                    print(f"✅ Background image saved locally: {local_url}")
                    return local_url

            # If no image data found, return placeholder
            print("⚠️  No image data in response, using placeholder")
            return "/uploads/mock-images/placeholder.png"

        except Exception as e:
            print(f"Error generating background image: {e}")
            return "/uploads/mock-images/placeholder.png"

    def generate_final_images(self, character_image_data: bytes, product_image_data: bytes,
                            background_image_data: bytes, story: str) -> List[dict]:
        """
        Generate final brand storytelling images by fusing character, product, and background images with story

        Args:
            character_image_data: Binary data of generated character image
            product_image_data: Binary data of uploaded product image
            background_image_data: Binary data of generated background image
            story: Brand story narrative

        Returns:
            List of dicts with fused image URLs and prompts
        """
        # Check if we're using mock data
        is_mock_data = (
            character_image_data == b"mock_character_image_data" or
            product_image_data == b"mock_product_image_data" or
            background_image_data == b"mock_background_image_data" or
            character_image_data in [b"mock_char", b"mock_character"] or
            product_image_data in [b"mock_prod", b"mock_product"] or
            background_image_data in [b"mock_bg", b"mock_background"]
        )

        images = []

        # Real image fusion code (currently unreachable due to early return above)
        try:
            character_img = Image.open(BytesIO(character_image_data))
            product_img = Image.open(BytesIO(product_image_data))
            background_img = Image.open(BytesIO(background_image_data))
        except Exception as e:
            print(f"Error loading images for fusion: {e}")
            return []

        # Create 3 variations with different fusion approaches
        fusion_styles = [
            "seamlessly integrated composition",
            "dramatic storytelling scene",
            "professional brand presentation"
        ]

        for i, style in enumerate(fusion_styles, 1):
            prompt = f"""Create a compelling brand storytelling image by fusing these elements:

Story: {story}

Fusion Style: {style}

Combine the character, product, and background into a single, cohesive image that tells the brand story. Ensure all elements are harmoniously integrated and the composition supports the narrative effectively."""

            try:
                # Use Gemini's multi-image fusion capability
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=[
                        prompt,
                        character_img,
                        product_img,
                        background_img
                    ],
                    config=types.GenerateContentConfig(
                        response_modalities=['Text', 'Image']
                    )
                )

                # Extract and save the fused image
                for part in response.candidates[0].content.parts:
                    if part.inline_data:
                        # Convert inline data to bytes
                        image_data = part.inline_data.data

                        # Save locally and return URL
                        filename = f"final_{uuid.uuid4()}.png"
                        local_url = self._save_image_locally(image_data, "final", filename)
                        print(f"✅ Final fused image saved locally: {local_url}")

                        images.append({
                            "id": f"fused_img_{i}",
                            "prompt": prompt,
                            "image_url": local_url,
                            "fusion_style": style
                        })
                        break

            except Exception as e:
                print(f"Error generating fused image {i}: {e}")
                # Add placeholder for failed fusion
                images.append({
                    "id": f"fused_img_{i}",
                    "prompt": prompt,
                    "image_url": "/uploads/mock-images/placeholder.png",
                    "fusion_style": style,
                    "error": str(e)
                })

        return images

    def _extract_image_url(self, response) -> Optional[str]:
        """
        Extract image URL from Gemini API response

        Args:
            response: Gemini API response

        Returns:
            Image URL or None
        """
        try:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    # In production, upload to cloud storage and return public URL
                    # For now, return a placeholder filename
                    return f"generated_image_{hash(str(part.inline_data.data))}.png"
        except Exception as e:
            print(f"Error extracting image URL: {e}")

        return None
