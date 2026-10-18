"""Optional FastAPI demo backend. All records are synthetic/demo unless sourced explicitly."""
from pathlib import Path
import json, re
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).parent
app = FastAPI(title="Udaan Learning-to-Livelihood API", version="0.1.0", description="Demo APIs; sample opportunities are not live or verified.")
CAREERS = [
 {"id":"mobile","name":"मोबाइल रिपेयर तकनीशियन","skills":["मोबाइल","मरम्मत","repair","mobile"],"pathway":["बुनियादी इलेक्ट्रॉनिक्स","औज़ारों की पहचान","व्यावहारिक प्रशिक्षण","अभ्यास और पोर्टफोलियो","प्रशिक्षु या स्थानीय काम"]},
 {"id":"dairy","name":"डेयरी और पशु देखभाल","skills":["पशु","गाय","दूध","animal","dairy","cow"],"pathway":["पशु देखभाल की बुनियाद","दूध की स्वच्छता","विशेषज्ञ से सीखें","व्यावहारिक अनुभव","सेवा या व्यवसाय खोजें"]},
 {"id":"retail","name":"रिटेल और ग्राहक सेवा","skills":["दुकान","ग्राहक","बातचीत","customer","shop"],"pathway":["ग्राहक से संवाद","बुनियादी हिसाब","डिजिटल कौशल","अनुभव का रिकॉर्ड","काम के अवसर"]},
 {"id":"tailor","name":"टेलरिंग और कपड़ा डिज़ाइन","skills":["सिलाई","कपड़ा","डिज़ाइन","stitch","design"],"pathway":["सिलाई की बुनियाद","नाप और पैटर्न","छोटे प्रोजेक्ट","काम का नमूना","काम या उद्यम"]},
 {"id":"agritech","name":"कृषि तकनीक सहायक","skills":["खेती","खेत","पौधा","ड्रोन","farm","drone"],"pathway":["खेती की बुनियाद","तकनीक पहचानें","सुरक्षित अभ्यास","प्रशिक्षण की जाँच","स्थानीय समाधान"]},
 {"id":"electric","name":"इलेक्ट्रिकल और सौर ऊर्जा","skills":["बिजली","सौर","electric","solar"],"pathway":["सुरक्षा पहले","बुनियादी सिद्धांत","प्रशिक्षित मार्गदर्शन","प्रमाणपत्र जाँचें","प्रशिक्षु अवसर"]},
 {"id":"entrepreneur","name":"छोटा व्यवसाय और उद्यमिता","skills":["व्यवसाय","दुकान","ग्राहक","business"],"pathway":["समस्या पहचानें","छोटा बजट बनाएं","छोटा प्रयोग","ग्राहक प्रतिक्रिया","सहायता खोजें"]}
]
OPPORTUNITIES = json.loads((ROOT / "data/opportunities.json").read_text(encoding="utf-8"))
class Profile(BaseModel):
    name: str = Field(default="", max_length=80)
    education_level: str = Field(default="", max_length=80)
    location: str = Field(default="", max_length=160)
    interests: str = Field(default="", max_length=1000)
class SkillRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
class MatchRequest(BaseModel):
    text: str = Field(default="", max_length=5000)
    interests: str = Field(default="", max_length=1000)
    confirmed_skills: list[str] = Field(default_factory=list, max_length=30)
class EligibilityRequest(BaseModel):
    education_level: Optional[str] = None
    state: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=0, le=120)
    record_id: str = Field(min_length=1, max_length=100)

PROFILES = {}
@app.get("/api/health")
def health(): return {"status":"ok","mode":"demo","data_note":"Opportunity records are synthetic and not live/verified."}
@app.get("/api/occupations")
def occupations(): return {"items": CAREERS, "count": len(CAREERS)}
@app.post("/api/profile")
def save_profile(profile: Profile):
    profile_id = "demo-profile"
    PROFILES[profile_id] = profile.model_dump()
    return {"id":profile_id,"profile":PROFILES[profile_id],"storage":"in-memory demo only"}
@app.get("/api/profile/{profile_id}")
def get_profile(profile_id: str):
    if profile_id not in PROFILES: raise HTTPException(404,"Profile not found in this demo session")
    return {"id":profile_id,"profile":PROFILES[profile_id]}
