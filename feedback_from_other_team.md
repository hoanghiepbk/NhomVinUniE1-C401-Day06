# Feedback Analysis - Team VinUni-E1

Tài liệu tổng hợp đánh giá và góp ý từ các đội thi dành cho dự án **VinUni Onboarding Agent**.

---

## 1. Bảng điểm chi tiết

| Nhóm đánh giá | Tiêu chí 1 | Tiêu chí 2 | Tiêu chí 3 | 1 Điều team làm tốt | Gợi ý cải thiện |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **Vinuni-F1** | 3 | 2 | 3 | Pain point có, rõ ràng. | RAG thuần. Project này không cần dùng LangGraph. |
| **VinUni_E3** | 2 | 2 | 2 | Luồng LangGraph rõ ràng. | Nên làm pain point tốt hơn, tập trung vào user. |
| **VinUni F1** | 4 | 3 | 3 | Có khả năng chạy thực tế cao. | Nên chặn sớm bằng 1 con LLM xác định intent. |
| **VinUni_F1** | 4 | 2 | 3 | Giao diện đơn giản, dễ dùng. | Cải thiện quy trình chống spam. |
| **VinUni_F1** | 4 | 3 | 3 | Có danh sách checklist động. | Chưa có gợi ý để giúp người dùng đi đúng hướng. |
| **VINUNI_F3** | 2 | 2 | 2 | Có Architecture diagram tốt. | Handle spam, demo chưa show được cách xử lý lỗi. |
| **VinUni F2** | 3 | 4 | 3 | Có thể match nhiều role. | Input từ .txt không phải từ .pdf. |
| **VinUni F3** | 3 | 4 | 4 | Phân loại rõ các đối tượng. | Nên có thêm chức năng báo cáo khi thông tin sai. |
| **VinUniF1** | 4 | 4 | 4 | Không trả lời lan man. | Đầu vào nên kiểm chứng dữ liệu đúng hay chưa. |
| **VinUni E3** | 5 | 4 | 5 | Giải pháp hợp lý, sát thực tế. | Xử lý khi dk-sis quá tải/sập. |

---

## 2. Tổng kết & Hành động tiếp theo

Dựa trên bảng feedback, team E1 có thể tập trung vào các nhóm vấn đề sau:

### ✅ Thế mạnh cần phát huy
* **Tính thực tế:** Giải pháp sát sườn, có khả năng ứng dụng thực tế cao (Production-ready).
* **Kiến trúc hệ thống:** Sơ đồ Architecture diagram và việc chia role/đối tượng được đánh giá cao về sự chuyên nghiệp.
* **UI/UX:** Giao diện đơn giản, tập trung vào checklist động giúp người dùng dễ theo dõi nhiệm vụ.

### 🛠️ Các điểm cần cải thiện (Action Items)
1. **Tối ưu hóa LLM Flow:** - Có ý kiến cho rằng LangGraph có thể hơi "overkill" cho bài toán này, hoặc cần thêm node **