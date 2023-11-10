# utility functions go here
from array import array
from markdownify import MarkdownConverter
from components.loaders.loaders import Data_Loader


def to_markdown(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)


def preprocess_prompt(text_split: object):
    page_content = text_split.page_content
    if 'Header 3' in text_split.metadata.keys():
        metadata = text_split.metadata['Header 3']
    else:
        metadata = "Update"
    prompt_text = "<>" + metadata + "<>" + page_content
    return prompt_text


def get_splits(loader_name: str, version: str) -> list:
    loader = Data_Loader(name=loader_name, version=version)
    loader.load()
    return loader.splits
