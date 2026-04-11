"""Generate images from text prompts using Replicate API (Flux Schnell)."""
import os
import re
import replicate
from dotenv import load_dotenv

load_dotenv()


def parse_prompts(media_text: str) -> list[str]:
    """Extract numbered prompts from media agent output."""
    lines = media_text.strip().split("\n")
    prompts = []
    for line in lines:
        cleaned = re.sub(r"^\d+[\.\)]\s*", "", line.strip())
        if cleaned and len(cleaned) > 10:
            prompts.append(cleaned)
    return prompts[:4]  # Max 4 images to stay within free tier


def generate_images(prompts: list[str]) -> list[str]:
    """Send prompts to Replicate Flux Schnell and return image URLs."""
    image_urls = []

    for prompt in prompts:
        try:
            output = replicate.run(
                "black-forest-labs/flux-schnell",
                input={
                    "prompt": prompt,
                    "num_outputs": 1,
                    "go_fast": True,
                },
            )
            # Output is a list of FileOutput objects with a .url attribute
            if output and len(output) > 0:
                url = str(output[0])
                image_urls.append(url)
        except Exception as e:
            print(f"Image generation failed for prompt: {e}")
            continue

    return image_urls
