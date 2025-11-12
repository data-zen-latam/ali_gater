import json
from pathlib import Path

from litellm.router import Router
from ragas.llms import llm_factory

# Get the config path - go up two levels from this file to reach the root
LITELLM_CONFIG_PATH = Path(__file__).parent.parent.parent / "litellm_config.json"

router = Router(model_list=json.load(open(LITELLM_CONFIG_PATH)), routing_strategy="least-busy")

# Use ragas llm_factory with the router - it will automatically detect and wrap LiteLLM
evaluator_llm = llm_factory(model="gpt-4.1-mini", client=router)

claims_to_question_llm = router

