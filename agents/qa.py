from core.llm import call_claude

def run_qa(input_data):
    content = input_data["content"]

    prompt = f"""
You are a strict ad quality evaluator.

Evaluate this ad and give:
- Score (1-10)
- Improvements

Content:
{content}
"""

    return call_claude(prompt)