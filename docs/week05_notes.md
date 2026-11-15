##Kết quả kiểm thử luồng Frontend – API – PostgreSQL
- **GET `/courses`, `/sections`, `/students/22000004/enrollments`:** Hiển thị đúng danh sách lớp và số chỗ còn lại từ `v_section_summary`.
- **POST `/enrollments` (`22000004` - `WEB-01`):** Trả về `201 Created`, bảng `enrollments` thêm bản ghi mới, `remaining` giảm từ `1` xuống `0`, bảng `enrollment_events` ghi nhận sự kiện `CREATED`.
- **DELETE `/enrollments/22000004/WEB-01`:** Trả về `204 No Content`, xóa bản ghi khỏi `enrollments`, `remaining` về `1`, `enrollment_events` ghi nhận `CANCELLED`.
- **Xử lý tranh chấp (HTTP 409):** Khi 2 tab cùng mở lớp `RACE-01` còn 1 chỗ, tab bấm sau nhận `HTTP 409` và tự động cập nhật nút sang `Hết chỗ`.