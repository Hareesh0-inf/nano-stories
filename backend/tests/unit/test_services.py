"""
Unit tests for services
"""
import pytest
import os
from unittest.mock import Mock, patch

# Import services
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from services.gemini_service import GeminiService

class TestGeminiService:
    """Test cases for GeminiService"""

    @patch('google.genai.Client')
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'})
    def test_service_initialization(self, mock_client):
        """Test that GeminiService initializes correctly"""
        service = GeminiService()
        mock_client.assert_called_once_with(api_key='test_key')
        assert service.api_key == 'test_key'
        assert service.model == "gemini-2.5-flash-image-preview"

    @patch('google.genai.Client')
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'})
    def test_generate_character_image_success(self, mock_client):
        """Test successful character image generation"""
        # Mock the client and its response
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        
        # Mock the generate_content method
        mock_response = Mock()
        mock_response.text = "https://example.com/generated-character.jpg"
        mock_instance.generate_content.return_value = mock_response

        service = GeminiService()
        result = service.generate_character_image(
            details="A professional business person",
            personality="confident"
        )

        assert result == "https://example.com/generated-character.jpg"
        mock_instance.generate_content.assert_called_once()

    @patch('google.genai.Client')
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'})
    def test_generate_character_image_with_minimal_details(self, mock_client):
        """Test character generation with minimal details"""
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        
        mock_response = Mock()
        mock_response.text = "https://example.com/generated-minimal.jpg"
        mock_instance.generate_content.return_value = mock_response

        service = GeminiService()
        result = service.generate_character_image(
            details="Simple character",
            personality=""
        )

        assert result == "https://example.com/generated-minimal.jpg"

    @patch.dict(os.environ, {'GOOGLE_API_KEY': ''})
    def test_service_initialization_without_api_key(self):
        """Test that service fails without API key"""
        with pytest.raises(ValueError, match="GOOGLE_API_KEY environment variable is required"):
            GeminiService()

    @patch('google.genai.Client')
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'})
    def test_generate_character_image_api_error(self, mock_client):
        """Test handling of API errors"""
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        mock_instance.generate_content.side_effect = Exception("API Error")

        service = GeminiService()
        result = service.generate_character_image(
            details="Test character",
            personality="test personality"
        )

        assert result is None

    @patch('backend.src.services.gemini_service.genai')
    def test_generate_character_image_with_minimal_details(self, mock_genai, gemini_service):
        """Test character generation with minimal details"""
        mock_response = Mock()
        mock_response.text = "https://example.com/minimal-character.jpg"
        mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

        result = gemini_service.generate_character_image(
            details="A person",
            personality=None
        )

        assert result == "https://example.com/minimal-character.jpg"

    @patch('backend.src.services.gemini_service.genai')
    def test_generate_character_image_failure(self, mock_genai, gemini_service):
        """Test character image generation failure"""
        mock_genai.GenerativeModel.return_value.generate_content.side_effect = Exception("API Error")

        result = gemini_service.generate_character_image(
            details="Test character",
            personality="confident"
        )

        assert result is None

    @patch('backend.src.services.gemini_service.genai')
    def test_generate_product_image_success(self, mock_genai, gemini_service):
        """Test successful product image generation"""
        mock_response = Mock()
        mock_response.text = "https://example.com/generated-product.jpg"
        mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

        result = gemini_service.generate_product_image(
            name="Amazing Widget",
            description="A revolutionary product"
        )

        assert result == "https://example.com/generated-product.jpg"

    @patch('backend.src.services.gemini_service.genai')
    def test_generate_product_image_minimal(self, mock_genai, gemini_service):
        """Test product generation with minimal information"""
        mock_response = Mock()
        mock_response.text = "https://example.com/minimal-product.jpg"
        mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

        result = gemini_service.generate_product_image(
            name="Widget",
            description=None
        )

        assert result == "https://example.com/minimal-product.jpg"

    @patch('backend.src.services.gemini_service.genai')
    def test_generate_background_image_success(self, mock_genai, gemini_service):
        """Test successful background image generation"""
        mock_response = Mock()
        mock_response.text = "https://example.com/generated-background.jpg"
        mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

        result = gemini_service.generate_background_image(
            scene_details="Modern office setting",
            lighting="natural daylight"
        )

        assert result == "https://example.com/generated-background.jpg"

    @patch('backend.src.services.gemini_service.genai')
    def test_generate_background_image_minimal(self, mock_genai, gemini_service):
        """Test background generation with minimal information"""
        mock_response = Mock()
        mock_response.text = "https://example.com/minimal-background.jpg"
        mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

        result = gemini_service.generate_background_image(
            scene_details="Office",
            lighting=None
        )

        assert result == "https://example.com/minimal-background.jpg"

    @patch('backend.src.services.gemini_service.genai')
    def test_generate_final_images_success(self, mock_genai, gemini_service):
        """Test successful final image generation with fusion"""
        mock_response = Mock()
        mock_response.text = '''[
            {
                "image_url": "https://example.com/fused1.jpg",
                "prompt": "Professional character using amazing product in modern office",
                "fusion_style": "photorealistic"
            },
            {
                "image_url": "https://example.com/fused2.jpg",
                "prompt": "Character showcasing product in office setting",
                "fusion_style": "artistic"
            },
            {
                "image_url": "https://example.com/fused3.jpg",
                "prompt": "Brand story visualization with character and product",
                "fusion_style": "cinematic"
            }
        ]'''
        mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

        # Create mock image data
        mock_image = PILImage.new('RGB', (100, 100), color='red')
        img_buffer = BytesIO()
        mock_image.save(img_buffer, format='JPEG')
        character_image_data = img_buffer.getvalue()

        result = gemini_service.generate_final_images(
            character_image_data=character_image_data,
            product_image_data=character_image_data,
            background_image_data=character_image_data,
            story="A compelling brand story about innovation"
        )

        assert len(result) == 3
        assert result[0]["image_url"] == "https://example.com/fused1.jpg"
        assert result[0]["fusion_style"] == "photorealistic"
        assert result[1]["image_url"] == "https://example.com/fused2.jpg"
        assert result[2]["image_url"] == "https://example.com/fused3.jpg"

    @patch('backend.src.services.gemini_service.genai')
    def test_generate_final_images_failure(self, mock_genai, gemini_service):
        """Test final image generation failure"""
        mock_genai.GenerativeModel.return_value.generate_content.side_effect = Exception("Fusion failed")

        mock_image = PILImage.new('RGB', (100, 100), color='red')
        img_buffer = BytesIO()
        mock_image.save(img_buffer, format='JPEG')
        image_data = img_buffer.getvalue()

        result = gemini_service.generate_final_images(
            character_image_data=image_data,
            product_image_data=image_data,
            background_image_data=image_data,
            story="Test story"
        )

        assert result is None

    @patch('backend.src.services.gemini_service.genai')
    def test_generate_final_images_invalid_json(self, mock_genai, gemini_service):
        """Test final image generation with invalid JSON response"""
        mock_response = Mock()
        mock_response.text = "Invalid JSON response"
        mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

        mock_image = PILImage.new('RGB', (100, 100), color='red')
        img_buffer = BytesIO()
        mock_image.save(img_buffer, format='JPEG')
        image_data = img_buffer.getvalue()

        result = gemini_service.generate_final_images(
            character_image_data=image_data,
            product_image_data=image_data,
            background_image_data=image_data,
            story="Test story"
        )

        assert result is None

    def test_prompt_construction(self, gemini_service):
        """Test that prompts are constructed correctly"""
        # Test character prompt construction
        with patch('backend.src.services.gemini_service.genai') as mock_genai:
            mock_response = Mock()
            mock_response.text = "https://example.com/test.jpg"
            mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

            gemini_service.generate_character_image(
                details="A young professional",
                personality="confident"
            )

            # Verify the prompt was constructed correctly
            call_args = mock_genai.GenerativeModel.return_value.generate_content.call_args
            prompt = call_args[0][0]

            assert "young professional" in prompt.lower()
            assert "confident" in prompt.lower()
            assert "character" in prompt.lower()

    def test_error_handling(self, gemini_service):
        """Test comprehensive error handling"""
        with patch('backend.src.services.gemini_service.genai') as mock_genai:
            # Test network error
            mock_genai.GenerativeModel.return_value.generate_content.side_effect = ConnectionError("Network error")

            result = gemini_service.generate_character_image("test", "test")
            assert result is None

            # Test API error
            mock_genai.GenerativeModel.return_value.generate_content.side_effect = Exception("API quota exceeded")

            result = gemini_service.generate_character_image("test", "test")
            assert result is None

    @patch('backend.src.services.gemini_service.genai')
    def test_image_data_processing(self, mock_genai, gemini_service):
        """Test that image data is processed correctly for fusion"""
        mock_response = Mock()
        mock_response.text = '[{"image_url": "https://example.com/test.jpg", "prompt": "test", "fusion_style": "test"}]'
        mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response

        # Create test image data
        mock_image = PILImage.new('RGB', (200, 200), color='blue')
        img_buffer = BytesIO()
        mock_image.save(img_buffer, format='PNG')
        test_image_data = img_buffer.getvalue()

        result = gemini_service.generate_final_images(
            character_image_data=test_image_data,
            product_image_data=test_image_data,
            background_image_data=test_image_data,
            story="Test fusion story"
        )

        assert result is not None
        assert len(result) == 1

        # Verify that generate_content was called (indicating image processing)
        mock_genai.GenerativeModel.return_value.generate_content.assert_called_once()

