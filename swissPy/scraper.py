import re
import json
import uvloop
import asyncio
import aiohttp

from pathlib import Path
from bs4.element import Tag
from datetime import datetime
from collections import ChainMap
from bs4 import BeautifulSoup, SoupStrainer
from pylatexenc.latex2text import LatexNodes2Text

PROBLEMS = 'https://projecteuler.net/problem=%d'
NUM_PROBLEMS = 667
TRANSLATE = LatexNodes2Text()
INFO = re.compile(r'Published on (\w+, .* (?:am|pm)); Solved by (\d+);Difficulty rating: (\d+%)')


async def _fetch_problem(url, session):
    async with session.get(url) as response:
        return await response.text()


async def _fetch_problems(url):
    def task_builder():
        for i in range(1, NUM_PROBLEMS + 1):
            yield asyncio.ensure_future(_fetch_problem(url % i, session))

    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*task_builder(), return_exceptions=True)


def _parse_problem(html):
    container = BeautifulSoup(html, 'html.parser')

    title = container.find('h2').get_text().strip()
    id_ = container.find('h3').get_text().strip()

    content = container.find(class_='problem_content').get_text().strip()
    content = TRANSLATE.latex_to_text(content)

    info = container.find('span', class_='info').get_text().strip()
    pub_date, solved_by, diff_rate = INFO.match(info).groups()

    return {
        'title': title,
        'id': id_,
        'content': content,
        'pub_date': pub_date,
        'solved_by': solved_by,
        'diff_rate': diff_rate
    }


def fetch_problems():
    uvloop.install()
    for page in asyncio.run(_fetch_problems(PROBLEMS)):
        yield _parse_problem(page)


if __name__ == "__main__":
    problems_path = Path(__file__).parent / 'jsons'

    problems = {
        'data': list(fetch_problems()),
        'date': datetime.now().isoformat(),
        'num_problems': NUM_PROBLEMS,
        'url': PROBLEMS  
    }
    with open(problems_path / 'solutions.json', 'r') as f:
        solutions = ChainMap(*json.load(f))

    for problem in problems['data']:
        id_ = problem['id'].replace('Problem ', '')
        problem['solution'] = solutions.get(id_, None)

    with open('problems.json', 'w') as f:
        json.dump(problems, f)