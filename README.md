# TravelBuddy AI Agent

TravelBuddy is an AI-powered travel assistant built to help you plan your trips in Vietnam effortlessly. The agent acts on your instructions to enforce budget restrictions, find bi-directional flights, filter hotels by rating and budget, discover local food using real-time search, and calculate ongoing trip expenses dynamically.

## Key Features
- **✈️ Flight Search:** Bi-directional flight searches across top Vietnamese airlines.
- **🏨 Hotel Booking:** Filters and sorts hotels based on user budget and ratings.
- **🍜 Local Food Discovery:** Real-time web search (powered by Tavily) to find authentic local food and estimate daily meal budgets.
- **💰 Budget Calculation:** Automatically aggregates multi-day trip costs and enforces user limits.
- **🔄 Dynamic UI Updates:** Pushes real-time context to the frontend as the agent decides on flights and hotels.

## Architecture
- **Backend:** Python, FastAPI, LangChain, LangGraph (using `MemorySaver` for state preservation and agentic workflows).
- **Frontend:** Next.js 14, Tailwind CSS (Summer Streetwear Vibes), Framer Motion. 

## Requirements
- Docker and Docker Compose (Recommended)
- Or if running locally: Node.js 20+, Python 3.11+
- `OPENAI_API_KEY` (Required for LLM)
- `TAVILY_API_KEY` (Required for Local Food Search)

---

## 🚀 Quick Start with Docker (Recommended)

1. **Set up Environment Variables:**
   Create an `.env` file in the `backend/` directory based on the example:
   ```bash
   cp backend/.env.example backend/.env
   ```
   Add your API keys to `backend/.env`:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

2. **Run the Application:**
   From the root of the project, run:
   ```bash
   docker-compose up --build
   ```

3. **Access the Application:**
   - **Frontend UI:** [http://localhost:3000](http://localhost:3000)
   - **Backend API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 💻 Manual Setup (Without Docker)

### 1. Backend Setup

Navigate to the backend directory:
```bash
cd backend
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Set up your `.env` (make sure both `OPENAI_API_KEY` and `TAVILY_API_KEY` are provided):
```bash
cp .env.example .env
```

Start the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup

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
