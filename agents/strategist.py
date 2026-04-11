from core.llm import call_claude

def run_strategist(input_data):
    product = input_data["product"]
    audience = input_data["audience"]
    platform = input_data["platform"]
    goal = input_data["goal"]

    prompt = f"""
You are a marketing strategist.

Product: {product}
Audience: {audience}
Platform: {platform}
Goal: {goal}

Return:

Hook:
Angle:
Positioning:
"""

    return call_claude(prompt)