from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ConfigDict
from ragas.llms import LangchainLLMWrapper
from ali_gater.prompts import GENERATE_QUESTIONS_PROMPT

# Load environment variables
load_dotenv()

# Initialize OpenAI ChatGPT model with JSON mode
llm = ChatOpenAI(
    model="gpt-4o-mini",
    model_kwargs={"response_format": {"type": "json_object"}}
)

# Wrap for ragas evaluation metrics
evaluator_llm = LangchainLLMWrapper(llm)

# Agent for generating questions from claims
claims_to_question_agent = create_agent(
    model=llm,
    system_prompt=GENERATE_QUESTIONS_PROMPT,
)

# LLM for extracting claims (with JSON mode)
extract_claims_llm = ChatOpenAI(
    model="gpt-4o-mini",
    model_kwargs={"response_format": {"type": "json_object"}}
)