from core.llm import call_claude

def run_strategist(input_data, insights=None):

    product = input_data["product"]
    audience = input_data["audience"]
    platform = input_data["platform"]
    goal = input_data["goal"]

    insights_block = ""
    if insights:
        insights_block = f"""
INSIGHTS FROM PAST HIGH-PERFORMING ADS:
{insights}

Use these insights to inform your strategy.

"""

    prompt = f"""
You are a senior marketing strategist.

Return ONLY valid JSON.

EXAMPLE OUTPUT:
{{
  "hook": "You've been applying lip tint wrong",
  "angle": "beauty mistake curiosity hook",
  "positioning": "viral Gen Z beauty product"
}}

{insights_block}REAL INPUT:
Product: {product}
Audience: {audience}
Platform: {platform}
Goal: {goal}

Return ONLY JSON.
"""

    return call_claude(prompt)
