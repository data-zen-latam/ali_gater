import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from ragas.metrics._factual_correctness import FactualCorrectness
from unstructured.partition.auto import partition

from ali_gater.utils import claims_to_question_llm, evaluator_llm

load_dotenv()


class Gater:
    """
    A lightweight principle driven checker.
    """

    def __init__(self, principles_source: str):
        self.principles_source = principles_source

    def _source_to_text(self) -> str:
        if urlparse(self.principles_source).scheme in ('http', 'https'):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.principles_source, headers=headers)
            response.raise_for_status()
            return response.text
        elif os.path.isfile(self.principles_source):
            elements = partition(filename=self.principles_source)
            return "\n".join([str(el) for el in elements])
        else:
            raise ValueError("The principles source must be a valid URL or a file path.")

    async def extract_claims(self) -> list[str]:
        """
        Extract claims from the given text using the claims_to_question_llm.
        """
        scorer = FactualCorrectness(llm=evaluator_llm, atomicity="high", coverage="high")
        prompt = f"Extract the main claims from the following text:\n\n{text}\n\nList the claims as bullet points."
        response = await claims_to_question_llm.apredict(prompt)
        claims = response.split("\n")
        return [claim.strip("- ").strip() for claim in claims if claim.strip()]


