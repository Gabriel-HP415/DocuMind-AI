# DocuMind-AI
AI-Powered PDF Question Answering System Using RAG

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

## Chạy nhanh

```powershell
# Backend
cd DocuMind-AI\backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env
python run.py

# Frontend (mở file HTML trực tiếp hoặc dùng Live Server)
mở file trong thư mục frontend/ bằng trình duyệt
```

Chi tiết cài đặt xem `backend/README.md`.
