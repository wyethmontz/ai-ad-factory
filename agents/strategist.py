from core.llm import call_claude

def run_strategist(input_data):

    product = input_data["product"]
    audience = input_data["audience"]
    platform = input_data["platform"]
    goal = input_data["goal"]

    prompt = f"""
You are a senior marketing strategist.

Return ONLY valid JSON.

EXAMPLE OUTPUT:
{{
  "hook": "You’ve been applying lip tint wrong",
  "angle": "beauty mistake curiosity hook",
  "positioning": "viral Gen Z beauty product"
}}

REAL INPUT:
Product: {product}
Audience: {audience}
Platform: {platform}
Goal: {goal}

Return ONLY JSON.
"""

    return call_claude(prompt)