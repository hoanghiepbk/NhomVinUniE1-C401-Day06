# Prototype README

## Mô tả prototype (2-3 câu)
Prototype `VinUni Onboarding Agent` là trợ lý AI hỗ trợ onboarding theo vai trò cho tân sinh viên và nhân viên mới tại VinUni. Hệ thống gồm setup wizard, checklist động theo ngữ cảnh (role/unit/housing), và chat RAG có citation từ dữ liệu FAQ seed để trả lời có căn cứ. Mục tiêu của bản này là kiểm chứng trải nghiệm onboarding end-to-end và giảm câu hỏi lặp cho bộ phận hỗ trợ.

## Level
Working

## Link prototype
- GitHub repo: https://github.com/hoanghiepbk/NhomVinUniE1-C401-Day06.git
- Diagram: `diagram.png`
- Deployed app: https://c401-c4-lab05-demo.vercel.app/
- Screenshot demo: `demo-screenshot`

## Tools và API đã dùng
- Tools:
  - Frontend: React, Vite
  - Backend: FastAPI, Uvicorn
  - AI/RAG: LangChain, LangGraph
  - Testing: Pytest
  - Deployment/config: Vercel (`vercel.json`)
- API:
  - Google Generative AI (Gemini) qua `langchain-google-genai` / `google-generativeai`
  - API nội bộ của hệ thống: `/api/onboarding/*`, `/api/chat`, `/api/actions/*`, `/api/retrieve/debug`

## Phân công: ai làm gì
- Đặng Tiến Dũng: Backend API + orchestration, tích hợp FE (trọng tâm `apps/api`)
- Phạm Hữu Hoàng Hiệp: RAG pipeline + data ingest, evaluation (trọng tâm `packages/rag`)
- Phạm Việt Cường: Evaluation + observability + CI + shared contracts, chất lượng backend (trọng tâm `infra`, `scripts` một phần, `.github/workflows`, `packages/shared`)
- Phạm Trần Thanh Lâm: RAG pipeline + slides + Frontend UX + checklist + feedback UI (trọng tâm `apps/web`)
