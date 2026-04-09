# SPEC — AI Product Hackathon

**Nhóm:** C4-C401  
**Track:** ☐ VinFast · ☐ Vinmec · ☑ VinUni-VinSchool · ☐ XanhSM · ☐ Open  

**Problem statement (1 câu):** *Tân sinh viên và nhân viên mới tại VinUni phải lục nhiều nguồn (portal, email, FAQ) để biết việc cần làm và câu hỏi thường gặp; hiện support trả lời lặp lại và dễ thiếu ngữ cảnh theo vai trò — prototype **VinUni Onboarding Agent** dùng RAG + wizard + checklist động để trả lời có trích dẫn nguồn và hướng dẫn theo role/unit/housing.*

---

## 1. AI Product Canvas

|   | Value | Trust | Feasibility |
|---|-------|-------|-------------|
| **Câu hỏi** | User nào? Pain gì? AI giải gì? | Khi AI sai thì sao? User sửa bằng cách nào? | Cost/latency bao nhiêu? Risk chính? |
| **Trả lời** | *Tân SV / NV mới — mất thời gian tìm lịch orientation, học phí, IT, KTX; AI trả lời theo ngữ cảnh session (role, đơn vị, KTX) và gắn checklist việc cần làm.* | *RAG có citation từ FAQ seed; user bấm **Báo sai** (feedback) hoặc **Chuyển bộ phận** (escalation); có thể mở rộng log DB để học từ correction.* | *Prototype: retrieval + LLM call theo từng câu hỏi — latency phụ thuộc provider; risk: hallucinate nếu không đủ chunk hoặc câu hỏi ngoài FAQ.* |

**Automation hay augmentation?** ☐ Automation · ☑ Augmentation  

**Justify:** *Augmentation — user luôn thấy câu trả lời kèm nguồn (RAG), checklist do rule + wizard tạo ra; user quyết định tin và làm theo link chính thức.*

**Learning signal:**

1. User correction đi vào đâu? *Hiện prototype: `POST /api/actions/report-error` và `/api/actions/transfer` in ra log; production nên ghi DB/analytics.*
2. Product thu signal gì để biết tốt lên hay tệ đi? *Tỷ lệ “Báo sai”, tỷ lệ escalation, thời gian hoàn thành checklist, repeat question cùng chủ đề.*
3. Data thuộc loại nào? ☐ User-specific · ☑ Domain-specific (FAQ VinUni seed) · ☐ Real-time · ☑ Human-judgment (feedback/escalate) · ☐ Khác: *session answers (role, unit, term, housing)*  

   Có marginal value không? (Model đã biết cái này chưa?) *Giá trị marginal nằm ở **kết hợp** role + unit + housing với đúng đoạn FAQ và checklist — không chỉ QA chung chung.*

---

## 2. User Stories — 4 paths

### Feature: *Setup Wizard + checklist động*

**Trigger:** *User mở UI → trả lời 4 câu (role, unit, term, housing) → `POST /api/onboarding/initialize` tạo session + checklist.*

| Path | Câu hỏi thiết kế | Mô tả |
|------|-------------------|-------|
| Happy — AI đúng, tự tin | User thấy gì? Flow kết thúc ra sao? | *Checklist hiển thị đúng template SV/NV; nếu chọn KTX = Có thì thêm task KTX; progress % cập nhật khi hoàn thành (theo thiết kế UI).* |
| Low-confidence — AI không chắc | System báo "không chắc" bằng cách nào? User quyết thế nào? | *Chat RAG có thể trả lời ngắn + trích dẫn; nếu retrieval yếu, product có thể hiển thị ít citation hoặc gợi ý hỏi bộ phận (mở rộng).* |
| Failure — AI sai | User biết AI sai bằng cách nào? Recover ra sao? | *Thông tin sai so với portal chính thức → user **Báo sai**; không thay thế nguồn chính thức.* |
| Correction — user sửa | User sửa bằng cách nào? Data đó đi vào đâu? | *Feedback text gửi API; sau này gắn ticket/CMS để cập nhật FAQ seed.* |

### Feature: *Chat RAG có citation (VinUni FAQ seed)*

**Trigger:** *User gõ câu hỏi (vd: “Lịch orientation xem ở đâu?”) → `POST /api/chat` với `session_id` để giữ ngữ cảnh.*

| Path | Câu hỏi thiết kế | Mô tả |
|------|-------------------|-------|
| Happy — AI đúng, tự tin | User thấy gì? Flow kết thúc ra sao? | *Câu trả lời grounded, có meta/citation theo chunk FAQ; user đi tiếp checklist.* |
| Low-confidence — AI không chắc | System báo "không chắc" bằng cách nào? User quyết thế nào? | *Ít hit retrieval → trả lời thận trọng hoặc gợi ý liên hệ; có endpoint debug `POST /api/retrieve/debug` cho dev.* |
| Failure — AI sai | User biết AI sai bằng cách nào? Recover ra sao? | *Hallucination hoặc trích sai đoạn → **Báo sai**; ưu tiên link portal trong checklist.* |
| Correction — user sửa | User sửa bằng cách nào? Data đó đi vào đâu? | *Cùng luồng report-error; cập nhật nội dung seed / quy trình nội bộ.* |

### Feature: *Escalation — chuyển bộ phận*

**Trigger:** *User bấm **Chuyển bộ phận** → `POST /api/actions/transfer`.*

