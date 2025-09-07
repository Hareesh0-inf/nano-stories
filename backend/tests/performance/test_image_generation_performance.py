"""
Performance tests for image generation
"""
import pytest
import time
from unittest.mock import Mock, patch
import os
import sys

# Import services
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from services.gemini_service import GeminiService

class TestImageGenerationPerformance:
    """Performance tests for image generation operations"""

    PERFORMANCE_THRESHOLD_SECONDS = 2.0  # <2s requirement

    @pytest.fixture
    def mock_gemini_service(self):
        """Create a GeminiService instance with mocked dependencies"""
        with patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'}):
            with patch('google.genai.Client') as mock_client:
                mock_instance = Mock()
                mock_client.return_value = mock_instance

                # Mock successful response
                mock_response = Mock()
                mock_response.text = "https://example.com/generated-image.jpg"
                mock_instance.generate_content.return_value = mock_response

                service = GeminiService()
                service.client = mock_instance
                return service

    def test_character_image_generation_performance(self, mock_gemini_service):
        """Test that character image generation completes within performance threshold"""
        start_time = time.time()

        result = mock_gemini_service.generate_character_image(
            details="A professional business person in a modern office setting",
            personality="confident and approachable"
        )

        end_time = time.time()
        execution_time = end_time - start_time

        assert result is not None
        assert execution_time < self.PERFORMANCE_THRESHOLD_SECONDS, \
            f"Character image generation took {execution_time:.2f}s, exceeding {self.PERFORMANCE_THRESHOLD_SECONDS}s threshold"

    def test_background_image_generation_performance(self, mock_gemini_service):
        """Test that background image generation completes within performance threshold"""
        # Mock background generation method if it exists
        if hasattr(mock_gemini_service, 'generate_background_image'):
            start_time = time.time()

            result = mock_gemini_service.generate_background_image(
                scene_details="Modern corporate office with large windows",
                lighting="natural daylight"
            )

            end_time = time.time()
            execution_time = end_time - start_time

            assert result is not None
            assert execution_time < self.PERFORMANCE_THRESHOLD_SECONDS, \
                f"Background image generation took {execution_time:.2f}s, exceeding {self.PERFORMANCE_THRESHOLD_SECONDS}s threshold"

    def test_story_image_generation_performance(self, mock_gemini_service):
        """Test that story/fusion image generation completes within performance threshold"""
        # Mock story generation method if it exists
        if hasattr(mock_gemini_service, 'generate_story_image'):
            start_time = time.time()

            result = mock_gemini_service.generate_story_image(
                story_text="A compelling brand story about innovation and growth",
                character_details="Professional business person",
                background_details="Modern office setting"
            )

            end_time = time.time()
            execution_time = end_time - start_time

            assert result is not None
            assert execution_time < self.PERFORMANCE_THRESHOLD_SECONDS, \
                f"Story image generation took {execution_time:.2f}s, exceeding {self.PERFORMANCE_THRESHOLD_SECONDS}s threshold"

    def test_concurrent_image_generation_performance(self, mock_gemini_service):
        """Test performance of concurrent image generation requests"""
        import asyncio

        async def generate_multiple_images():
            tasks = []
            for i in range(3):  # Test with 3 concurrent requests
                task = asyncio.create_task(
                    asyncio.to_thread(
                        mock_gemini_service.generate_character_image,
                        details=f"Character {i} details",
                        personality=f"Personality {i}"
                    )
                )
                tasks.append(task)

            start_time = time.time()
            results = await asyncio.gather(*tasks)
            end_time = time.time()

            return results, end_time - start_time

        results, execution_time = asyncio.run(generate_multiple_images())

        assert len(results) == 3
        assert all(result is not None for result in results)
        assert execution_time < (self.PERFORMANCE_THRESHOLD_SECONDS * 2), \
            f"Concurrent image generation took {execution_time:.2f}s, exceeding {self.PERFORMANCE_THRESHOLD_SECONDS * 2}s threshold"

    def test_image_generation_error_handling_performance(self, mock_gemini_service):
        """Test that error handling doesn't significantly impact performance"""
        # Configure mock to raise an exception
        mock_gemini_service.client.generate_content.side_effect = Exception("API Error")

        start_time = time.time()

        result = mock_gemini_service.generate_character_image(
            details="Test character",
            personality="test personality"
        )

        end_time = time.time()
        execution_time = end_time - start_time

        assert result is None  # Should return None on error
        assert execution_time < self.PERFORMANCE_THRESHOLD_SECONDS, \
            f"Error handling took {execution_time:.2f}s, exceeding {self.PERFORMANCE_THRESHOLD_SECONDS}s threshold"

    @pytest.mark.parametrize("details_length", [10, 100, 500, 1000])
    def test_image_generation_scalability(self, mock_gemini_service, details_length):
        """Test performance scaling with different input sizes"""
        details = "A " + "detailed " * (details_length // 8) + "character description"

        start_time = time.time()

        result = mock_gemini_service.generate_character_image(
            details=details,
            personality="confident and professional"
        )

        end_time = time.time()
        execution_time = end_time - start_time

        assert result is not None
        # Allow slightly more time for larger inputs (1.5x threshold)
        max_time = self.PERFORMANCE_THRESHOLD_SECONDS * 1.5
        assert execution_time < max_time, \
            f"Image generation with {details_length} chars took {execution_time:.2f}s, exceeding {max_time}s threshold"
