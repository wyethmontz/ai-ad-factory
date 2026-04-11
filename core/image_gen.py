"""Generate images from text prompts using Pollinations.ai (free, no API key)."""
import re
import urllib.parse


def parse_prompts(media_text: str) -> list[str]:
    """Extract numbered prompts from media agent output."""
    lines = media_text.strip().split("\n")
    prompts = []
    for line in lines:
        cleaned = re.sub(r"^\d+[\.\)]\s*", "", line.strip())
        # Skip short lines, headers, and markdown
        if cleaned and len(cleaned) > 10 and not cleaned.startswith("**") and not cleaned.startswith("#"):
            prompts.append(cleaned)
    return prompts[:4]  # Max 4 images


def shorten_prompt(prompt: str, max_chars: int = 200) -> str:
    """Shorten a long prompt to work with Pollinations URL limits."""
    # Remove markdown formatting
    prompt = re.sub(r"\*\*.*?\*\*", "", prompt)
    prompt = re.sub(r"--ar \d+:\d+", "", prompt)
    prompt = re.sub(r"--style \w+", "", prompt)
    prompt = prompt.strip()

    # Clean trailing punctuation
    prompt = prompt.rstrip(",.;:!? ")

    if len(prompt) <= max_chars:
        return prompt

    # Take the first sentence or first max_chars characters
    first_sentence = prompt.split(". ")[0]
    if len(first_sentence) <= max_chars:
        return first_sentence.rstrip(",.;:!? ")

    return prompt[:max_chars].rsplit(" ", 1)[0].rstrip(",.;:!? ")


def generate_images(prompts: list[str]) -> list[str]:
    """Build Pollinations.ai image URLs from prompts.

    Pollinations generates images on-the-fly from a URL.
    No API key, no signup, no cost.
    """
    # Pollinations allows only 1 concurrent request for anonymous users
    # Generate 1 hero image from the best prompt
    short = shorten_prompt(prompts[0])
    encoded = urllib.parse.quote(short)
    seed = hash(short) % 100000  # Consistent seed per prompt
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=768&height=768&nologo=true&seed={seed}"

    return [url]
