# उड़ान — Learning-to-Livelihood for Rural India

A mobile-first Hindi prototype connecting everyday strengths to career exploration, learning pathways, local opportunity discovery, teacher-created lessons, and family conversations.

> **Honesty note:** This repository is a demonstrator, not a production service. All nearby opportunity records are labelled sample/demo data. It does not contain live vacancies, verified partner listings, real payments, real referrals, a hosted LLM, a production RAG index, or a production student database. Career and skill suggestions are rule-based prototype guidance, not formal assessments.

## What works in the prototype

- **बात करें / Talk:** Editable text input; Web Speech API voice recognition when the browser supports it; speech playback where supported; rule-based skill suggestions with student confirmation; career cards.
- **सीखें / Learn:** Multiple career pathways; step completion; locally persisted progress; saved careers.
- **मौके / Chances:** Opportunity map-style SVG with selectable pins and a list alternative; career and type filters; detail cards; visible source and demo status. The map is intentionally schematic and distances are sample values.
- **शिक्षक / Teacher:** Synthetic cohort profiles; a consent-gated demo referral; text/voice input for a module; generated title, exactly five meaningful steps and a quiz; editable content; local save; Free / Per module / Subscription mock pricing; simulated publication state.
- **परिवार / Family:** Four-part family summary (steps, nearby opportunity, cost, first earning); Hindi text-to-speech where available; WhatsApp share link/Web Share API and copy fallback.
- **Offline basics:** Browser localStorage for profile, saved careers/opportunities, pathway progress and module; service-worker cache for the app shell after first successful load; connection status. This is not a claim of tested, conflict-safe background synchronization.
- **Optional FastAPI demo API:** Health, occupations, profiles, skill extraction, career matching, pathways, sample opportunities, cautious eligibility response, consent-gated referrals and module generation.

## Run the frontend

Python 3 is sufficient for the static frontend. From this directory:

```bash
python -m http.server 4173
```

Open <http://localhost:4173>. Service-worker/PWA installation requires localhost or HTTPS. The initial Google Fonts import is optional; the page falls back to system sans-serif fonts if unavailable. For low-connectivity use, remove the external font import to make the demo fully self-contained.

## Run the optional API

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn api:app --reload --port 8000
```

Open <http://localhost:8000> for the combined app, <http://localhost:8000/docs> for the OpenAPI UI, and <http://localhost:8000/api/health> for status. When the frontend is served by FastAPI, hidden-skill extraction calls the API and falls back to local rules if it is unavailable. Other frontend features remain client-side demo logic. Profiles in the API are in-memory and disappear on restart.

## Tests

```bash
pip install -r requirements.txt
pytest -q
```

Manual checks for speech recognition, speech playback, share behaviour and offline/PWA behaviour depend on browser, permissions, network and device. No automated browser/device test suite is included.

## Architecture

```mermaid
flowchart TD
  U[Student / Teacher / Family] --> PWA[Responsive Hindi PWA]
  PWA --> UI[Five-tab UI and accessible controls]
  UI --> LS[Browser localStorage]
  UI --> SW[Service worker app-shell cache]
  UI --> VOICE[Web Speech API fallback]
  UI -. optional future integration .-> API[FastAPI REST API]
  API --> RULES[Rule-based skill / career / eligibility logic]
  API --> DATA[Versioned JSON demo data]
  API -. production extension .-> DB[(PostgreSQL + migrations]
  API -. production extension .-> RAG[Curated knowledge base / RAG]
  API -. configured provider .-> AI[LLM / BHASHINI adapters]
```

## Repository layout

- `index.html`, `app.js`: frontend and five-tab interaction flows.
- `manifest.webmanifest`, `sw.js`: install metadata and basic shell cache.
- `api.py`: optional FastAPI demo endpoints.
- `data/opportunities.json`: explicitly synthetic sample records.
- `tests/test_api.py`: API business-rule tests.
- `Dockerfile`, `docker-compose.yml`: optional API container.

## Configuration and deployment

- Frontend: deploy `index.html`, `app.js`, `manifest.webmanifest`, and `sw.js` to any static host supporting HTTPS.
- API: build the included Docker image or deploy with Uvicorn behind a production ASGI server and HTTPS reverse proxy.
- There are no API keys or secrets in the frontend. `.env.example` documents placeholders for a future deployment; no provider credentials are required by this demo.
- This repository does not yet implement production authentication, server-side role authorization, persistent profile storage, durable sync queues/conflict resolution, a real RAG service, verified official scheme ingestion, actual BHASHINI integration, a real map tile provider, or production payment processing. Do not expose real minors' data through this demo.

## Privacy and safety

Use synthetic profiles only. Do not collect precise location, sensitive eligibility details, voice recordings, or personal contacts in a production system without a privacy review, appropriate consent and safeguards. Referral and publication actions are local demo states only. Check the DPDP Act and rules/commencement provisions in force before deployment.

## Extend the prototype

1. Add an occupation to `careers` in `app.js` and `CAREERS` in `api.py`, with evidence-based source metadata.
2. Add opportunities to `data/opportunities.json` only after obtaining a reliable source; distinguish `verified` from `demo_unverified` and include `last_verified` and a source URL.
3. Add an AI provider behind a backend-only adapter and validate structured output before display.
4. Replace localStorage with IndexedDB for larger offline data and implement a durable authenticated sync queue before claiming robust offline sync.
5. Add provider adapters for speech-to-text/text-to-speech, with typed fallbacks and permission/error handling.

## Demo walkthrough (2–3 minutes)

1. In **बात करें**, review the prefilled sample story, press “मेरी खूबियाँ पहचानें”, and confirm or edit the inferred skills.
2. Open one career card, mark a learning step complete in **सीखें**, then switch to **मौके** to select a sample pin and inspect the explicit demo/source label.
3. In **शिक्षक**, generate a module from the sample plant-care explanation; review its five steps and quiz, change pricing, and save/publish the local demo state.
4. In **परिवार**, choose the same career, play the summary if supported, and try the WhatsApp/share fallback.
5. Refresh to show local persistence; optionally test offline after the first successful visit.
