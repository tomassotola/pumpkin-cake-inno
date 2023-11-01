
from .loader_models import SchemaParser
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter
import json


def transform_elements(element: str) -> str:
    match element:
        case "Title":
            return "\n### "
        case "NarrativeText":
            return "\n"
        case "ListItem":
            return "\n* "
        case _:
            return "\n"


class Alteryx_Loader:
    def __init__(self, version: str) -> None:
        self.name = "alteryx"
        self.version = version
        self.schema = None
        self.md = None
        self.relevant_notes = None

    def __prepare_schema(self) -> None:
        # loadign specific schema by name
        raw_schemas = open(
            f"components/loaders/schemas.json", "r").read()
        all_schemas = json.loads(raw_schemas)['schemas']
        selected_schema = SchemaParser(**all_schemas[self.name])
        start_condition = selected_schema.start
        self.schema = SchemaParser(
            start=start_condition,
            end=selected_schema.end
        )

    def __load_raw_and_convert(self) -> None:
        # loading data and converts to unstructured
        raw_notes = UnstructuredMarkdownLoader(
            f"./raw_notes/{self.name}/release_notes_text_{self.version}.txt", mode="elements"
        )
        self.md = raw_notes.load()

    def __optimise_to_schema(self) -> None:
        start_index = 0
        end_index = 0
        start_condition_found = False
        end_condition_found = False
        start_condition = self.schema.start
        end_condition = self.schema.end

        for each in self.md:
            if start_condition in each.page_content and start_condition_found is False:
                # Finding relevant page element and adding +1 to trim the part of text inbetween
                start_index = self.md.index(each) + 1
                start_condition_found = True
            if end_condition in each.page_content and end_condition_found is False:
                end_index = self.md.index(each)
                end_condition_found = True
        # storing relevant notes inside the class
        self.relevant_notes = self.md[start_index:end_index]

    def load_and_optimise(self):
        self.__load_raw_and_convert()
        self.__prepare_schema()
        self.__optimise_to_schema()


class Data_Loader:
    def __init__(self, name: str, version: str = None) -> None:
        self.version = version
        self.name = name
        self.schema = None
        self.relevant_notes = None
        self.optimised_md = None
        self.splits = None

    def __load_data_for_version(self) -> None | str:
        # initilises specific loader and returns relevant notes
        if self.name == "alteryx":
            loader = Alteryx_Loader(self.version)
            loader.load_and_optimise()
            self.relevant_notes = loader.relevant_notes
        else:
            raise Exception("Loader not found")

    def __convert_to_md(self):
        # transforming categories used by unstructured back to markdown for splitting - we're using transform elements func
        # to ensure consistency in mapping categories
        formatted_items = [
            f"{transform_elements(item.metadata['category'])}{item.page_content}" for item in self.relevant_notes]
        joined_content = ("").join(formatted_items)
        self.optimised_md = joined_content

    def __prepare_splits(self):
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on
        )
        self.splits = markdown_splitter.split_text(self.optimised_md)

    def load(self):
        self.__load_data_for_version()
        self.__convert_to_md()
        self.__prepare_splits()


# loader = Data_Loader(name="alteryx", version="2023.1")
# loader.load()
# print(loader.splits[0])
# print(loader.splits[-1])
