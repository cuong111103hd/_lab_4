# TravelBuddy AI Agent

TravelBuddy is an AI-powered travel assistant built to help you plan your trips in Vietnam effortlessly. The agent enforces budget restrictions, provides bi-directional flight searches, sorts hotels by rating (within budget), and maintains an ongoing budget calculation sheet.

## Architecture
- **Backend:** Python, FastAPI, LangChain, LangGraph (using `MemorySaver` for state preservation).
- **Frontend:** Next.js 14, Tailwind CSS (Summer Streetwear Vibes), Framer Motion. 

## Requirements
- Docker and Docker Compose
- Or if running locally: Node.js 20+, Python 3.11+
- OpenAI API Key

---

## 🚀 Quick Start with Docker (Recommended)

1. **Set up Environment Variables:**
   Create an `.env` file in the `backend/` directory from the example:
   ```bash
   cp backend/.env.example backend/.env
   ```
   Add your `OPENAI_API_KEY` to `backend/.env`.

2. **Run the Application:**
   Run the following command at the root of the project:
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - **Frontend UI:** [http://localhost:3000](http://localhost:3000)
   - **Backend API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 💻 Manual Setup (Without Docker)

### 1. Backend Setting

Navigate to the backend directory:
```bash
cd backend
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Set up your `.env` (make sure your OpenAI API key is added):
```bash
cp .env.example .env
```

Start the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

### 2. Frontend Setting

Navigate to the frontend directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Start the development server:
```bash
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000) in your browser.
