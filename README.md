# VinUni Onboarding Agent (Prototype)

Integrated AI Assistant for role-based onboarding (New Students / New Staff). Features a RAG-powered chat, setup wizard, and dynamic checklist.

## 1) Setup & Installation

### Backend
**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend
```bash
cd apps/web
npm install
```

## 2) Run Local Like Vercel (Recommended)

To simulate the Vercel environment locally (using `vercel.json` routing and a single port):

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Run Dev Server**:
   ```bash
   vercel dev
   ```
   This will start both backend and frontend, and proxy `/api/*` requests automatically.
   Access the application at: **http://localhost:3000**

---

## 3) Manual Maintenance (Separate Servers)

If you prefer to run the components separately:

### Backend
```bash
source venv/bin/activate
PYTHONPATH=. python3 -m uvicorn apps.api.main:app --reload
```

### Frontend
```bash
cd apps/web
npm run dev
```

## 4) Testing & Verification

### Automated Tests
```bash
PYTHONPATH=. python3 -m pytest tests/test_onboarding_flow.py
```

### Manual Verification
1. Open the UI.
2. Complete the **Setup Wizard** (4 questions).
3. Interact with the **AI Agent** (e.g., "Lịch orientation xem ở đâu?").
4. Verify the **Checklist** on the left panel updates based on your role.

## 5) Key Features
- **Role-based Setup**: Tailored onboarding for Students vs. Staff.
- **Dynamic Checklist**: Tasks generated based on role, department, and housing status.
- **RAG with Citations**: Answers are grounded in VinUni FAQ data.
- **Vercel Native**: Configured for serverless deployment via `vercel.json`.

## 6) API Structure
- `GET /api/onboarding/setup-questions`: Initialize wizard.
- `POST /api/onboarding/initialize`: Create session & checklist.
- `GET /api/onboarding/checklist/{session_id}`: Track progress.
- `POST /api/chat`: Context-aware chat.

## 7) Vercel Production Deployment
Connect this repository to Vercel. It will automatically detect `vercel.json`.
- **Build Command**: `cd apps/web && npm install && npm run build`
- **Output Directory**: `apps/web/dist`
