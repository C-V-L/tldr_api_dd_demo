import os 
import pickle
from decouple import config
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, download_loader, GPTListIndex, LLMPredictor, PromptHelper
from llama_index import ServiceContext, StorageContext, load_index_from_storage

os.environ['OPENAI_API_KEY'] = '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'
import pdb; pdb.set_trace()
# PromptHelper.set_openai_key(os.environ['OPENAI_API_KEY'])

def authorize_gdocs():
	google_oauth2_scopes = [
		"https://www.googleapis.com/auth/documents.readonly"
	]
	cred = None
	if os.path.exists("token.pickle"):
		with open("token.pickle", 'rb') as token:
			cred = pickle.load(token)
	if not cred or not cred.valid:
		if cred and cred.expired and cred.refresh_token:
			cred.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file("credentials.json", google_oauth2_scopes)
			cred = flow.run_local_server(port=3000)
		with open("token.pickle", 'wb') as token:
			pickle.dump(cred, token)


# function to authorize or download latest credentials 
# authorize_gdocs()

# initialize LlamaIndex google doc reader
GoogleDocsReader = download_loader('GoogleDocsReader')

# list of google docs we want to index 
gdoc_ids = ['1dZgdb8vqtJ015v3y9e89eYcBhqWbh8vq041FJqwoZso']

loader = GoogleDocsReader()
import pdb; pdb.set_trace()
# load gdocs and index them 
# documents = loader.load_data(gdoc_ids)
# index = GPTVectorStoreIndex.from_documents(documents=documents)
# index.storage_context.persist(persist_dir = 'storage')


# storage_context = StorageContext.from_defaults(persist_dir = 'storage')
# index = load_index_from_storage(storage_context)
# query_engine = index.as_query_engine()

# response = query_engine.query("I have provided you two terms of service for two different terms of service for a music streaming application. Can you compare and contrast the two in substantial detail?")
