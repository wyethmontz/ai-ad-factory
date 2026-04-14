import os
import re
import replicate
from dotenv import load_dotenv

load_dotenv()


def generate_images(media_prompts: str, max_images: int = 3) -> list[str]:
    """
    Takes the numbered media prompts from the media agent,
    extracts individual prompts, and generates images via Flux on Replicate.
    Returns a list of image URLs.
    """
    # Extract numbered prompts (e.g. "1. ...", "2. ...")
    lines = re.findall(r'\d+\.\s*(.+)', media_prompts)
    if not lines:
        # Fallback: split by newlines and take non-empty lines
        lines = [l.strip() for l in media_prompts.split('\n') if l.strip()]

    # Limit to max_images to control cost
    lines = lines[:max_images]

    image_urls = []
    for prompt in lines:
        try:
            output = replicate.run(
                "black-forest-labs/flux-schnell",
                input={
                    "prompt": prompt,
                    "num_outputs": 1,
                    "aspect_ratio": "1:1",
                    "output_format": "webp",
                    "output_quality": 80,
                }
            )
            # output is a list of FileOutput URLs
            if output:
                url = str(output[0])
                image_urls.append(url)
        except Exception as e:
            print(f"[IMAGE GEN ERROR] {e}")
            continue

    return image_urls
