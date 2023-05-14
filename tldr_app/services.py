import os 
from decouple import config
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from .models import *

class QueryGPT():	
	def initiate_query(query):
		os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')
		file = open('/Users/axeld/Documents/turing/4mod/projects/tldr_api/data/tos.txt', 'w')
		file.write(query)
		file.close()
		documents = SimpleDirectoryReader('data').load_data()
		index = GPTVectorStoreIndex.from_documents(documents=documents)
		query_engine = index.as_query_engine()
		response = query_engine.query("I am providing you the terms and services of a company and I am seeking information about how this would apply to me. Am I allowed to assign my rights under this agreement to anyone else without the other party's consent?")
		return response