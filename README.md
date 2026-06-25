# DocuMind-AI
AI-Powered PDF Question Answering System Using RAG

## Yêu cầu hệ thống

- **Docker** (Docker Desktop) + **Docker Compose v2**
- **RAM**: Tối thiểu 8GB (khuyến nghị 16GB+)
- **Ổ cứng**: 10GB trống

## Cài đặt nhanh

### 1. Clone project
```bash
git clone <repo-url>
cd DocuMind-AI
```

### 2. Tạo file .env (nếu chưa có)
```bash
cp backend/.env.example backend/.env
```

### 3. Khởi chạy
```bash
docker compose up -d
```

Đợi 2-3 phút để:
- MySQL khởi tạo database
- Ollama pull model llama3.2:3b (lần đầu)
- Frontend + Backend khởi động

### 4. Tạo tài khoản admin
```bash
docker exec documind_backend python -m app.scripts.seed_admin
```

### 5. Truy cập
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **Docs API**: http://localhost:8000/docs

**Đăng nhập**: admin@documind.ai / Admin@123

## Cấu trúc dự án

```
DocuMind-AI/
├── frontend/                    # Giao diện người dùng (HTML + Tailwind)
│   ├── landing.html
│   ├── sign_in.html
│   ├── register.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── chat.html
│   ├── admin.html
│   └── DESIGN.md
├── backend/                     # FastAPI REST API
│   ├── app/
│   │   ├── api/v1/routers/     # auth, pdf, chat, admin, health
│   │   ├── core/               # config + security (JWT, bcrypt)
│   │   ├── db/                 # SQLAlchemy async engine + schema.sql
│   │   ├── middleware/         # JWT auth dependencies
│   │   ├── models/             # User, PdfDocument, ChatSession, ChatMessage
│   │   ├── repositories/       # UserRepository, PdfRepository, ChatRepository
│   │   ├── schemas/            # Pydantic schemas
│   │   └── services/
│   │       ├── pdf_processor/  # PyPDF loader + LangChain chunker
│   │       ├── vector_store/   # SentenceTransformers + FAISS
│   │       └── rag/            # LangChain + Ollama Llama3 chain
│   ├── uploads/                # Lưu file PDF
│   ├── faiss_index/            # Lưu vector index
│   ├── scripts/seed_admin.py
│   ├── tests/test_api.py
│   ├── main.py + run.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── .gitignore
│   ├── Dockerfile
│   └── README.md
└── docker-compose.yml
```

## Lệnh Docker thường dùng

```bash
# Xem logs
docker compose logs -f

# Restart
docker compose restart

# Dừng
docker compose down

# Rebuild (sau khi update code)
docker compose up -d --build

# Xóa toàn bộ data
docker compose down -v
```

## Khắc phục lỗi thường gặp

### Lỗi "Connection refused" với Ollama
Đợi 2-3 phút cho Ollama pull model xong:
```bash
docker compose logs ollama
```

### Lỗi database
Kiểm tra MySQL đã healthy chưa:
```bash
docker compose ps
docker compose logs mysql
```

### Tốc độ AI chậm
- Ollama chạy trên CPU. Để nhanh hơn, cần GPU với CUDA.
- Đã tối ưu: streaming response, context giảm, output limit.
    