| Path | Câu hỏi thiết kế | Mô tả |
|------|-------------------|-------|
| Happy — AI đúng, tự tin | User thấy gì? Flow kết thúc ra sao? | *Xác nhận đã escalate (prototype trả `escalated`).* |
| Low-confidence — AI không chắc | System báo "không chắc" bằng cách nào? User quyết thế nào? | *User chủ động chuyển khi không đủ tin chatbot.* |
| Failure — AI sai | User biết AI sai bằng cách nào? Recover ra sao? | *Luồng nhân sự tiếp nhận case (cần tích hợp ticket thật).* |
| Correction — user sửa | User sửa bằng cách nào? Data đó đi vào đâu? | *Lý do escalation lưu để định tuyến đúng team.* |

---

## 3. Eval metrics + threshold

**Optimize precision hay recall?** ☑ Precision · ☐ Recall  

**Tại sao?** *Ưu tiên **đúng và có căn cứ** (FAQ + citation) hơn là trả lời dài lan man — sai thông tin onboarding (học phí, deadline) tốn support và niềm tin.*

**Nếu sai ngược lại thì chuyện gì xảy ra?** *Chọn recall quá cao → trả lời nhiều nhưng sai/ngụy — user làm sai thủ tục.*

| Metric | Threshold | Red flag (dừng khi) |
|--------|-----------|---------------------|
| *Tỷ lệ câu trả lời có ít nhất 1 citation khớp retrieval (manual sample)* | *≥80% trên bộ câu hỏi onboarding chuẩn* | *<60% trong 1 sprint* |
| *Tỷ lệ “Báo sai” / số câu chat* | *≤5% sau khi ổn định FAQ* | *>15% trong 1 tuần* |
| *Pass automated flow (wizard + chat + actions)* | *100% CI test onboarding* | *Test fail liên tục* |
| *Latency p95 chat (prototype)* | *<5s (tùy provider)* | *>15s thường xuyên* |

---

## 4. Top 3 failure modes

*"Failure mode nào user KHÔNG BIẾT bị sai? Đó là cái nguy hiểm nhất."*

| # | Trigger | Hậu quả | Mitigation |
|---|---------|---------|------------|
| 1 | *Câu hỏi ngoài FAQ seed hoặc policy đổi mà seed chưa cập nhật* | *Model tự suy diễn, trông hợp lý nhưng sai* | *Ràng buộc RAG + hiển thị citation; khi retrieval trống → từ chối trả lời chắc chắn và gợi ý portal/escalation.* |
| 2 | *Nhầm role (SV vs Staff) hoặc checklist không khớp thực tế đơn vị* | *User bỏ sót việc hoặc làm sai quy trình* | *Wizard bắt buộc role; mở rộng checklist theo unit; kiểm định với owner HR/Student Affairs.* |
| 3 | *User tin hoàn toàn chat, không đối chiếu portal chính thức* | *Sai deadline/học phí dù AI “tự tin”* | *Copy UX: luôn nhắc nguồn chính thức; checklist dẫn link portal; metric “Báo sai”.* |

---

## 5. ROI 3 kịch bản

|   | Conservative | Realistic | Optimistic |
|---|-------------|-----------|------------|
| **Assumption** | *50 user onboarding/kỳ, 50% dùng đủ wizard + chat* | *200 user/kỳ, 70% dùng* | *500+ user/kỳ, 85% dùng, tích hợp ticket thật* |
| **Cost** | *Chi phí inference + bảo trì seed nhỏ* | *Tăng query chat + retrieval* | *Scale + monitoring + CMS FAQ* |
| **Benefit** | *Giảm 1–2 giờ hỏi đáp lặp/tuần cho bộ phận liên quan* | *Giảm 5–10 giờ + tăng tỷ lệ hoàn thành checklist đúng hạn* | *Giảm đáng kể ticket FAQ lặp, tăng NPS onboarding* |
| **Net** | *ROI dương nếu cost inference được kiểm soát* | *Cân bằng khi có owner nội dung FAQ* | *Cần đầu tư sản phẩm + vận hành* |

**Kill criteria:** *Sau 2 tháng: tỷ lệ “Báo sai” + escalation cao mà không cải thiện nội dung; hoặc cost vận hành (LLM + người duyệt FAQ) vượt rõ ràng giá trị giờ support tiết kiệm được.*

---

## 6. Mini AI spec (1 trang)

**VinUni Onboarding Agent** là trợ lý onboarding theo vai trò cho **tân sinh viên** và **nhân viên mới**: người dùng trả lời wizard (role, khoa/đơn vị, kỳ, nhu cầu KTX), hệ thống tạo **session** và **checklist** động (thêm bước KTX nếu cần). **Chat** dùng **RAG** trên file seed FAQ (`data/vinuni_freshman_faq_seed.json`), trả lời có ngữ cảnh session và trích dẫn nguồn. **Trust:** không thay thế portal chính thức — citation và checklist dẫn link; **Báo sai** và **Chuyển bộ phận** là lớp an toàn. **Quality:** ưu tiên **precision** (đúng, có căn cứ) hơn khối lượng câu trả lời; đo bằng sample có citation, tỷ lệ feedback, và test tự động luồng onboarding. **Data flywheel:** FAQ seed cập nhật từ feedback/escalation và owner domain; session answers giúp cá nhân hóa checklist và prompt context — mở rộng sau bằng analytics và kho tri thức có quản trị phiên bản.

**API chính (tham chiếu code):** `GET /api/onboarding/setup-questions`, `POST /api/onboarding/initialize`, `GET /api/onboarding/checklist/{session_id}`, `POST /api/chat`, `POST /api/actions/report-error`, `POST /api/actions/transfer`, `POST /api/retrieve/debug` (debug).

---

*Tài liệu này điền theo cấu trúc `01-spec-template.md` và nội dung thực tế của dự án VinUni Onboarding Agent (README + `apps/api` + `packages/rag`).*
