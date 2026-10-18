
# उड़ान — Learning-to-Livelihood for Rural India
# drive link of the video prototype - https://drive.google.com/file/d/1zj-jdx4x-EZ-4asNBBu4zxRLmEYNRGI4/view?usp=sharing
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
<img width="5191" height="4640" alt="Udaan Browser Demo Platform-2026-10-18-175305" src="https://github.com/user-attachments/assets/6fa9d68b-bff5-4ca4-ab15-6014e9462455" />

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


[Udaan_README_Expanded.md](https://github.com/user-attachments/files/33633989/Udaan_README_Expanded.md)# उड़ान (Udaan) — Learning-to-Livelihood for Rural India

> **Discover strengths → explore careers → learn practical skills → find opportunities → build a livelihood.**

A mobile-first, Hindi-first prototype connecting rural Indian learners' everyday strengths to career exploration, personalized learning pathways, local opportunity discovery, teacher-created lessons, and family conversations.

**Project status:** Functional demonstrator, not a production service. This README clearly separates current functionality from future architecture recommendations.

> **Honesty note:** All nearby opportunity records are labelled sample/demo data. The prototype does not contain live vacancies, verified partner listings, real payments, real external referrals, a hosted LLM, a production RAG index, or a production student database. Career and skill suggestions are rule-based prototype guidance, not formal assessments. Browser voice capabilities depend on browser, device, permissions and connectivity.

---

## Contents

1. [Product vision](#1-product-vision)
2. [What works in the prototype](#2-what-works-in-the-prototype)
3. [Page-by-page technology chart](#3-page-by-page-technology-chart)
4. [Technology stack: current vs production](#4-technology-stack-current-vs-production)
5. [Architecture diagrams](#5-architecture-diagrams)
6. [How each feature is incorporated](#6-how-each-feature-is-incorporated)
7. [AI, RAG and recommendation strategy](#7-ai-rag-and-recommendation-strategy)
8. [Offline-first design](#8-offline-first-design)
9. [Repository layout](#9-repository-layout)
10. [Run locally](#10-run-locally)
11. [API reference](#11-api-reference)
12. [Production roadmap](#15-production-roadmap)
13. [Configuration and deployment](#16-configuration-and-deployment)
14. [Demo walkthrough](#17-demo-walkthrough)
15. [Known limitations](#18-known-limitations)


---

## 1. Product vision

Education does not always translate into relevant practical skills, career clarity or economic opportunity. Rural learners may have limited access to career guidance, vocational training, mentors, professional exposure and trustworthy information about nearby opportunities. Useful abilities developed through family responsibilities, community work, agriculture, repairs, creative activities or helping customers can remain invisible to formal career systems.

Udaan aims to connect these fragmented experiences in one accessible journey:

1. **Discover:** Identify possible strengths from everyday experiences.
2. **Explore:** Show a broad range of academic, vocational, creative, technical, agricultural and entrepreneurial careers.
3. **Learn:** Turn a career interest into practical, ordered learning steps.
4. **Connect:** Discover relevant opportunities with transparent source and verification labels.
5. **Support:** Enable teachers to create local learning content and families to discuss next steps.
6. **Continue:** Keep selected information and progress on the device for basic offline use.

### Core users

- Students from Class 9 through graduation.
- Teachers and village facilitators supporting multiple students.
- Parents and family members supporting career decisions.
- Future institutional partners: schools, NGOs, vocational providers, employers and community organizations.

### Design principles

- Hindi-first and mobile-first.
- Voice input where supported, with an equivalent text alternative.
- Large, labelled controls and simple language.
- No assumption that all students want engineering, medicine or government jobs.
- Transparent distinction between inferred, student-confirmed, assessed and certified skills.
- Verified sources for factual opportunity and eligibility claims.
- Honest offline and integration status.
- Data minimization and age-appropriate privacy safeguards.

---

## 2. What works in the prototype

| Feature | Current prototype behaviour | Important boundary |
|---|---|---|
| **बात करें / Talk** | Editable text input; Web Speech API recognition when supported; browser speech playback where supported; rule-based skill suggestions; student confirmation; career cards | Suggestions are exploratory, not a formal aptitude assessment or certification |
| **सीखें / Learn** | Multiple career pathways; step completion; locally persisted progress; saved careers | Persistence is browser/device-local, not a secure multi-device account |
| **मौके / Chances** | Schematic SVG map with selectable pins; list alternative; career/type filters; opportunity detail cards; source and demo-status labels | Map is not geographic; distances and opportunity entries are sample data |
| **शिक्षक / Teacher** | Synthetic cohort profiles; consent-gated demo referral; typed/voice module input; generated title, exactly five meaningful steps and one quiz; editable content; local save; Free / Per module / Subscription mock pricing; simulated publication state | No real referral is delivered, no external publication occurs and no money is processed |
| **परिवार / Family** | Four-part summary covering steps, nearby opportunity, cost and first earning; browser Hindi text-to-speech where available; WhatsApp link/Web Share API/copy fallback | Sharing opens an external action or copies text; the app cannot claim that a message was sent |
| **Offline basics** | `localStorage` for profile, saved careers/opportunities, pathway progress and module; service-worker app-shell cache after a successful first load; connection status | Not a claim of durable background sync, conflict-safe multi-device sync or universal offline speech |
| **Optional FastAPI API** | Health, occupations, profiles, rule-based skill extraction, career matching, pathways, sample opportunities, cautious eligibility response, consent-gated demo referrals and module endpoints | Profile data is in-memory; API sync is explicitly not a production sync implementation |

---

## 3. Page-by-page technology chart

This chart maps each visible page to the current implementation, the method used, and the likely production upgrade. **Future options are recommendations, not currently connected services.**

| Page / component | Current technology | How it is incorporated | Recommended production technology / method |
|---|---|---|---|
| Shared app shell | HTML5, CSS3, CSS variables, responsive media queries | `index.html` contains the five-tab interface; shared styles define colors, spacing, cards and controls | React + TypeScript if the UI grows; reusable accessible components and design tokens |
| **बात करें — Talk** | JavaScript forms; browser Web Speech API when supported; rule-based extraction | User types or dictates a story, edits the transcript, sees inferred skill tags and related career cards | Backend AI-provider adapter, schema-validated structured outputs, evidence spans, uncertainty and student confirmation |
| Talk voice playback | Browser `speechSynthesis` where available | Reads available content aloud without requiring a separate audio asset | Speech-provider adapter; configured BHASHINI or another service only when access, consent and language support are confirmed |
| Career recommendations | Rule-based keyword matching in frontend and optional FastAPI | Skills, text and interests are matched against a small occupation catalogue | Versioned occupation taxonomy, transparent matching rules, curated evidence and evaluated AI-assisted ranking |
| **सीखें — Learn** | JavaScript pathway data and UI state | Selected career renders ordered steps; learners mark steps complete | Versioned pathway API with prerequisites, sources, duration, cost classification and content review |
| Saved learning progress | Browser `localStorage` | Saves selected careers and completion state on the same browser/device | IndexedDB/Dexie for structured offline data; authenticated sync API with idempotency and conflict handling |
| **मौके — Chances** | SVG schematic map, JavaScript pin interactions, JSON demo records | Pins open detail cards; filters and list view use the same sample data | Leaflet, suitable OSM-compatible data/tiles, attribution, sourced coordinates and spatial search |
| Opportunity trust labels | Source/status fields in demo records and UI | Marks data as demonstration/unverified instead of implying live vacancies | Source ingestion, verification workflow, `last_verified_at`, expiry, freshness checks and report-an-issue process |
| **शिक्षक — Teacher** | JavaScript rules, form controls, synthetic cohort data | Generates a title, five meaningful steps and one quiz; allows editing and mock pricing | AI module generation with strict schema, teacher review, moderation, versioning and secure cohort access |
| Teacher referrals | Consent-gated demo endpoint/UI | Requires a consent confirmation and returns a demo status only | Authenticated referral workflow, purpose-specific consent, object-level authorization, audit log and real partner integration |
| **परिवार — Family** | JavaScript summary templates | Creates four practical sections: steps, opportunity, cost and first earning | Reviewed localized templates grounded in source-backed records; never guarantee earnings or jobs |
| Family sharing | Web Share API where supported, WhatsApp share URL and copy fallback | Presents a prepared message; user completes any external action | Device-tested share flow, privacy-aware preview and explicit user control |
| Local profile/settings | HTML controls and `localStorage` | Stores demo preferences locally | Authenticated profile service, consent records, data export/deletion and retention policy |
| Offline app shell | `sw.js`, Web App Manifest, browser storage | Caches a limited set of app resources after the first successful load | Workbox or equivalent, versioned cache lifecycle, offline fallbacks and device-level offline tests |
| Optional backend | Python, FastAPI, Pydantic, Uvicorn | Validates API request bodies and exposes OpenAPI docs | Modular API, PostgreSQL, migrations, authentication, authorization, rate limits and monitoring |
| Demo data | Version-controlled JSON and in-memory API objects | Supplies synthetic career/opportunity records | Curated source registry, database migrations, admin review and record expiry |
| Tests | pytest | Exercises selected API and business rules | Unit, integration, contract, browser E2E, accessibility, security, offline/reconnect and load tests |
| Container | Docker and Docker Compose | Offers a repeatable local API runtime | CI-built images, pinned dependencies, scanning, secrets management and deployment health checks |

### Technology status legend

- **Implemented:** Present in the current repository.
- **Browser-dependent:** Requires compatible browser/device, permission or connectivity.
- **Demo only:** Sample data or simulated action; no external transaction occurs.
- **Recommended:** A possible production upgrade, not currently integrated.

---

## 4. Technology stack: current vs production

### Current prototype stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend structure | HTML5 | Semantic page structure and forms |
| Styling | CSS3, CSS variables, media queries | Responsive layout and shared visual style |
| Client logic | Vanilla JavaScript (`app.js`) | Navigation, skill rules, pathways, filters, module and family flows |
| Voice | Browser Web Speech APIs when available | Speech recognition and speech synthesis fallback |
| Client persistence | `localStorage` | Demo profile, saved items and progress |
| PWA | Web App Manifest + service worker | Install metadata and limited app-shell cache |
| Backend | Python + FastAPI | Optional REST API |
| Validation | Pydantic models | Request validation and field limits |
| API documentation | FastAPI OpenAPI / Swagger UI | Interactive API reference |
| Data | JSON + in-memory demo objects | Synthetic opportunity and profile records |
| Tests | pytest | Automated business-rule/API checks |
| Packaging | Docker + Compose | Optional local API container |

### Production architecture options

| Concern | Recommended option | Why / method |
|---|---|---|
| Frontend | React + TypeScript + Vite, if justified by UI complexity | Component reuse, typed data contracts and maintainable routing |
| Styling | CSS modules or Tailwind CSS with design tokens | Consistent responsive components |
| Routing | React Router if moving to React | Deep links and route-level loading |
| Localization | i18next/react-i18next or equivalent | Keep Hindi and regional-language strings separate from UI logic |
| Offline data | IndexedDB + Dexie | Transactions and structured cached records |
| Service worker | Workbox or equivalent | Versioned caching and predictable update behaviour |
| Backend | FastAPI with modular routers/services | Validation, OpenAPI and Python AI ecosystem |
| Database | PostgreSQL + Alembic migrations | Durable profiles, modules, referrals and opportunities |
| Retrieval | Curated source records + retrieval service; pgvector only if useful | Ground recommendations in approved source material |
| AI | Provider-independent backend adapter | Change model providers without rewriting business logic |
| Structured output | Pydantic / JSON Schema validation | Reject malformed or unsupported model output |
| Speech | Provider adapter for browser speech and configured services | Language flexibility and honest fallback behaviour |
| Maps | Leaflet + permitted tile/geodata source | Real geography, attribution and interactive map controls |
| Authentication | Established OIDC/OAuth-compatible service or reviewed session design | Identity and account lifecycle |
| Authorization | Server-side role-based and object-level checks | Prevent access to another student's data |
| Observability | Structured logs, metrics, error reporting, uptime checks | Diagnose failures and track service health |
| CI/CD | GitHub Actions or equivalent | Automated tests, linting, dependency checks and deployment gates |
| Deployment | Static HTTPS hosting + API container + managed database | Separate frontend/API scaling and secure operations |

**Architecture principle:** Do not adopt every technology just because it appears here. Select the smallest reliable set that meets pilot needs.

---

## 5. Architecture diagrams


### 5.1 System architecture — current and future
<img width="7787" height="7897" alt="Udaan Browser Demo Platform-2026-10-18-174704" src="https://github.com/user-attachments/assets/f7a5d7da-f124-4aec-b1ae-e1b66d5e7d5f" />

### 5.2 Learner journey

<img width="8192" height="642" alt="Udaan Browser Demo Platform-2026-10-18-174833" src="https://github.com/user-attachments/assets/fd20a4e3-373e-43ff-bd60-3e0c0c99d857" />

```

### 5.3 Feature-to-technology map

<img width="3720" height="4482" alt="Udaan Browser Demo Platform-2026-10-18-174936" src="https://github.com/user-attachments/assets/961ce664-0edb-41da-82f4-2b1627e1a068" />


### 5.4 Future AI and RAG request flow

This is a proposed architecture, not a currently connected LLM/RAG service.

<img width="8192" height="3396" alt="Udaan Browser Demo Platform-2026-10-18-175020" src="https://github.com/user-attachments/assets/b9778eb3-bf0c-443f-987c-5f40d070a864" />


## 6. How each feature is incorporated

### A. बात करें — hidden-skills discovery

**Current flow**

`Student story → editable text/transcript → rule-based extraction → possible skills → student confirmation → career cards`

- Text is the universal fallback.
- Browser speech recognition is attempted only when supported.
- Skill rules look for signals such as animal care, customer interaction, basic repair, craft work and agriculture.
- The UI treats results as inferred suggestions, not as certified skills.
- Career cards connect the story to several possible occupations.

**Production upgrade**

1. Normalize the transcript without removing local terms.
2. Extract candidate skills into a validated structured object.
3. Include evidence spans from the student's own description.
4. Represent uncertainty and ask the learner to confirm, edit or reject suggestions.
5. Keep inferred skills separate from formally assessed or certified skills.
6. Use confirmed skills and interests to update career matching and pathway suggestions.
7. Evaluate results on reviewed Hindi and regional-language examples.

### B. सीखें — learning pathways

**Current flow**

`Career selection → pathway data → ordered steps → completion state → localStorage`

- Career pathways contain actionable demonstration steps.
- Completion is saved in browser storage.
- Pathway content is general guidance and should not be treated as verified qualification advice.

**Production upgrade**

- Store occupations, courses, qualifications, prerequisites and job openings as separate record types.
- Add source URL, provider, content version, review date and verification status.
- Display duration and fees only when supported by reliable information.
- Track progress with content version and timestamp.
- Use deterministic prerequisites; let AI simplify explanations rather than invent official requirements.

### C. मौके — hyperlocal opportunity discovery

**Current flow**

`Career/type filter → JSON sample records → SVG pin or list selection → detail card → demo/source status`

- The map is a schematic illustration, not a real geographic map.
- Distances and opportunity entries are sample values.
- A list alternative supports users who find maps difficult to navigate.

**Production upgrade**

- Use Leaflet and a compliant map tile/geodata provider with attribution.
- Store coordinates only when needed and obtained from a reliable source.
- Track `source_url`, `source_name`, `verification_status`, `last_verified_at`, `expires_at` and applicable geography.
- Build a source review, deduplication, stale-record and report-an-issue process.
- Do not fabricate vacancies, fees, seats, deadlines, contacts or salaries.
- Provide a text/list alternative to every map-only interaction.

### D. शिक्षक — voice-to-module builder

**Current flow**

`Typed/spoken topic → rule-based generation → title + exactly five meaningful steps + one quiz → edit → local save/mock pricing`

- The teacher can review and edit generated content.
- Pricing options are demonstration controls.
- Save/publish status is simulated; no payment is processed and no external publication occurs.

**Production upgrade**

- Validate the module with a strict schema: title, exactly five ordered non-empty steps, quiz and answer format.
- Keep modules in draft until reviewed by the teacher.
- Add versioning, moderation, accessibility review and publication controls.
- Enforce cohort membership and authorization on the server.
- Add real payment processing only after operational, legal, tax, refund and safeguarding requirements are reviewed.

### E. परिवार — family-friendly career guidance

**Current flow**

`Selected career → four-part summary → browser speech or visible text → share URL/Web Share/copy fallback`

The four required parts are:

1. **चार कदम:** Practical steps toward the career.
2. **पास का मौका:** Relevant opportunity only when supported by the data; otherwise say it is unverified or unavailable.
3. **कितना खर्च:** Distinguish verified fees, estimates and unknown costs.
4. **पहली कमाई:** Explain prerequisites and uncertainty; never promise income or employment.

**Production upgrade**

- Use reviewed, localized templates grounded in approved sources.
- Make the source and uncertainty visible.
- Keep student choice central in family discussions.
- Ask for user confirmation before sharing personal information externally.

---

## 7. AI, RAG and recommendation strategy

### Current prototype

The prototype uses deterministic keyword/rule-based logic for hidden skills and career matching. The optional FastAPI endpoints return structured demo responses. This is useful for demonstrating the user journey, but it is **not a hosted LLM or production RAG implementation**.

### Recommended production AI design

1. **Provider adapter:** Keep model configuration and credentials on the backend.
2. **Curated knowledge base:** Store approved occupations, training resources, schemes, scholarships, official application pages and source metadata.
3. **Retrieval:** Retrieve relevant records before generating factual explanations.
4. **Structured output:** Validate profile, career match, pathway and module responses with Pydantic/JSON Schema.
5. **Evidence:** Attach source IDs/URLs to claims that depend on factual records.
6. **Uncertainty:** Return “unknown” or ask a question when evidence is missing.
7. **Fallback:** Preserve rule-based guidance and text entry if the model or speech provider is unavailable.
8. **Evaluation:** Test relevance, diversity of careers, source correctness, hallucination rates, language quality and harmful bias.

### Deterministic eligibility rules

Eligibility must not be decided by free-form LLM judgement.

A rules engine should return one of:

- `eligible`
- `possibly_eligible_more_information_required`
- `not_eligible_under_available_rules`
- `unable_to_determine`

Each result should show the rules evaluated, missing information and official source. The current demo intentionally returns `unable_to_determine` when it lacks an authoritative scheme rule.

### Knowledge record fields

A production record should include as many of these fields as relevant:

```json
{
  "id": "example-record-id",
  "name": "Example training opportunity",
  "record_type": "training",
  "description": "Description from a reviewed source",
  "eligibility": [],
  "state": "configured-state",
  "district": "configured-district",
  "education_levels": [],
  "application_url": null,
  "source_name": "Official source name",
  "source_url": "https://example.gov.in/",
  "verification_status": "needs_review",
  "last_verified_at": null,
  "expires_at": null,
  "related_occupations": []
}
```

This is a schema illustration, not a real opportunity record. Replace example values with verified data before use.

---

## 8. Offline-first design

### What is implemented

- Browser `localStorage` for selected profile/preferences, saved careers/opportunities, pathway progress and module state.
- A service worker that caches a limited app shell after a successful first load.
- A Web App Manifest for install metadata.
- A visible connection status indicator.

### What is not yet implemented

- A comprehensive IndexedDB data model.
- A durable sync outbox with server acknowledgements.
- Idempotent sync operations and conflict resolution.
- Reliable multi-device sync.
- Guaranteed offline speech recognition.
- Full device/network-throttling automation.

### Recommended sync contract

1. Save the change locally first.
2. Update the UI immediately.
3. Add a uniquely identified operation to a local queue.
4. Send it when a real API request succeeds.
5. Mark it synchronized only after server acknowledgement.
6. Retry failures with backoff and retain pending changes.
7. Handle conflicting edits explicitly.
8. Never treat `navigator.onLine === true` as proof that the backend is reachable.

Do not claim robust offline synchronization until it is implemented and tested under interrupted connectivity.

---

## 9. Repository layout

```text
rural-livelihood-platform/
├── index.html                  # Main Hindi UI and five-tab shell
├── app.js                      # Frontend interactions and demo logic
├── manifest.webmanifest        # PWA install metadata
├── sw.js                       # Limited app-shell service-worker cache
├── api.py                      # Optional FastAPI demo backend
├── requirements.txt            # Python dependencies
├── .env.example                # Future configuration placeholders
├── Dockerfile                  # Optional API container
├── docker-compose.yml           # Local container setup
├── data/
│   └── opportunities.json      # Synthetic/demo opportunity records
├── tests/
│   ├── conftest.py
│   └── test_api.py             # Selected API and business-rule tests
├── docs/
│   ├── TECHNOLOGY_MAP.md       # Detailed page-to-technology matrix
│   ├── architecture.mmd        # Editable system architecture diagram
│   ├── learner-journey.mmd     # Editable learner journey
│   └── feature-tech-map.mmd    # Editable feature/technology map
├── ARCHITECTURE.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

## 10. Run locally

### Requirements

- Python 3.10+ is recommended; use a version compatible with the pinned dependencies.
- A modern browser.
- No AI-provider credentials are required for the rule-based demo.

### Option A — Run the static frontend

From the project root:

```bash
python -m http.server 4173
```

Open <http://localhost:4173>.

This serves the frontend only; it does not start FastAPI. Service workers generally require `localhost` or HTTPS. Browser speech capabilities vary. The Google Fonts import is optional; system fonts are used as a fallback. For a self-contained low-connectivity demo, remove the external font import and use local/system fonts.

### Option B — Run the FastAPI backend

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies and start the server:

```bash
pip install -r requirements.txt
uvicorn api:app --reload --port 8000
```

Open:

- App: <http://localhost:8000>
- OpenAPI UI: <http://localhost:8000/docs>
- Health check: <http://localhost:8000/api/health>

When the frontend is served by FastAPI, hidden-skill extraction can call the API and fall back to local rules if the API is unavailable. Other frontend features remain client-side demo logic. API profiles are stored in memory and disappear when the process restarts.

### Option C — Docker

```bash
docker compose up --build
```

Use the port configured in `docker-compose.yml`. This is a local demo configuration, not a hardened production deployment.

---

## 11. API reference

The exact implementation is in `api.py`; the generated OpenAPI UI at `/docs` is the source of truth.

| Method | Endpoint | Current behaviour | Important limitation |
|---|---|---|---|
| `GET` | `/api/health` | Returns demo health status | Does not represent full production dependency readiness |
| `GET` | `/api/occupations` | Returns the small demo career catalogue | Not an exhaustive or official taxonomy |
| `POST` | `/api/profile` | Saves a demo profile in memory | No authentication or durable database |
| `GET` | `/api/profile/{profile_id}` | Reads a profile from the current process | Data disappears on restart |
| `POST` | `/api/skills/extract` | Rule-based inferred skill suggestions | Not an aptitude test |
| `POST` | `/api/careers/match` | Keyword-signal career matching | Scores are exploratory signals, not validated aptitude scores |
| `POST` | `/api/pathways/generate?career_id=...` | Returns a career's general guidance steps | Prerequisites and provider details need verification |
| `GET` | `/api/opportunities` | Returns demo records; optional `career_id` filter | Records are not live/verified opportunities |
| `POST` | `/api/eligibility/check` | Returns `unable_to_determine` without an authoritative rule | No production scheme-rule database |
| `GET` | `/api/facilitator/cohorts` | Returns a synthetic cohort | Not connected to real students |
| `POST` | `/api/referrals` | Requires `consent_confirmed` and returns demo status | No real organization receives the referral |
| `POST` | `/api/modules/generate` | Generates a demo title, five steps and quiz | Rule-based, not LLM-generated |
| `POST` | `/api/modules` | Checks exactly five steps and teacher review | Saves demo status only; no external publishing/payment |
| `GET` | `/api/modules` | Returns the demo module list response | Does not persist modules in the API |
| `POST` | `/api/sync` | Returns a demo acknowledgement | Explicitly does not perform production synchronization |

Example health request:

```bash
curl http://localhost:8000/api/health
```

Example skill extraction:

```bash
curl -X POST http://localhost:8000/api/skills/extract \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"मैं गायों का दूध निकालता हूँ और दुकान पर ग्राहकों की मदद करता हूँ।\"}"
```

Windows users may prefer PowerShell's `Invoke-RestMethod` for JSON requests.

---



## 15. Production roadmap

### Phase 1 — Pilot foundation

- [ ] Choose the pilot district, supported languages and local partner model.
- [ ] Review the five-tab user journey with students, teachers and families.
- [ ] Establish a clear data schema and source/verification policy.
- [ ] Add CI for tests and dependency checks.
- [ ] Replace demo opportunity entries only with sourced, reviewed records.

### Phase 2 — Trusted opportunity data

- [ ] Create source ingestion and review workflows.
- [ ] Add last-verified timestamps, expiry and stale-record alerts.
- [ ] Integrate a real map with permitted geospatial data and attribution.
- [ ] Implement official application links and document checklists.
- [ ] Add deterministic eligibility rules with explainable source-linked results.

### Phase 3 — Secure accounts and durable storage

- [ ] Add authentication and server-side role/object authorization.
- [ ] Add PostgreSQL and database migrations.
- [ ] Define data retention, deletion, export and consent lifecycle.
- [ ] Add teacher cohorts, consent-aware referrals and audit records.

### Phase 4 — Reliable offline learning

- [ ] Add IndexedDB for structured local records.
- [ ] Implement a durable sync outbox with unique operation IDs.
- [ ] Add retries, server acknowledgements and conflict resolution.
- [ ] Test interrupted connectivity and recovery on low-end Android devices.
- [ ] Clearly distinguish local save, pending sync and confirmed synchronization.

### Phase 5 — Grounded AI and multilingual voice

- [ ] Add backend-only model and speech-provider adapters.
- [ ] Build a curated knowledge base and retrieval process with source citations.
- [ ] Validate AI outputs with strict schemas and safe fallbacks.
- [ ] Keep eligibility decisions deterministic.
- [ ] Evaluate Hindi and regional-language quality with local reviewers.
- [ ] Track quality, uncertainty and source correctness with privacy-safe evaluation data.

### Phase 6 — Teacher and family workflows

- [ ] Add secure module draft/review/publish/version management.
- [ ] Add verified mentor/employer onboarding and moderation.
- [ ] Run accessibility, privacy and safeguarding reviews.
- [ ] Consider real payments only after operational and legal requirements are settled.

### Phase 7 — Production operations

- [ ] Threat model and security testing.
- [ ] Performance, load and reliability testing.
- [ ] Monitoring, alerts, backups and restore drills.
- [ ] Incident response and support process.
- [ ] Define outcome metrics: learning completion, verified opportunity engagement, referral outcomes and student-reported usefulness.

---

## 16. Configuration and deployment

### Configuration

See `.env.example` for placeholders. The rule-based demo does not require AI-provider credentials.

For a production deployment:
- Store secrets in the hosting provider's secret manager.
- Never commit `.env` files or expose credentials in frontend bundles.
- Configure HTTPS, allowed origins, database credentials and session settings.
- Document every integration as `not_configured`, `sandbox` or `production`.
- Review provider data-processing terms before sending student information to external AI/speech services.

### Deployment pattern

**Prototype**
- Static frontend on any HTTPS static host.
- FastAPI on a Python ASGI-capable host or Docker runtime.
- JSON sample data and in-memory API records.

**Production**
- Static frontend/CDN with cache versioning.
- FastAPI behind HTTPS reverse proxy or API gateway.
- Managed PostgreSQL with migrations and encrypted backups.
- Private object storage only if learning media requires it.
- Backend AI/speech adapters with timeouts, quotas, monitoring and fallbacks.
- Authentication, authorization, secret management, rate limiting and incident response.

The current repository is not production-ready until persistence, authorization, privacy controls, monitoring, backups and end-to-end tests have been implemented and reviewed.

---

## 17. Demo walkthrough (2–3 minutes)

1. **Talk:** Describe helping with dairy, a shop, tailoring or farm tasks. Review the inferred strengths and edit them.
2. **Learn:** Open a related career, inspect the pathway and mark a step complete.
3. **Chances:** Select a schematic pin and point out the sample-data/source label.
4. **Teacher:** Generate a plant-care lesson, review the five steps and quiz, change a mock pricing option and save the demo state.
5. **Family:** Open the same career summary, play speech if supported and demonstrate the share/copy fallback.
6. Refresh the browser to demonstrate local persistence.
7. Explain which capabilities work now and which need real integrations before a pilot.

---

## 18. Known limitations

- Skill extraction and career matching use rules/keywords, not a hosted LLM or validated aptitude model.
- The opportunity map is a schematic SVG; coordinates and distances are not authoritative.
- Opportunity records are sample data, not live vacancies or verified partnerships.
- API profiles are stored in memory and disappear when the process restarts.
- Browser voice support varies by browser, device, permissions and connectivity.
- Service-worker caching is limited to the app shell.
- Comprehensive IndexedDB persistence, durable background synchronization and conflict resolution are not implemented.
- Module pricing and publication are simulated; no money is charged and no external publication occurs.
- Production authentication, role authorization, a persistent student database, production RAG, verified government data ingestion, actual BHASHINI integration, real map tiles and production monitoring are not connected.
- The current tests do not constitute full browser, device, security, accessibility or load testing.

