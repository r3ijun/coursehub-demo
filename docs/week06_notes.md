# Buổi 6 - Docker, Testing, CI

## Môi trường
- **OS:** Windows
- **Docker version:** Docker Desktop (Compose v2)
- **Python / Node version:** Python 3.12 (image) / Python 3.14 (local venv), Node.js v22

## Kết quả local
- `pytest backend/tests -q`: 2 passed
- `npm test`: 8 passed (0 failed)
- `npm run build`: Thành công, xuất bundle ra `frontend/dist/`
- `docker compose up --build`: Thành công, `backend` đạt trạng thái `healthy` (cổng `8000`) và `frontend` chạy ổn định qua Nginx (cổng `8080`)

## Một luồng tích hợp đã kiểm tra
- **Request:**
  - `GET http://127.0.0.1:8080/api/sections` và `GET http://127.0.0.1:8080/api/students/22000004/enrollments`
  - `POST http://127.0.0.1:8080/api/enrollments` với payload `{"student_id": "22000004", "class_section_id": "WEB-01"}`
  - `DELETE http://127.0.0.1:8080/api/enrollments/22000004/WEB-01`
- **HTTP status:** `200 OK` (GET), `201 Created` (POST), `204 No Content` (DELETE)
- **SQL xác nhận:**
  - Sau POST: Bảng `enrollments` xuất hiện cặp `(22000004, WEB-01)`, `v_section_summary` cập nhật `remaining = 0`, bảng `enrollment_events` ghi nhận sự kiện `CREATED`.
  - Sau DELETE: Xóa bản ghi trong `enrollments`, `remaining` phục hồi về `1`, `enrollment_events` ghi nhận thêm `CANCELLED`.

## Debug / AI
1. **Xung đột cổng 8080 khi chạy `docker compose up`:**
   - **Lỗi gặp phải:** `Bind for 0.0.0.0:8080 failed: port is already allocated`.
   - **Bằng chứng đã xem:** Chạy `netstat -ano | findstr :8080` và `Get-Process -Id 4228` phát hiện dịch vụ nền `MTAgentService` đang chiếm cổng `8080`.
   - **Xử lý & xác minh:** Dừng dịch vụ `MTAgentService` qua `services.msc`, kiểm tra lại `netstat` thấy cổng trống, chạy lại `docker compose up -d` thành công và truy cập được `http://127.0.0.1:8080`.
2. **Lỗi import module khi chạy `pytest`:**
   - **Lỗi gặp phải:** `ModuleNotFoundError: No module named 'backend'` khi gọi `pytest backend/tests -q`.
   - **Bằng chứng đã xem:** Traceback tại dòng `from backend.app.main import app` do thư mục `backend/tests` thiếu tệp nhận diện package.
   - **Xử lý & xác minh:** Bổ sung tệp `backend/tests/__init__.py` theo gợi ý kỹ thuật, chạy lại `pytest backend/tests -q` đạt `2 passed`.

## Pull Request / CI
- **PR:** Nhánh `week06-docker-ci` -> `main`
- **Reviewer:** Thành viên nhóm kiểm tra diff và dựng lại Compose
- **CI run:** Đạt xanh cả 3 job (`backend`, `frontend`, `docker`) trên GitHub Actions