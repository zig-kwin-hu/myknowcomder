import transformers
import os
from transformers import TRANSFORMERS_CACHE
cache_path = os.getenv('TRANSFORMERS_CACHE', TRANSFORMERS_CACHE)
print(f"Huggingface cache path: {cache_path}")
model_name = "golaxy/KnowCoder-7B-base"

tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
model = transformers.AutoModel.from_pretrained(model_name)
