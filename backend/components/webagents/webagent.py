from pyppeteer import launch
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
from .webagent_models import Agent, Config
import json
import asyncio


def to_markdown(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)


async def scrape_pages(url: str, release: str) -> None:
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url, timeout=100000)
    page = await page.content()
    await browser.close()
    soup = BeautifulSoup(page, "html.parser")
    body = soup.find("body")
    content = to_markdown(soup=body)
    notes = open(f"raw_notes/alteryx/release_notes_text_{release}.txt", "w")
    notes.write(content)
    print(f'Added release notes for {release} release')


class Web_Agent:
    def __init__(self, name: str) -> None:
        self.agent_name = name
        self.locations = None
        self.meta = None

    def initialise(self):
        # Initialising agent and loading data from config.json file.
        raw_agents = open("./components/webagents/config.json", "r").read()
        agents = json.loads(raw_agents)['agents']
        try:
            agent = Agent(**agents[self.agent_name])
            self.locations = agent.locations
            self.meta = agent.meta
            print(f"Initialised {self.agent_name} agent")
        except:
            raise Exception("Agent not found. Check available agents.")

    def get_data(self):
        alteryx_pages = self.locations
        for each in range(0, len(alteryx_pages)):
            page = alteryx_pages[each]
            asyncio.get_event_loop().run_until_complete(
                scrape_pages(url=page.url, release=page.meta)
            )


# config = Config(
#     agent_name="alteryx"
# )

# agent = Web_Agent(name=config.agent_name)
# agent.initialise()
# agent.get_data()
