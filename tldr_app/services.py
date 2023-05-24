import os
from decouple import config
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from .models import *
import json


class QueryGPT():	
  os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')
  def initiate_query(self, query):
    query_engine = query_to_file(query)
    responses = []
    for area_of_focus in query[0].areas_of_focus:
      response = query_engine.query(f"I am providing you the terms and services of a company. You are instructed to read these terms of service and to respond to the query I have in regard to the terms of service. My query is: How does this terms of service address {area_of_focus}. Please respond with the information in the format of a json string like this: {query_response_format()} where the key 'area_of_focus' is {area_of_focus}. Please make sure that the formatting of the json string is correct and there are no additional single or double quotes other than what a json string would require")
      result = Result(response=json.loads(str(response)), query=query[0])
      result.save()
      responses.append(result)
    return responses
  
  def compare(self, list_tos):
    query_engine = query_to_file(list_tos)
    response = query_engine.query(f"I am providing you the terms and services of two companies. You are instructed to read these terms of service and to respond to the query I have in regard to the terms of service. My query is: How does the first company's terms of service compare to the second company's terms of service. Please respond with the information in the format of a json string like this: {comparison_response_format()} where the areas_of_focus is one of the following: {areas_of_focus()}. Replace the place holders company_name_1 and company_name_2 with the actual company names. State how they differ in the values for the company names. Please make sure that the formatting of the json string is correct and there are no additional single or double quotes other than what a json string would require")
    comparison = Comparison(response=json.loads(str(response)))
    comparison.save()
    return comparison

def query_to_file(query):
  if len(query) == 1:
    file = open('data/tos.txt', 'w')
    file.write(query[0].tos)
    file.close()
    query_engine = create_query_engine(directory='data')
    return query_engine
  else:
    file1 = open('compare/tos1.txt', 'w')
    file1.write(query[0].tos)
    file1.close()
    file2 = open('compare/tos2.txt', 'w')
    file2.write(query[1].tos)
    file2.close()
    query_engine = create_query_engine(directory='compare')
    return query_engine

def create_query_engine(directory):
    documents = SimpleDirectoryReader(directory).load_data()
    index = GPTVectorStoreIndex.from_documents(documents=documents)
    query_engine = index.as_query_engine()
    return query_engine

def query_response_format():
  format = """
      {
				"title": "areas_of_focus"
        "impact": "key information about how this terms of service would effect me in regards to this area_of_focus.",
        "actionable": "any steps outlined in the terms of service how I, as the consumer can take to protect myself in regards to this area_of_focus.",
        "ranking": "On a scale of 1 to 10, with 1 being the most business friendly and 10 being the most consumer friendly, how does this terms of service compare on the issue of this area_of_focus with that of the industry standard. Do not include complete sentences such as 'on a scale of 1 to 10, this is a 7.' in that case, just respond 7. You need to be succinct."
      }
     """
  return format

def comparison_response_format():
  format = """
      {
				"title": "areas_of_focus"
        "company_1": "Name of company_1",
        "company_2": "Name of company_2."
        "comparison": "How company_1 differs from company_2 in regards to this area_of_focus."
      }
     """
  return format

def areas_of_focus():
	[
      "reoccurring payments",
      "mandatory binding arbitration",
      "data collection",
      "data sharing",
      "data storage",
      "data security",
      "right to termination",
      "user restrictions"
	]