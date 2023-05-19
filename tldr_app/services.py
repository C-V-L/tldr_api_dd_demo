import os
from decouple import config
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from .models import *
import json


class QueryGPT():	
  os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')
  def initiate_query(query):
    query_to_file(query)
    query_engine = create_query_engine()
    responses = []
    json_string = """
      {
				"title": "areas_of_focus"
        "impact": "key information about how this terms of service would effect me in regards to this area_of_focus.",
        "actionable": "any steps outlined in the terms of service how I, as the consumer can take to protect myself in regards to this area_of_focus.",
        "ranking": "On a scale of 1 to 10, with 1 being the most business friendly and 10 being the most consumer friendly, how does this terms of service compare on the issue of this area_of_focus with that of the industry standard. Do not include complete sentences such as 'on a scale of 1 to 10, this is a 7.' in that case, just respond 7. You need to be succinct."
      }
     """
    for area_of_focus in query.areas_of_focus:
      response = query_engine.query(f"I am providing you the terms and services of a company. You are instructed to read these terms of service and to respond to the query I have in regard to the terms of service. My query is: How does this terms of service address {area_of_focus}. Please respond with the information in the format of a json string like this: {json_string} where the key 'area_of_focus' is {area_of_focus}. Please make sure that the formatting of the json string is correct and there are no additional single or double quotes other than what a json string would require")
      result = Result(response=json.loads(str(response)), query=query)
      result.save()
      responses.append(result)
    return responses

def query_to_file(query):
  file = open('data/tos.txt', 'w')
  file.write(query.tos)
  file.close()
  
def create_query_engine():
    documents = SimpleDirectoryReader('data').load_data()
    index = GPTVectorStoreIndex.from_documents(documents=documents)
    query_engine = index.as_query_engine()
    return query_engine