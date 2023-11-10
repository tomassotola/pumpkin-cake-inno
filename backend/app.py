import dotenv
from utils import preprocess_prompt, get_splits
from langchain.chat_models import ChatOpenAI
from components.llms.llms import Extraction_Chain, generate_llm_schema
from components.webagents.webagent import Web_Agent
from components.loaders.loaders import Data_Loader
from models import Config, Update
from elasticsearch import Elasticsearch


def initialize_llm() -> ChatOpenAI:
    # Initializing llm
    dotenv.load_dotenv()
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        max_tokens=2000,
    )
    return llm


def upload_to_es(updates: object) -> None:
    es = Elasticsearch(
        "http://localhost:9200",
        # ca_certs="http_ca.crt",
        # basic_auth=("elastic", ELASTIC_PASSWORD)
    )

    #upload index
    mappings = {
        "properties": {
        "Feature": { "type": "text" },
        "Summary": { "type": "text" },
        "Tags":{ "type": "keyword" },
        "Release":{ "type": "keyword" },
        "Product":{ "type": "keyword" },
        "Type":{ "type": "keyword" },
        "Deprecations":{ "type": "keyword" }
        }
    }

    if not es.indices.exists(index="alteryx_updates"):
        es.indices.create(index="alteryx_updates", mappings=mappings)

    for each in range(0, len(updates)):
        resp = es.index(index="alteryx_updates", document=updates[each])
        print(resp)


def process_data(config: Config):
    print("version " + config.version )

     # Loading data and splitting texts
    text_splits = get_splits(
        loader_name=config.loader_name,
        version=config.version
    )

    # Preparing chain
    llm = initialize_llm()
    llm_schema = generate_llm_schema(
        schema_name=config.schema_name
    )
    chain = Extraction_Chain(
        chain_name=config.chain_name,
        llm=llm
    )

    updates = []
    # text = preprocess_prompt(text_splits[0])
    # preview = chain.preview(
    #     schema=llm_schema,
    #     prompt_text=text
    # )
    # print(preview)
    for index, text_split in enumerate(text_splits):
        prompt_text = preprocess_prompt(text_split)
        print(f"requesting {index} split")
        response = chain.run(
            schema=llm_schema,
            prompt_text=prompt_text
        )
        parsed = Update(**response['update'][0])
        parsed.Release = config.version
        parsed.Product = config.product_name
        updates.append(parsed.model_dump_json())
        
    upload_to_es(updates=updates)


def scrape_data(config: Config):
    agent = Web_Agent(name=config.web_agent_name)
    agent.initialise()
    agent.get_data()


def app():
    versions = ["2020.1", "2020.2", "2020.3", "2020.4", "2021.1", "2021.2", "2021.3", "2021.4", "2022.1", "2022.3", "2023.1", "2023.2"]

    # 2020.4 not completed
    # Add full summary of the feature
    # Check 2020.2 last feature how it gets sent to OpenAI
    # Add url to release page
    config = Config(
        web_agent_name="alteryx",
        loader_name="alteryx",
        version="",
        schema_name="alteryx_notes",
        chain_name="alteryx",
        product_name="Alteryx"
    )
    # Scraping data
    # scrape_data(config=config)

    for version in versions:
        config.version = version
        process_data(config=config)


if __name__ == "__main__":
    app()
