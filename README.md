# CodeforcesAnalyzer

A full-stack web application for analyzing Codeforces user data, visualizing performance, and providing AI-powered recommendations and chat. The project consists of a React + Vite frontend and a Python Flask backend with ML, GenAI, and FAISS integration.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Setup Instructions](#setup-instructions)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Running the Application](#running-the-application)
- [API & Integration](#api--integration)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

**CodeforcesAnalyzer** helps users analyze their Codeforces contest data, visualize progress, and get personalized recommendations using machine learning and generative AI. It features:
- Data extraction from Codeforces API
- User and problem analytics
- AI-powered chat and recommendations
- Interactive visualizations

---

## Features

### Frontend (React + Vite)
- Modern SPA built with React and Vite
- Dashboard with user statistics and heatmaps
- AI Chat interface for Q&A and recommendations
- Rating and problem recommendation visualizations
- Responsive UI with Tailwind CSS

### Backend (Flask, ML, GenAI)
- REST API built with Flask
- Data extraction and preprocessing from Codeforces
- Machine learning for problem recommendations
- FAISS vector search for GenAI chat
- Integration with Google GenAI and Sentence Transformers
- CSV and FAISS-based data storage

---

## Directory Structure

```
CodeforcesAnalyzer/
├── Backend/
│   ├── app.py                # Main Flask app
│   ├── requirements.txt      # Python dependencies
│   ├── data/                # Data extraction scripts & CSVs
│   ├── db/                  # FAISS index and chunk files
│   ├── GenAI/               # GenAI ingestion and query scripts
│   ├── model/               # ML models
│   └── src/                 # Feature engineering, recommend, visualize
├── Frontend/
│   ├── src/                 # React source code
│   ├── public/              # Static assets
│   ├── package.json         # Frontend dependencies
│   └── ...
└── README.md                # Project documentation
```

---

## Setup Instructions

### Backend Setup
1. **Install Python (>=3.8) and pip**
2. Navigate to the Backend folder:
   ```sh
   cd CodeforcesAnalyzer/Backend
   ```
3. (Optional) Create and activate a virtual environment:
   ```sh
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix/Mac:
   source venv/bin/activate
   ```
4. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
5. **Download/prepare data:**
   - Use `data/extract_data.py` to fetch and preprocess Codeforces data.
   - Ensure `cf_data.csv` and FAISS index files are present in `data/` and `db/`.
6. **Run the backend server:**
   ```sh
   python app.py
   ```
   The server will start on `http://localhost:5000` by default.

### Frontend Setup
1. **Install Node.js (>=18) and npm**
2. Navigate to the Frontend folder:
   ```sh
   cd CodeforcesAnalyzer/Frontend
   ```
3. **Install dependencies:**
   ```sh
   npm install
   ```
4. **Run the frontend dev server:**
   ```sh
   npm run dev
   ```
   The app will be available at `http://localhost:5173`.

---

## Running the Application
- **Development:**
  - Start the backend (`python app.py`)
  - Start the frontend (`npm run dev`)
  - The frontend will communicate with the backend via REST API (CORS enabled)
- **Production:**
  - Build the frontend (`npm run build`) and serve with a static server or integrate with backend

---

## API & Integration
- The backend exposes REST endpoints for data, recommendations, and chat.
- The frontend (see `src/api.js`) communicates with these endpoints.
- GenAI chat and recommendations require proper API keys and model files.

---

## Contributing
Pull requests are welcome! Please open issues for suggestions or bugs.

---

## License
This project is for educational and research purposes.
