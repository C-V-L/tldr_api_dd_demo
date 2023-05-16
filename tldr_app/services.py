import os
from decouple import config
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from .models import *

# class QueryGPT():	
# 	def initiate_query(query):
# 		os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')
# 		file = open('data/tos.txt', 'w')
# 		file.write(query.tos)
# 		file.close()
# 		documents = SimpleDirectoryReader('data').load_data()
# 		index = GPTVectorStoreIndex.from_documents(documents=documents)
# 		query_engine = index.as_query_engine()
# 		responses = []
# 		for area_of_focus in query.areas_of_focus:
# 			response = query_engine.query(f"I am providing you the terms and services of a company and I am seeking information about how this would apply to me. I am concerned about this area: {area_of_focus}. Please provide me the following information in the following format: AREA OF FOCUS: {area_of_focus} REQUEST 1: information about how this terms of service would effect me with regards to {area_of_focus}. REQUEST 2: any steps outlined in the terms of service how I, as the consumer can take to protect myself in regards to the issue of {area_of_focus}. REQUEST 3: On a scale of 1 to 10, with 1 being the most business friendly and 10 being the most consumer friendly, how doe this terms of service compare on the issue of {area_of_focus} with that of the industry standard. Do not include complete sentences such as 'on a scale of 1 to 10, this is a 7.' in that case, just respond 7. You need to be succinct.I want the formatting to be exactly like I outlined above, with you including the capital letters of what I have provided in the prompt and the lowercase letters to be your response. Make sure the entire response is 200 words/ 1300 characters or less. Please only include the information I am specifically requesting. Do not include anything extraneous and do not quote extensively from the terms.")
# 			responses.append(str(response))
# 		return responses


class QueryGPT:
  def __init__(self):
    os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

  def initiate_query(self, query):
    with open('data/tos.txt', 'w') as file:
        file.write(query.tos)

    documents = SimpleDirectoryReader('data').load_data()
    index = GPTVectorStoreIndex.from_documents(documents=documents)
    query_engine = index.as_query_engine()
    responses = []

    prompt_template = (
        "I am seeking information about the terms and services of a company and how they apply to me. "
        "I am particularly concerned about the area of {area_of_focus}. "
        "Please provide me with the following information:\n\n"
        "AREA OF FOCUS: {area_of_focus}\n\n"
        "REQUEST 1: How does this terms of service affect me in relation to {area_of_focus}?\n\n"
        "REQUEST 2: What steps are outlined in the terms of service that I, as the consumer, can take to protect myself "
        "regarding the issue of {area_of_focus}?\n\n"
        "REQUEST 3: On a scale of 1 to 10, with 1 being the most business-friendly and 10 being the most consumer-friendly, "
        "how does this terms of service compare to the industry standard regarding {area_of_focus}? "
        "Please provide a numeric rating between 1 and 10, without additional sentences or explanations.\n\n"
        "Please respond in a succinct manner, following the outlined format. "
        "Ensure that the entire response is within 200 words / 1300 characters and includes only the specifically requested information. "
        "Avoid quoting extensively from the terms."
    )

    for area_of_focus in query.areas_of_focus:
        prompt = prompt_template.format(area_of_focus=area_of_focus)
        response = query_engine.query(prompt)
        responses.append(str(response))

    return responses

# how are we setting the response preferences? 
# ex: response = openai.Completion.create(
#   model="text-davinci-003",
#   prompt="A neutron star is the collapsed core of a massive supergiant star, which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei.\n\nTl;dr",
#   temperature=0.7,
#   max_tokens=60,
#   top_p=1,
#   frequency_penalty=0,
#   presence_penalty=1
# )