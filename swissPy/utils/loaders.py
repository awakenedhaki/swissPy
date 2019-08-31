import json

from pathlib import Path
from typing import Dict, Uninon


def load_extensions() -> Dict[str, str]:
    '''
    Open and return extensions JSON
    '''
    EXTENSIONS: Path = Path(__file__).parents[1] / 'jsons' / 'extensions.json'
    with EXTENSIONS.open('r') as f:
        return json.load(f)


def load_problems() -> Dict[str, Union[Dict[str, str], str]]:
    '''
    Open and return problems JSON
    '''
    PROBLEMS: Path = Path(__file__).parents[1] / 'jsons' / 'problems.json'
    with PROBLEMS.open('r') as f:
        return json.load(f)


def load_template() -> Dict[str, str]:
    '''
    Open and return templates JSON.
    '''
    TEMPLATES: Path = Path(__file__).parents[1] / 'jsons' / 'templates.json'
    with TEMPLATES.open('r') as f:
        return json.load(f)
