import os
import json
import logging
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

CHROMA_BASE_DIR = os.getenv("CHROMA_BASE_DIR", "data/chroma_db")
LAPTOPS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "laptops")


class LaptopsDB:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.chroma_base_dir = CHROMA_BASE_DIR
        self.laptops_dir = LAPTOPS_PATH
        
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")




def main():
    pass


if __name__ == "__main__":
    main()