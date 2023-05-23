import pytest
from tldr_app.models import *
from tldr_app.services import QueryGPT, query_to_file
import vcr

my_vcr = vcr.VCR(
    filter_headers=['Authorization'],
)

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

def test_query_to_file(db):
  random_user = User.objects.create(name="Hady")
  random_query = Query.objects.create(tos="Sample TOS.", user=random_user, areas_of_focus= ["mandatory binding arbitration", "focus"])
  query_to_file(random_query)
  
  with open('data/tos.txt', 'r') as f:
    file_contents = f.read()

  assert file_contents == "Sample TOS."


