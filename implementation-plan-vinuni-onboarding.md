# Kế hoạch triển khai chi tiết — VinUni Onboarding Agent

## 1) Mục tiêu triển khai

Xây dựng hệ thống AI Onboarding theo hướng **augmentation**:
- Trả lời câu hỏi onboarding bằng RAG (quy định học vụ + thủ tục hành chính).
- Dẫn luồng công việc theo checklist cá nhân hóa theo vai trò.
- Có cơ chế phản hồi sai, chuyển bộ phận phụ trách, và đo lường chất lượng.

> Ghi chú: **Data fix cứng** (policy, FAQ, form links, deadlines...) nhóm sẽ bổ sung sau theo từng đợt.

---

## 2) Kiến trúc kỹ thuật đề xuất (MVP)

## 2.1 Thành phần hệ thống
- **Frontend Web**: giao diện chat + checklist + feedback.
- **Backend API**: xử lý session, intent routing, gọi RAG pipeline.
- **RAG Engine**:
  - ingest tài liệu nội bộ
  - chunking + embedding
  - retrieval + rerank
  - answer generation có trích dẫn
- **Data layer**:
  - vector DB cho knowledge chunks
  - relational DB cho user/session/event logs
- **Observability**:
  - log, metrics dashboard, tracing cơ bản.

## 2.2 Luồng xử lý
1. User gửi câu hỏi + context (role, đơn vị/khoa, kỳ).
2. Backend chuẩn hóa câu hỏi, xác định intent.
3. Retriever lấy top-k chunks liên quan.
4. Generator tạo câu trả lời dựa trên chunks + policy prompt.
5. Trả về:
   - câu trả lời ngắn gọn
   - trích dẫn nguồn
   - next step/action
   - tùy chọn `Báo sai` / `Chuyển bộ phận`.

---

## 3) Công nghệ cần dùng

## 3.1 Stack chính
- **Frontend**: Next.js (React + TypeScript), Tailwind CSS.
- **Backend (chốt dùng)**: **FastAPI (Python)**.
- **LLM integration**: OpenAI API (chat + embeddings).
- **Vector DB**: Chroma (local dev) -> có thể nâng cấp Qdrant/Pinecone khi scale.
- **RDBMS**: PostgreSQL.
- **ORM/DB access (chốt dùng)**: **SQLAlchemy**.
- **Auth (MVP)**: mock role-based auth (Student/Staff/Admin), sau đó tích hợp SSO.
- **Monitoring**: OpenTelemetry basic logs + Grafana/Metabase (tùy hạ tầng).

## 3.2 Thư viện đề xuất (nếu dùng Python)
- `fastapi`, `uvicorn`
- `pydantic`
- `langchain` (framework chính cho RAG/orchestration)
- `langgraph` (quản lý workflow nhiều bước: clarify/escalate/checklist)
- `chromadb`
- `sqlalchemy`, `psycopg2-binary`
- `python-dotenv`
- `pytest`

## 3.3 Chuẩn dự án
- Monorepo:
  - `apps/web` (frontend)
  - `apps/api` (backend)
  - `packages/shared` (types/constants/interfaces)
  - `packages/rag` (ingest, retrieval, prompt policy)
- Config môi trường:
  - `.env.example` commit lên repo
  - `.env` local không commit

## 3.4 Boundary kỹ thuật (để tránh trùng code)
- `apps/api`: chỉ chứa REST API, auth/session, validation, rate-limit, event logging.
- `packages/rag`: chỉ chứa ingest/chunk/index/retrieval/rerank/prompt policy/langgraph nodes.
- `packages/shared`: schema dùng chung (DTO, enums, API contracts), **owner chính: Cường**.
- `apps/web`: chỉ chứa UI/UX, không gọi trực tiếp logic RAG; mọi truy vấn đi qua `apps/api`.
- Quy tắc bắt buộc: thay đổi cross-package cần issue riêng + 2 reviewer (owner chính + owner phụ).

---

## 4) Phạm vi MVP và phần để data bổ sung sau

