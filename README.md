🚀 AI‑RRS: AI Resume Ranking System 🎯

A Flask‑based web application that ranks candidate resumes against a given job description using a hybrid TF‑IDF and BM25 approach. Implements a modern, glassmorphic UI with drag‑and‑drop file uploads and in‑browser previews.

---
## ✨ Features

- **📂 Upload & Drag‑Drop**: Multi‑file upload (PDF, DOCX, DOC, TXT) via drag‑and‑drop or file browser.
- **🔍 Text Extraction**: Robust extraction from PDFs, DOCX, and legacy DOC (via Windows COM), with plain‑text fallback.
- **⚖️ Hybrid Similarity Ranking**: Combines TF‑IDF cosine similarity (60%) with BM25 scores (40%) for relevance scoring.
- **💎 Interactive UI**: Glassmorphic design, progress bars, ranked list view, and document preview modal.
- **🛡️ File Validation & Cleanup**: Extension checks, filename sanitization, upload size limits (16 MB), and automatic cleanup after processing.

---
## 📋 Prerequisites

- **🐍 Python 3.8+**
- **📦 pip** package manager
- **📝 Microsoft Word** (for `.doc` → `.docx` conversion via COM on Windows)
- **📤 Redis & Celery** (optional; for background task processing at scale)

---
## 🛠️ Installation

1. **🔄 Clone the repository**

   ```bash
   git clone https://github.com/your‑username/ai‑rrs.git
   cd ai‑rrs
   ```

2. **🐣 Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate       # Windows
   ```

3. **📥 Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **📚 Setup NLTK stopwords** (one‑time)

   ```bash
   python -c "import nltk; nltk.download('stopwords')"
   ```

5. **⚙️ Configure environment variables** (optional)

   Create a `.env` file in project root:
   ```ini
   FLASK_ENV=development
   UPLOAD_FOLDER=uploads
   MAX_CONTENT_LENGTH=16777216  # 16MB
   SECRET_KEY=your_secret_key
   ```

---
## 🚀 Running the App

```bash
export FLASK_APP=app.py           # Linux/Mac
set FLASK_APP=app.py              # Windows
export FLASK_ENV=development      # optional
flask run --port 5002             # default port 5002
```

Open your browser at **http://localhost:5002** 🔗

---
## ⚙️ Configuration

- **`config.py`**: (optional) holds centralized Flask settings.
- **🛑 Upload Limits**: controlled via `app.config['MAX_CONTENT_LENGTH']`.
- **✅ Allowed Extensions**: set in `ALLOWED_EXTENSIONS`.

---
## 📂 Project Structure

```
ai‑rrs/
├── app.py                    # Flask application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── uploads/                  # Temporary upload folder
│   └── resumes/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js           # (future) move inline scripts here
├── templates/
│   └── index.html
└── utils/
    ├── extract_text.py       # PDF/DOCX/DOC/TXT extraction
    ├── rank_resumes.py       # TF‑IDF + BM25 hybrid ranking
    └── file_validation.py    # Filename cleaning and extension checks
```

---

## 🔌 API Endpoints

- **`GET /`**: Render the upload form.
- **`POST /`**: Accept JD text + files, return ranked results.
- **`GET /preview?path=<file_path>`**: Return HTML preview of an uploaded resume.

---
## 🤝 Contributing

1. Fork the repository 🍴
2. Create a feature branch: `git checkout -b feature/my‑feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my‑feature`
5. Open a Pull Request 📨

Please ensure all new code is covered by unit tests ✅ and passes linting (Flake8, mypy).

---
## 📝 License

[MIT License](LICENSE)
