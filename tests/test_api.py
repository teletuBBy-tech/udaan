from fastapi.testclient import TestClient
from api import app
client=TestClient(app)
def test_health_is_demo():
    r=client.get('/api/health'); assert r.status_code==200 and r.json()['mode']=='demo'
def test_skill_extraction_uses_text_evidence():
    r=client.post('/api/skills/extract',json={'text':'मैं गायों का दूध निकालता हूँ और मोबाइल ठीक करता हूँ'})
    labels={s['label'] for s in r.json()['skills']}; assert 'पशु देखभाल' in labels and 'बुनियादी मरम्मत' in labels
    assert all(s['status']=='inferred_unconfirmed' for s in r.json()['skills'])
def test_opportunities_explicitly_demo():
    r=client.get('/api/opportunities'); assert r.status_code==200
    assert all(o['verification']=='demo_unverified' for o in r.json()['items'])
def test_eligibility_does_not_guess():
    r=client.post('/api/eligibility/check',json={'record_id':'unknown-scheme'})
    assert r.status_code==200 and r.json()['status']=='unable_to_determine'
def test_module_requires_exactly_five_steps_and_review():
    assert client.post('/api/modules',json={'steps':['1','2']}).status_code==422
    assert client.post('/api/modules',json={'steps':['1','2','3','4','5']}).status_code==400
    r=client.post('/api/modules',json={'steps':['1','2','3','4','5'],'reviewed_by_teacher':True})
    assert r.status_code==200 and r.json()['payments']=='mock_only'
def test_referral_requires_consent():
    assert client.post('/api/referrals',json={'student_id':'synthetic'}).status_code==400
    assert client.post('/api/referrals',json={'student_id':'synthetic','consent_confirmed':True}).json()['external_delivery'] is False
def test_frontend_is_served_by_combined_app():
    r=client.get('/')
    assert r.status_code==200 and 'उड़ान' in r.text
    assert client.get('/app.js').status_code==200

def test_career_match_returns_multiple_exploration_options():
    r=client.post('/api/careers/match',json={'text':'मैं गायों की देखभाल करता हूँ और मोबाइल ठीक करता हूँ'})
    assert r.status_code==200 and len(r.json()['items'])>=5
