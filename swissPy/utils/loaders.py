import json

from pathlib import Path


def load_extensions():
    EXTENSIONS = Path(__file__).parent / 'jsons' / 'extensions.json'
    with EXTENSIONS.open('r') as f:
        return json.load(f)


def load_problems():
    PROBLEMS = Path(__file__).parent / 'jsons' / 'problems.json'
    with PROBLEMS.open('r') as f:
        return json.load(f)


def load_template():
    TEMPLATES = Path(__file__).parent / 'jsons' / 'templates.json'
    with TEMPLATES.open('r') as f:
        return json.load(f)