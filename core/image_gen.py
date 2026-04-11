"""Generate images from text prompts using Pollinations.ai (free, no API key)."""
import re
import urllib.parse


def parse_prompts(media_text: str) -> list[str]:
    """Extract image prompts from media agent output."""
    # Strip all markdown formatting first
    text = re.sub(r"\*\*", "", media_text)
    text = re.sub(r"--ar \d+:\d+", "", text)
    text = re.sub(r"--style \w+", "", text)

    prompts = []
    for line in text.strip().split("\n"):
        # Remove numbering like "1." or "1)" or "Scene 1:"
        cleaned = re.sub(r"^\d+[\.\)]\s*", "", line.strip())
        cleaned = re.sub(r"^Scene \d+:\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = cleaned.strip()

        # Skip empty, short, or header lines
        if not cleaned or len(cleaned) < 20:
            continue
        if cleaned.startswith("#") or cleaned.upper() == cleaned:
            continue

        prompts.append(cleaned)

    return prompts[:4]


def shorten_prompt(prompt: str, max_chars: int = 200) -> str:
    """Shorten a long prompt to work with Pollinations URL limits."""
    prompt = prompt.rstrip(",.;:!? ")

    if len(prompt) <= max_chars:
        return prompt

    first_sentence = prompt.split(". ")[0]
    if len(first_sentence) <= max_chars:
        return first_sentence.rstrip(",.;:!? ")

    return prompt[:max_chars].rsplit(" ", 1)[0].rstrip(",.;:!? ")


def generate_images(prompts: list[str]) -> list[str]:
    """Build Pollinations.ai image URLs from prompts."""
    image_urls = []

    for prompt in prompts[:4]:
        short = shorten_prompt(prompt)
        encoded = urllib.parse.quote(short)
        seed = hash(short) % 100000
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=768&height=768&nologo=true&seed={seed}"
        image_urls.append(url)

    return image_urls
