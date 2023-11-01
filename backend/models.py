from array import array
from pydantic import BaseModel, field_validator, Field
from typing import Optional


def extract_specific_tags(tags: array, products_to_check: array) -> array:
    tags_matched_products = []
    for product in range(0, len(products_to_check)):
        for tag in range(0, len(tags)):
            if products_to_check[product] in tags[tag]:
                tags_matched_products.append(tags[tag])
    return tags_matched_products


class Config(BaseModel):
    web_agent_name: str
    loader_name: str
    version: str
    schema_name: str
    chain_name: str
    product_name: str


class Update(BaseModel):
    Feature: str
    Summary: str
    Tags: Optional[list[str]]
    Release: str = Field(default="2021.2")
    Product: str = Field(default="Alteryx")
    Type: str = Field(default="New Feature")
    Deprecations: str

    @field_validator('Tags', mode="before")
    def transform_to_list(value: int) -> list:
        products_to_check = [
            "Alteryx Analytics Cloud", "Alteryx Intelligence Suite", "Designer Cloud", "Cloud Execution for Desktop"
        ]
        tags = value.split(",")
        matched_tags = extract_specific_tags(
            tags=tags, products_to_check=products_to_check)

        return matched_tags
