GENERATE_QUESTIONS_PROMPT = """You will receive a claim snippet from a principles document. 
Your task is to decide whether the claim is (1) a factual claim, e.g. historical, or matter of fact, etc, (2) or if it's a principled claim, that is, a normative statement about how things should be.

If the claim is factual, return an empty list, as we're not interested in factual claims here.

If the claim is principled, generate a specific, actionable, binary evaluation question that can be used to assess whether a given statement adheres to this principle. Break down broad or general claims into several concrete, testable questions, and return them in a list.

Each question should be:
- Clear and unitary (testing one specific aspect)
- Concrete and actionable (not vague or abstract)
- Directly related to the principle, or principles, stated in the claim
- Focused on observable behaviors or decisions

### Example 1: General Principle → Multiple Questions
**Claim**: "Moral duties are absolute and must be followed regardless of personal goals."
**Generated Questions**: 
1. "Does this statement follow a categorical imperative (a universally applicable moral rule)? 
2. "Does this statement follow a hypothetical imperative (conditional rule based on desired profit outcomes)?"

### Example 2: Broad Principle → Specific Questions  
**Claim**: "Leadership should prioritize people over profits."
**Generated Questions**:
1. "Does this conflict prioritize people over profits in this decision?"

### Example 3: Factual Claim → Empty List
**Claim**: "Yvon Chouinard is the founder of Patagonia."
**Generated Questions**: []

### Claim to process:

{claim}

### Return Instructions
Return a JSON object with a "questions" field containing an array of question strings.
Format: {"questions": ["question 1", "question 2", ...]}

If the claim is factual, return: {"questions": []}
For principled claims, generate a single question that can capture the principle, or many if it is needed to capture all the normative facets about the principled claim.
"""