## 4.1 Phạm vi làm ngay
- Chat onboarding cơ bản cho 2 vai trò: `Student`, `Staff`.
- 6-10 intent onboarding phổ biến.
- Trả lời có trích dẫn.
- Feedback `helpful/not helpful`.
- Escalation cơ bản theo intent.

## 4.2 Data fix cứng bổ sung sau (TODO Data)
- Bộ FAQ chính thức theo từng role.
- Danh sách form/link chính thức từng thủ tục.
- Timeline/deadline theo kỳ.
- Danh bạ bộ phận xử lý theo chủ đề.
- Mapping intent -> đơn vị xử lý.

---

## 5) Các bước thực hiện chi tiết (theo sprint)

## Sprint 0 (0.5-1 ngày): Setup
1. Tạo repo + cấu trúc thư mục chuẩn.
2. Setup lint/format/test cơ bản.
3. Thêm CI chạy `lint + unit tests`.
4. Viết `README` + hướng dẫn run local.

**Output:** repo chạy được local, có pipeline CI pass.

## Sprint 1 (2-3 ngày): Backend + RAG khung
1. Tạo endpoint chat `/api/chat`.
2. Xây khung RAG:
   - ingest pipeline (placeholder data)
   - retrieval top-k
   - answer template có citation.
3. Thêm session model + log query/response.
4. Rule an toàn:
   - thiếu context -> hỏi lại
   - thiếu nguồn -> không trả lời chắc chắn.

**Output:** chat API trả lời được với dữ liệu mẫu.

## Sprint 2 (2-3 ngày): Frontend + UX flow
1. Dựng chat UI + panel checklist.
2. Form setup context đầu phiên (role, khoa/đơn vị, kỳ).
3. Hiển thị citation + confidence label (low/med/high).
4. Nút `Báo sai` và `Chuyển bộ phận`.

**Output:** end-to-end demo: hỏi -> trả lời -> citation -> feedback.

## Sprint 3 (2 ngày): Evaluation + hardening
1. Thêm bộ test prompt theo intent.
2. Script eval cơ bản:
   - grounded rate
   - task success proxy
   - latency p50/p95.
3. Cải thiện prompt policy và retrieval.
4. Chuẩn bị demo script + slide.

**Output:** báo cáo metric v1 + demo ổn định.

---

## 6) Phân chia công việc đều, không trùng lặp

Nguyên tắc:
- Mỗi thành viên **sở hữu 1 module chính** + 1 module phụ review chéo.
- Không sửa cùng thư mục trong cùng 1 task nếu không cần thiết.
- Mọi task phải có issue ID và branch riêng.

## 6.1 Bảng ownership chính
| Thành viên | Ownership chính | Ownership phụ (review) | Folder chính |
|---|---|---|---|
| **Đặng Tiến Dũng** | Backend API + orchestration | Review FE integration | `apps/api` |
| **Phạm Hữu Hoàng Hiệp** | RAG pipeline + data ingest | Review eval | `packages/rag` |
| **Phạm Việt Cường** | Evaluation + observability + CI + shared contracts | Review backend quality | `infra`, `scripts`, `.github/workflows`, `packages/shared` |
| **Phạm Trần Thanh Lâm** | Frontend UX + checklist + feedback UI | Review prompt UX outputs | `apps/web` |

## 6.2 Workload cân bằng theo điểm effort (story points)
- Mỗi người mục tiêu: **8-10 points/sprint**.
- Task lớn (>5 points) bắt buộc tách thành 2-3 subtask.
- Review chéo tính effort riêng (1-2 points).

## 6.3 Ma trận task mẫu (không trùng lặp)
| Task ID | Mô tả | Owner | Reviewer | Không đụng vào |
|---|---|---|---|---|
| BE-01 | Tạo endpoint `/api/chat` + schema | Dũng | Cường | `apps/web` |
| RAG-01 | Ingest + chunk + index pipeline | Hiệp | Dũng | `apps/web` |
| FE-01 | Chat UI + context form + citations | Lâm | Hiệp | `apps/api` |
| OPS-01 | CI lint/test + logging dashboard basic | Cường | Lâm | `packages/rag` |

