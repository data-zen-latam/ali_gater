# ali-gater

A principle-based evaluation framework that transforms principles into actionable assessment questions.

## Overview

ali-gater is a Python package that helps you evaluate company statements, communications, and documents against a set of defined principles. It works by:

1. **Breaking down principles** - Takes a principles text and extracts individual claims
2. **Generating evaluation questions** - Creates specific questions to assess each claim
3. **Evaluating statements** - Applies these questions to analyze company statements, policies, or other documents

Perfect for compliance checking, policy alignment, ethical assessment, or ensuring organizational communications align with stated values.

## Installation

```bash
pip install ali-gater
```

## Usage

```python
from ali_gater import Gater

# Initialize with your principles document
gater = Gater(principles_text="Your principles document here...")

# Extract claims from principles
claims = gater.extract_claims()

# Generate evaluation questions
questions = gater.generate_questions(claims)

# Evaluate a company statement
evaluation = gater.evaluate_statement(
    statement="Company statement to evaluate...",
    questions=questions
)
```

## Use Cases

- **Compliance Checking** - Verify if company policies align with regulatory principles
- **Values Assessment** - Evaluate if communications reflect stated organizational values
- **Ethical Review** - Check statements against ethical guidelines
- **Policy Alignment** - Ensure documents adhere to established principles

## Development

### Setup

This project uses `uv` for dependency management. First, install `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then, create a virtual environment and install dependencies:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src tests
ruff check src tests
```

### Type Checking

```bash
mypy src
```

## License

MIT
