"""Tests for the Gater class and utilities."""

import tempfile
from pathlib import Path

import pytest
import requests
from ragas.metrics import AspectCritic

from ali_gater import Gater
from ali_gater.utils import evaluator_llm, router

# Test data
TEST_URL = "https://briandoddonleadership.com/2019/06/20/truett-cathys-6-legacy-principles-for-leading-chick-fil-a/"
TEST_PDF_URL = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"  # Public test PDF


@pytest.fixture
def temp_pdf():
    """Download a test PDF to a temporary file."""
    response = requests.get(TEST_PDF_URL)
    response.raise_for_status()

    with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False) as f:
        f.write(response.content)
        temp_path = f.name

    yield temp_path

    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


class TestGater:
    """Test suite for Gater class."""

    def test_load_text_from_url(self):
        """Test loading text from a URL."""
        gater = Gater(principles_source=TEST_URL)
        text = gater._source_to_text()

        assert len(text) > 0, "Should load text from URL"
        assert isinstance(text, str), "Text should be a string"
        print(f"\nLoaded {len(text)} characters from URL")
        print(f"First 200 chars: {text[:200]}...")

    def test_load_text_from_pdf(self, temp_pdf):
        """Test loading text from a PDF file."""
        gater = Gater(principles_source=temp_pdf)
        text = gater._source_to_text()

        assert len(text) > 0, "Should load text from PDF"
        assert isinstance(text, str), "Text should be a string"
        print(f"\nLoaded {len(text)} characters from PDF")
        print(f"First 200 chars: {text[:200]}...")

    def test_invalid_source(self):
        """Test that invalid source raises ValueError."""
        gater = Gater(principles_source="invalid_path_that_does_not_exist.txt")

        with pytest.raises(ValueError, match="must be a valid URL or a file path"):
            gater._source_to_text()

    def test_router_works(self):
        """Test the plain LiteLLM router from utils."""
        response = router.completion(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": "Say 'Hello from router!' in exactly 5 words."}]
        )

        assert response is not None, "Router should return a response"
        assert hasattr(response, 'choices'), "Response should have choices"
        assert len(response.choices) > 0, "Response should have at least one choice"
        print(f"\nRouter response: {response.choices[0].message.content}")

    def test_evaluator_llm_exists(self):
        """Test that evaluator_llm is properly initialized."""
        assert evaluator_llm is not None, "Evaluator LLM should be initialized"
        print(f"\nEvaluator LLM type: {type(evaluator_llm)}")

    def test_aspect_critic_with_evaluator_llm(self):
        """Test AspectCritic accepts evaluator_llm."""
        categorical_over_hypothetical = AspectCritic(
            name="categorical_over_hypothetical",
            definition="Does the response follow categorical imperatives (universally applicable moral rules regardless of personal goals) rather than hypothetical imperatives (conditional rules based on desired outcomes)?",
            llm=evaluator_llm,
        )

        assert categorical_over_hypothetical is not None, "AspectCritic should be created"
        assert categorical_over_hypothetical.name == "categorical_over_hypothetical"
        print(f"\nAspectCritic created: {categorical_over_hypothetical.name}")