---

## 8) Rủi ro chính và phương án dự phòng

| Rủi ro | Mức độ | Ứng phó |
|---|---|---|
| Thiếu data thật ban đầu | Cao | Dùng data mock schema chuẩn, thay bằng data thật sau mà không đổi code |
| Prompt trả lời lan man | Trung bình | Thêm response template + max tokens + rule hỏi lại |
| Retrieval sai tài liệu | Cao | Tune chunk size, top-k, metadata filter theo role |
| User spam câu hỏi | Cao | Sửa rule base thành local LLM để phân loại câu hỏi |

## 8.1 Risk register mở rộng (khi triển khai thực tế)
| ID | Rủi ro phát sinh | Dấu hiệu nhận biết | Cách giảm thiểu | Owner |
|---|---|---|---|---|
| R-01 | Intent route sai khi user hỏi nhiều ý trong 1 câu | Bot trả lời lệch 1 nửa câu hỏi | Thêm query decomposition + classifier 2 tầng | Hiệp |
| R-02 | Citation không support đúng kết luận | Câu trả lời đúng bề mặt nhưng dẫn nguồn không khớp | Bắt buộc answer-from-context + citation validator | Dũng |
| R-03 | Dữ liệu lỗi thời theo kỳ/đợt | Trả lời sai deadline, sai biểu mẫu mới | Thêm metadata `effective_date`, `version`, `expires_at` | Hiệp |
| R-04 | Timeout/rate-limit từ LLM API | p95 latency tăng cao, request fail | Retry có backoff + fallback response + queue ngắn | Cường |
| R-05 | Lộ dữ liệu nhạy cảm trong log | Log chứa thông tin cá nhân | PII redaction + log minimization + role audit | Cường |
| R-06 | Session lệch trạng thái khi mở nhiều tab | Checklist nhảy bước, mất context | Session lock nhẹ + state merge rule | Lâm |

## 8.2 Mitigation checklist trước khi merge
- [ ] Có fallback khi retrieval rỗng hoặc LLM timeout.
- [ ] Có kiểm tra citation hợp lệ trước khi trả response.
- [ ] Có metadata version cho dữ liệu (date/version/source).
- [ ] Không log dữ liệu cá nhân nhạy cảm.
- [ ] Có test regression cho ít nhất 20 câu hỏi vàng.
- [ ] PR không chạm ngoài boundary nếu chưa có approval.

## 8.3 Runbook sự cố nhanh
1. **LLM lỗi/timeout**: trả về thông báo an toàn + gợi ý `Chuyển bộ phận`; bật retry 1-2 lần.
2. **Vector DB lỗi**: chuyển sang FAQ fallback cứng (nếu có) + gắn cờ degraded mode.
3. **Citation mismatch**: chặn response, yêu cầu retrieve lại với bộ lọc metadata.
4. **Latency tăng đột biến**: giảm top-k, bật cache câu hỏi lặp, ghi lại trace để tối ưu.
5. **Bug production**: rollback bản mới nhất, mở incident ticket, postmortem trong 24h.

## 8.4 Golden set và regression test
- Tạo bộ `golden_questions_v1.json` gồm 50-100 câu:
  - 40% FAQ phổ biến
  - 30% câu mơ hồ cần hỏi lại
  - 20% câu cần escalation
  - 10% câu ngoài phạm vi
- Chạy regression ở CI mỗi PR:
  - grounded rate không giảm > 3%
  - escalation đúng intent >= 85%
  - p95 latency không vượt ngưỡng đã cam kết

---

## 9) Kế hoạch bàn giao demo

- Demo script 5-7 phút gồm:
  1. Setup role/context
  2. Hỏi 2 câu FAQ chuẩn
  3. 1 câu mơ hồ để bot hỏi lại
  4. 1 câu ngoài phạm vi để bot escalate
- Chuẩn bị:
  - 1 video backup 2 phút
  - 1 file metrics snapshot
  - 1 slide kiến trúc + ownership + lessons learned

