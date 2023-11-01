from typing_extensions import Required
from kor.nodes import Object, Text
from langchain.prompts import PromptTemplate
from kor import create_extraction_chain
from typing import Optional


def generate_llm_schema(schema_name: str) -> Object:
    if schema_name == "alteryx_notes":
        ayx_notes_schema = Object(
            id="update",
            # description="Information about specific feature update mentioned inside the text",
            attributes=[
                Text(
                    id="Feature",
                    description="Name of feature that has been updated.",
                ),
                Text(
                    id="Summary",
                    description="Short summary of the update.",
                ),
                Text(
                    id="Tags",
                    description="List of features mentioned inside the text separated by ',' separator.",
                ),
                Text(
                    id="Deprecations",
                    description="List of no longer supported features mentioned inside the text separated by ',' separator.",
                )
            ],
            examples=[
                ("We have deprecated these connectors: Dynamics CRM Input and Output, Google Sheets Input and Output, Salesforce Wave Output. For more information, go to Data Sources or visit the Community article.",
                    [
                        {
                            "Feature": "Deprecation of connectors",
                            "Summary": "We have deprecated these connectors: Dynamics CRM Input and Output, Google Sheets Input and Output, Salesforce Wave Output.",
                            "Tags": "",
                            "Deprecations": "Dynamics CRM Input and Output, Google Sheets Input and Output, Salesforce Wave Output"
                        },
                    ]
                 ),
                (
                    "Alteryx Designer version 2023.1 offers separate GA and FIPS 140-2 capable products. For more information about FIPS, go to the NIST FIPS FAQ page.",
                    [
                        {
                            "Feature": "Alteryx Designer version 2023.1",
                            "Summary": "Alteryx Designer version 2023.1 offers separate GA and FIPS 140-2 capable products.",
                            "Tags": "Alteryx Designer",
                            "Deprecations": ""
                        },
                    ]
                ),
                (
                    "The 2023.1 release brings Okta authentication support, single sign-on (SSO), for SAP Hana. You can now authenticate to SAP Hana Cloud with Okta accounts from Alteryx Designer.",
                    [
                        {
                            "Feature": "Okta authentication support for SAP Hana",
                            "Summary": "You can now authenticate to SAP Hana Cloud with Okta accounts.",
                            "Tags": "Alteryx Designer",
                            "Deprecations": ""
                        },
                    ]
                ),
                (
                    "We've made a change to the Alteryx Intelligence Suite (2023.1) installer due to a compiling issue in Build 2023.1.17039. Please download and reinstall the latest Alteryx Intelligence Suite Build 2023.1.0.17033 from the license portal.",
                    [
                        {
                            "Feature": "Alteryx Intelligence Suite",
                            "Summary": "We've made a change to the Alteryx Intelligence Suite (2023.1) installer due to a compiling issue in Build 2023.1.17039.",
                            "Tags": "Alteryx Intelligence Suite"
                        },
                    ]
                ),
                (
                    "Cloud Execution for Desktop is now available for Designer version 2023.1 (included in the 2023.1.1.200 Patch 1 release). Schedule and run your Designer Desktop-built workflows in the cloud. Cloud Execution for Desktop lets you link your Alteryx Designer Desktop instance to an Alteryx Analytics Cloud Platform (AACP) workspace and then save your desktop-built workflows to the AACP library (which belongs to your AACP workspace). Once saved to the library, you can navigate to AACP and schedule those workflows to run.",
                    [
                        {
                            "Feature": "Cloud Execution for Desktop",
                            "Summary": "Cloud Execution for Desktop is now available for Designer version 2023.1 (included in the 2023.1.1.200 Patch 1 release). Schedule and run your Designer Desktop-built workflows in the cloud. Cloud Execution for Desktop lets you link your Alteryx Designer Desktop instance to an Alteryx Analytics Cloud Platform (AACP) workspace and then save your desktop-built workflows to the AACP library (which belongs to your AACP workspace). Once saved to the library, you can navigate to AACP and schedule those workflows to run.",
                            "Tags": "Alteryx Analytics Cloud Platform (AACP)"
                        },
                    ]
                ),
            ],
            many=False,
        )
        return ayx_notes_schema
    else:
        raise Exception("Schema does not exist.")


instruction_template = PromptTemplate(
    input_variables=["format_instructions", "type_description"],
    template=(
        "Your goal is to extract structured information from the user's input that matches the form described below. You must return response in the following format. When extracting information please make sure it matches the type information exactly. Do not add any attributes that do not appear in the schema shown below.""\n\n"
        "You are provided with a suggested feature name that user's input is about. You can use this suggestion to better understand what the text is about, however you need to make your own judgement on whether suggested feature name is accurate. The suggested feature name is marked with <> separator.\n\n."
        "{type_description}\n\n"
        "{format_instructions}\n"
    ),
)


class Extraction_Chain():
    def __init__(self, chain_name: str, llm: object) -> None:
        self.name = chain_name
        self.llm = llm
        self.encoder = "csv"
        self.insturctions_template = instruction_template

    def run(self, schema: object, prompt_text: str) -> None:
        chain = create_extraction_chain(
            llm=self.llm,
            node=schema,
            encoder_or_encoder_class=self.encoder,
            instruction_template=instruction_template
        )
        response = chain.run(prompt_text)["data"]
        return response

    def preview(self, schema: object, prompt_text: str) -> str:
        chain = create_extraction_chain(
            llm=self.llm,
            node=schema,
            encoder_or_encoder_class=self.encoder,
            instruction_template=instruction_template
        )
        return chain.prompt.format_prompt(text=prompt_text).to_string()
