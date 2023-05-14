import os 
from decouple import config
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from .models import *

class QueryGPT():	
	def initiate_query(query):
		os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')
		file = open('data/tos.txt', 'w')
		file.write(query.tos)
		file.close()
		documents = SimpleDirectoryReader('data').load_data()
		index = GPTVectorStoreIndex.from_documents(documents=documents)
		query_engine = index.as_query_engine()
		# Possibly will want to make this an array that is iterated over... each item is a separate query to the ChatGPT database. 
		response = query_engine.query(f"I am providing you the terms and services of a company and I am seeking information about how this would apply to me. Here are the two areas of focus I am concerned about; they will be in an array format but they are two separate and distinct issues. Please provide me it in the following format. The focus then a colon and then any relevant bullet points on that issue. Please also include information on how I, as a consumer, can protect my interests and rights in these regards.{query.areas_of_focus}")
		return response