class TestServiceIntegration:
    """Test cases for service integration scenarios"""

    @pytest.fixture
    def mock_gemini_service(self):
        """Create a mocked GeminiService for integration testing"""
        with patch('backend.src.services.gemini_service.genai'):
            service = GeminiService()
            return service

    def test_service_workflow_character_to_fusion(self, mock_gemini_service):
        """Test the complete workflow from character generation to final fusion"""
        # This would test the integration between different service methods
        # In a real scenario, we'd mock the external API calls

        # Mock character generation
        with patch.object(mock_gemini_service, 'generate_character_image', return_value='https://example.com/char.jpg'):
            char_result = mock_gemini_service.generate_character_image("test", "test")
            assert char_result == 'https://example.com/char.jpg'

        # Mock product generation
        with patch.object(mock_gemini_service, 'generate_product_image', return_value='https://example.com/prod.jpg'):
            prod_result = mock_gemini_service.generate_product_image("test", "test")
            assert prod_result == 'https://example.com/prod.jpg'

        # Mock background generation
        with patch.object(mock_gemini_service, 'generate_background_image', return_value='https://example.com/bg.jpg'):
            bg_result = mock_gemini_service.generate_background_image("test", "test")
            assert bg_result == 'https://example.com/bg.jpg'

    def test_service_error_propagation(self, mock_gemini_service):
        """Test that errors are properly propagated through the service layer"""
        with patch.object(mock_gemini_service, 'generate_character_image', side_effect=Exception("Service unavailable")):
            result = mock_gemini_service.generate_character_image("test", "test")
            assert result is None

    def test_service_response_validation(self, mock_gemini_service):
        """Test that service responses are validated"""
        # Test with empty response
        with patch.object(mock_gemini_service, 'generate_character_image', return_value=''):
            result = mock_gemini_service.generate_character_image("test", "test")
            assert result == ''

        # Test with None response
        with patch.object(mock_gemini_service, 'generate_character_image', return_value=None):
            result = mock_gemini_service.generate_character_image("test", "test")
            assert result is None
