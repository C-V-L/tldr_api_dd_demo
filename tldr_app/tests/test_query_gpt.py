import pytest
from tldr_app.models import *
from tldr_app.services import QueryGPT, query_to_file
import vcr
from unittest.mock import patch, MagicMock
import json

my_vcr = vcr.VCR(
    filter_headers=['Authorization'],
)
# def test_create_query_engine(db):
#   query_gpt = QueryGPT()
#   query_engine = query_gpt.create_query_engine()
#   assert isinstance(query_engine, object)

def test_initiate_query(db):
  query_gpt = QueryGPT()
  random_user = User.objects.create(name="Hady")
  random_query = Query.objects.create(tos="The Parties agree that all claims and disputes arising under or relating to this Agreement are first to be settled by mediation administered by Arbitration Resolution Services (ARS. The parties expressly agree to abide by the Mediation Rules & Regulations of ARS as found at the ARS website, www.arbresolutions.com. Any unresolved disputes arising under or relating to this Agreement are to be settled by binding arbitration. The arbitration shall be conducted by ARS and the parties shall be bound by any and the applicable arbitration rules of ARS and any award/decision rendered. ARS rules can be found at the ARS website. Any decision or award as a result of any such arbitration proceeding shall be in writing and shall provide an explanation for all decisions. Any such arbitration shall be conducted by an arbitrator experienced in [insert industry or legal experience required for arbitrator]and shall include a written record of the arbitration hearing. An award of arbitration may be confirmed in a court of competent jurisdiction. Unless the parties agree otherwise, the same individual will not serve as both mediator arbitrator.", user=random_user, areas_of_focus= ["mandatory binding arbitration", "focus"])

  with my_vcr.use_cassette('fixtures/vcr_cassettes/query_gpt.yaml'):
    response = query_gpt.initiate_query(random_query)
    assert isinstance(response, list)
    first_list_element = response[0]
    second_list_element = response[1]
    assert first_list_element.query.areas_of_focus[0] == 'mandatory binding arbitration'
    assert first_list_element.query.areas_of_focus[1] == 'focus'
    assert isinstance(first_list_element.response, dict)
    assert isinstance(first_list_element.response['title'], str)
    assert isinstance(first_list_element.response['impact'], str)
    assert isinstance(first_list_element.response['actionable'], str)
    assert isinstance(first_list_element.response['ranking'], str)

def test_query_response_format_error(db):
  query_gpt = QueryGPT()
  random_user = User.objects.create(name="Hady")
  random_query = Query.objects.create(tos="The Parties agree that all claims and disputes arising under or relating to this Agreement are first to be settled by mediation administered by Arbitration Resolution Services (ARS. The parties expressly agree to abide by the Mediation Rules & Regulations of ARS as found at the ARS website, www.arbresolutions.com. Any unresolved disputes arising under or relating to this Agreement are to be settled by binding arbitration. The arbitration shall be conducted by ARS and the parties shall be bound by any and the applicable arbitration rules of ARS and any award/decision rendered. ARS rules can be found at the ARS website. Any decision or award as a result of any such arbitration proceeding shall be in writing and shall provide an explanation for all decisions. Any such arbitration shall be conducted by an arbitrator experienced in [insert industry or legal experience required for arbitrator]and shall include a written record of the arbitration hearing. An award of arbitration may be confirmed in a court of competent jurisdiction. Unless the parties agree otherwise, the same individual will not serve as both mediator arbitrator.", user=random_user, areas_of_focus= ["mandatory binding arbitration", "focus"])
  format = """
        {
          "title": "areas_of_focus"
          "impact": "key information about how this terms of service would effect me in regards to this area_of_focus.",
          "actionable": "any steps outlined in the terms of service how I, as the consumer can take to protect myself in regards to this area_of_focus.',
          "ranking": "On a scale of 1 to 10, with 1 being the most business friendly and 10 being the most consumer friendly, how does this terms of service compare on the issue of this area_of_focus with that of the industry standard. Do not include complete sentences such as 'on a scale of 1 to 10, this is a 7.' in that case, just respond 7. You need to be succinct.",
        }
      """
  
  with my_vcr.use_cassette('fixtures/vcr_cassettes/query_gpt_500_error.yaml'):
    with patch('llama_index.query_engine.retriever_query_engine.RetrieverQueryEngine.query') as mock_response:
      mock_response.return_value = format
      response = query_gpt.initiate_query(random_query)
      json_format = json.loads("""
      {
				"title": "focus",
        "impact": "We were unable to get our pal ChatGPT to do something useful, please try again.",
        "actionable": "Please try again",
        "ranking": "n/a"
      }""")
      json_response = json.loads(response[1].response)
      assert json_response == json_format

def test_query_to_file(db):
  random_user = User.objects.create(name="Hady")
  random_query = Query.objects.create(tos="Sample TOS.", user=random_user, areas_of_focus= ["mandatory binding arbitration", "focus"])
  query_to_file(random_query)
  
  with open('data/tos.txt', 'r') as f:
    file_contents = f.read()

  assert file_contents == "Sample TOS."


