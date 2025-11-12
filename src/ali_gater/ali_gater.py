import os
import asyncio
from urllib.parse import urlparse
import json

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from ragas.metrics._factual_correctness import FactualCorrectness
from unstructured.partition.auto import partition

from ali_gater.utils import claims_to_question_agent, extract_claims_llm

load_dotenv()


class Gater:
    """
    A lightweight principle driven checker.
    """

    def __init__(self, principles_source: str):
        self.principles_source = principles_source
        self.text = self._source_to_text()
        self.claims = []

    def _source_to_text(self) -> str:
        if urlparse(self.principles_source).scheme in ('http', 'https'):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.principles_source, headers=headers)
            response.raise_for_status()
            
            # Parse HTML and extract main content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script, style, nav, header, footer elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'iframe', 'noscript']):
                element.decompose()
            
            # Try to find main content area (common patterns)
            main_content = (
                soup.find('main') or 
                soup.find('article') or 
                soup.find('div', class_=['content', 'post-content', 'entry-content', 'article-content']) or
                soup.find('body')
            )
            
            # Extract text and clean up whitespace
            text = main_content.get_text(separator='\n', strip=True) if main_content else soup.get_text(separator='\n', strip=True)
            
            # Remove excessive blank lines
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            return '\n\n'.join(lines)
            
        elif os.path.isfile(self.principles_source):
            elements = partition(filename=self.principles_source)
            return "\n".join([str(el) for el in elements])
        else:
            raise ValueError("The principles source must be a valid URL or a file path.")

    async def extract_claims(self) -> None:
        """
        Extract claims from the given text using the claims_to_question_llm.
        """
        scorer = FactualCorrectness(llm=extract_claims_llm, atomicity="high", coverage="high") # type: ignore
        self.claims = await scorer.decompose_claims(self.text, callbacks=None)

        return None
    
    async def _generate_questions_from_claim(self, claim: str) -> list[str]:
        """
        Generate one or multiple evaluation questions from a single claim.
        Returns empty list if the claim is factual.
        """
        response = await claims_to_question_agent.ainvoke(
            {"messages": [{"role": "user", "content": claim}]}
        )
        
        # Extract the AIMessage from the response
        ai_message = response['messages'][-1]
        content = ai_message.content
        
        try:
            data = json.loads(content) if isinstance(content, str) else content
            
            # If it's an empty dict {} or has no questions, return empty list
            if not data or not data.get('questions'):
                return []
            
            return data['questions']
        except (json.JSONDecodeError, AttributeError, TypeError):
            # If parsing fails, return empty list
            return []
    
    async def generate_questions(self) -> list[str] | None:
        """
        Generate evaluation questions from the extracted claims using the claims_to_question_llm.
        Parallelized with asyncio for efficiency. Each claim may generate multiple questions.
        """
        # Get list of question lists from all claims in parallel
        question_lists = await asyncio.gather(*[self._generate_questions_from_claim(claim) for claim in self.claims])
        
        # Flatten the list of lists and filter out empty strings
        all_questions = [q for question_list in question_lists for q in question_list if len(q.strip()) > 0]
        return all_questions

    

    



