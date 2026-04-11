"""Generate images from text prompts using Pollinations.ai (free, no API key)."""
import re
import urllib.parse


def parse_prompts(media_text: str) -> list[str]:
    """Extract numbered prompts from media agent output."""
    lines = media_text.strip().split("\n")
    prompts = []
    for line in lines:
        cleaned = re.sub(r"^\d+[\.\)]\s*", "", line.strip())
        if cleaned and len(cleaned) > 10:
            prompts.append(cleaned)
    return prompts[:4]  # Max 4 images


def generate_images(prompts: list[str]) -> list[str]:
    """Build Pollinations.ai image URLs from prompts.

    Pollinations generates images on-the-fly from a URL.
    No API key, no signup, no cost.
    """
    image_urls = []

    for prompt in prompts:
        encoded = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=768&height=768&nologo=true"
        image_urls.append(url)

    return image_urls
