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
		responses = []
		for area_of_focus in query.areas_of_focus:
			# response = query_engine.query(f"I am providing you the terms and services of a company and I am seeking information about how this would apply to me. I am concerned about this area: {area_of_focus}. Please provide me the following information in the following format: AREA OF FOCUS: {area_of_focus} REQUEST 1: key information about how this terms of service would effect me with regards to {area_of_focus}. REQUEST 2: any steps outlined in the terms of service how I, as the consumer can take to protect myself in regards to the issue of {area_of_focus}. REQUEST 3: On a scale of 1 to 10, with 1 being the most business friendly and 10 being the most consumer friendly, how does this terms of service compare on the issue of {area_of_focus} with that of the industry standard. Do not include complete sentences such as 'on a scale of 1 to 10, this is a 7.' in that case, just respond 7. You need to be succinct.I want the formatting to be exactly like I outlined above, with you including the capital letters of what I have provided in the prompt and the lowercase letters to be your response. Make sure the entire response is 200 words/ 1300 characters or less. Please only include the information I am specifically requesting. Do not include anything extraneous and do not quote extensively from the terms.")
			response = query_engine.query(f"I am providing you the terms and services of a company and I am seeking information about how this would apply to me. I am concerned about this area: {area_of_focus}. Please provide me the following information in the format of a python dictionary where the key is {area_of_focus} and the values are dictionary keys: 'impact': 'key information about how this terms of service would effect me with regards to {area_of_focus}. 'actionable': any steps outlined in the terms of service how I, as the consumer can take to protect myself in regards to the issue of {area_of_focus}. 'ranking': 'On a scale of 1 to 10, with 1 being the most business friendly and 10 being the most consumer friendly, how does this terms of service compare on the issue of {area_of_focus} with that of the industry standard. Do not include complete sentences such as 'on a scale of 1 to 10, this is a 7.' in that case, just respond 7. You need to be succinct.' I want the formatting to be exactly like I outlined above, with you including the capital letters of what I have provided in the prompt and the lowercase letters to be your response. Make sure the entire response is 200 words/ 1300 characters or less. Please only include the information I am specifically requesting. Do not include anything extraneous and do not quote extensively from the terms. Make sure you close each dictionary with the appropriate bracket' and separate each dictionary with a comma.")
			responses.append(str(response))
		formatted_response = { "concerns": {} }
		for response in responses:
			f_response = eval(response)
			formatted_response["concerns"].update(f_response)
		import pdb; pdb.set_trace()
		return formatted_response