@app.post("/api/skills/extract")
def extract_skills(req: SkillRequest):
    text = req.text.lower()
    rules = [
      ("पशु देखभाल",["पशु","गाय","दूध","बकरी","animal","cow","dairy"]),
      ("ग्राहक से बातचीत",["ग्राहक","दुकान","सामान","बातचीत","customer","shop"]),
      ("बुनियादी मरम्मत",["मरम्मत","ठीक","खराबी","मोबाइल","repair","mobile"]),
      ("रचनात्मक हाथ का काम",["सिलाई","कपड़ा","डिज़ाइन","stitch","craft"]),
      ("खेती और प्रकृति",["खेती","खेत","पौधा","मिट्टी","फसल","farm","plant"]),
    ]
    skills = [{"label":name,"evidence":[term for term in terms if term.lower() in text],"status":"inferred_unconfirmed"} for name,terms in rules if any(term.lower() in text for term in terms)]
    return {"skills":skills,"note":"Inferred suggestions only; not an aptitude test or formal certification."}
@app.post("/api/careers/match")
def match_careers(req: MatchRequest):
    text = (req.text + " " + req.interests + " " + " ".join(req.confirmed_skills)).lower()
    scores=[]
    for c in CAREERS:
        hits=[s for s in c["skills"] if s.lower() in text]
        scores.append({"career_id":c["id"],"name":c["name"],"match_signals":hits,"score":len(hits),"interpretation":"exploration suggestion, not a definitive aptitude score"})
    return {"items":sorted(scores,key=lambda x:x["score"],reverse=True)}
@app.post("/api/pathways/generate")
def pathways(career_id: str):
    c=next((c for c in CAREERS if c["id"]==career_id),None)
    if not c: raise HTTPException(404,"Unknown occupation")
    return {"career_id":c["id"],"career":c["name"],"steps":[{"title":s,"status":"not_started","source_status":"general_guidance; verify provider requirements"} for s in c["pathway"]]}
@app.get("/api/opportunities")
def opportunities(career_id: Optional[str]=None):
    items=[o for o in OPPORTUNITIES if career_id is None or o["career_id"]==career_id]
    return {"items":items,"count":len(items),"warning":"All records are demonstration data; none should be treated as a live vacancy or verified opportunity."}
@app.post("/api/eligibility/check")
def eligibility(req: EligibilityRequest):
    # No actual scheme eligibility records are seeded; never guess eligibility.
    return {"status":"unable_to_determine","reason":"No authoritative scheme rule for this record is present in the demo knowledge base.","source":None,"record_id":req.record_id}
@app.post("/api/referrals")
def referral(payload: dict):
    if not payload.get("consent_confirmed"): raise HTTPException(400,"Appropriate consent confirmation is required")
    return {"status":"demo_saved","external_delivery":False,"note":"No real organization received this referral."}
@app.get("/api/facilitator/cohorts")
def cohorts(): return {"items":[{"id":"demo-cohort","name":"डेमो विद्यार्थी समूह","student_count":3,"synthetic":True}]}
class ModuleRequest(BaseModel):
    transcript: str = Field(min_length=1,max_length=5000)
@app.post("/api/modules/generate")
def generate_module(req: ModuleRequest):
    topic="पौधों की देखभाल" if "पौध" in req.transcript else "रोज़मर्रा के काम से सीखें"
    if topic=="पौधों की देखभाल": steps=["बीज को पहचानें और उसके उगने की जरूरत समझें।","पौधे के लिए मिट्टी और साफ जगह तैयार करें।","मिट्टी की नमी देखकर उचित मात्रा में पानी दें।","पौधे की जरूरत के अनुसार धूप और हवा दें।","उपयुक्त खाद और नियमित देखभाल के बारे में सीखें।"]
    else: steps=["विषय का उद्देश्य समझें।","जरूरी चीज़ों और सुरक्षित उपयोग को पहचानें।","शिक्षक के उदाहरण को ध्यान से देखें।","देखरेख में छोटा अभ्यास करें।","सीखी बात अपने शब्दों में दोहराएँ।"]
    return {"title":topic+" के पाँच कदम","steps":steps,"quiz":{"question":"पौधे की देखभाल में किस बात पर ध्यान देना चाहिए?","answer":"मिट्टी की नमी, धूप और पौधे की जरूरत"},"status":"draft_requires_teacher_review"}
@app.post("/api/modules")
def save_module(payload: dict):
    if len(payload.get("steps",[])) != 5: raise HTTPException(422,"A module must have exactly five ordered steps")
    if not payload.get("reviewed_by_teacher"): raise HTTPException(400,"Teacher review is required before publication")
    return {"id":"demo-module","status":"saved_in_demo","payments":"mock_only","externally_published":False}
@app.get("/api/modules")
def list_modules(): return {"items":[],"note":"Modules are stored locally in the browser prototype; this endpoint does not persist them."}
@app.post("/api/sync")
def sync(payload: dict): return {"status":"demo_acknowledged","synced":False,"note":"Production synchronization requires authentication, persistent storage and conflict handling."}

# Serve the same-origin frontend when running the combined demo on port 8000.
app.mount("/", StaticFiles(directory=ROOT, html=True), name="frontend")
