import os
import pandas as pd 
from dotenv import load_dotenv

load_dotenv()

def main():
  hf_token = os.getenv("HF_TOKEN")
  os.environ["HF_TOKEN"] = hf_token
  model_id = "meta-llama/Llama-3.2-3B-Instruct"

  
if __name__ == "__main__":
  main()
