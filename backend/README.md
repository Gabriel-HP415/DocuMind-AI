# DocuMind AI - Backend

FastAPI backend cho hệ thống hỏi đáp tài liệu PDF sử dụng RAG (Retrieval-Augmented Generation).

## Cấu trúc thư mục

```
backend/
├── app/
│   ├── api/v1/routers/     # API endpoints
│   ├── core/               # Config, security
│   ├── db/                 # Session, schema
│   ├── middleware/         # JWT auth
│   ├── models/             # SQLAlchemy models
│   ├── repositories/       # Data access layer
│   ├── schemas/            # Pydantic schemas
│   └── services/           # PDF, FAISS, RAG logic
├── uploads/                # Lưu file PDF
├── faiss_index/            # Lưu vector index
├── scripts/                # Seed admin
├── tests/                  # Unit tests
├── main.py                 # Entrypoint (app)
├── run.py                  # Dev server runner
├── requirements.txt
├── Dockerfile
└── .env.example
```

## Cài đặt trên Windows 11

### Yêu cầu

- Windows 11
- Python 3.11+ (đã thêm PATH khi cài)
- MySQL 8.0+ (local hoặc Docker)
- Ollama + model `llama3` (tùy chọn nếu chạy AI local)
- Git

### Bước 1: Clone & cài thư viện

```powershell
git clone <repo-url>
cd DocuMind-AI\backend

python -m venv .venv
.\.venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
```

### Bước 2: Cấu hình môi trường

```powershell
Copy-Item .env.example .env
```

Sửa `.env`:
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
- `OLLAMA_BASE_URL` (mặc định `http://localhost:11434`)
- `JWT_SECRET_KEY` (đổi sang chuỗi ngẫu nhiên dài)

### Bước 3: Chuẩn bị MySQL

Tạo database:

```sql
CREATE DATABASE documind_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Áp dụng schema:

```powershell
mysql -u root -p documind_ai < app\db\schema.sql
```

Hoặc chạy bằng Python:

```powershell
python scripts\seed_admin.py
```

### Bước 4: Chạy backend

```powershell
python run.py
```

Mở trình duyệt:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Docker Compose

```powershell
docker compose up --build
```

## API Endpoints

| Method | Path | Mô tả |
|--------|------|-------|
| POST | /api/v1/auth/register | Đăng ký |
| POST | /api/v1/auth/login | Đăng nhập (trả JWT) |
| POST | /api/v1/auth/logout | Logout (client xóa token) |
| POST | /api/v1/documents/upload-pdf | Upload PDF |
| GET | /api/v1/documents | Danh sách PDF của user |
| GET | /api/v1/documents/all | Danh sách tất cả PDF (admin) |
| GET | /api/v1/documents/{id} | Chi tiết PDF |
| DELETE | /api/v1/documents/{id} | Xóa PDF |
| POST | /api/v1/chat/ask | Hỏi đáp RAG |
| GET | /api/v1/chat/history/{session_id} | Lịch sử chat |
| GET | /api/v1/chat/sessions | Danh sách phiên chat |
| GET | /api/v1/admin/users | Danh sách users (admin) |
| DELETE | /api/v1/admin/user/{id} | Xóa user (admin) |
| GET | /api/v1/admin/documents/all | Danh sách tất cả tài liệu (admin) |
| GET | /api/v1/health | Health check |

## Test API cơ bản

Sử dụng Swagger UI (`/docs`) hoặc cURL:

```powershell
# Register
Invoke-RestMethod -Uri http://localhost:8000/api/v1/auth/register `
  -Method POST -ContentType "application/json" `
  -Body '{"fullname":"Test User","email":"test@example.com","password":"TestPass123!"}'

# Login
$login = Invoke-RestMethod -Uri http://localhost:8000/api/v1/auth/login `
  -Method POST -ContentType "application/json" `
  -Body '{"email":"test@example.com","password":"TestPass123!"}'
$token = $login.access_token

# Upload PDF
Invoke-RestMethod -Uri http://localhost:8000/api/v1/documents/upload-pdf `
  -Method POST -Headers @{Authorization="Bearer $token"} `
  -Form @{file=Get-Item "C:\path\to\file.pdf"}

# Ask
Invoke-RestMethod -Uri http://localhost:8000/api/v1/chat/ask `
  -Method POST -Headers @{Authorization="Bearer $token"} `
  -ContentType "application/json" `
  -Body '{"document_id":1,"question":"Tóm tắt nội dung chính"}'
```

## Lưu ý

- Backend hiện tại chỉ tập trung vào REST API + AI pipeline. Giao diện frontend đã có sẵn trong `DocuMind-AI/`.
- FAISS index được lưu theo từng `document_id` trong thư mục `faiss_index/`.
- File PDF được lưu bằng hash nội dung để tránh trùng lặp.
- Tích hợp frontend: cập nhật frontend gọi API tại `http://localhost:8000/api/v1` với header `Authorization: Bearer <token>`.
