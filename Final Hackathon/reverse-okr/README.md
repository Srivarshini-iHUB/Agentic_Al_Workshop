# Reverse OKR Hackathon Project

## Project Overview
This project implements a Reverse OKR (Objectives and Key Results) system using a pipeline of 5 AI agents. The system analyzes exploration logs, infers learning themes and intents, maps knowledge graphs, generates actionable learning outcomes, and finally produces retrospective OKRs to guide learning and development.

The project consists of a backend API built with FastAPI and a frontend React application built with React + Vite.



## workflow

                    [ User Input: Exploration Logs ]
         (YouTube URLs, GitHub Repos, PDFs, Figma files, etc.)
                                   ↓
              ┌─────────────────────────────────────┐
              │ 1. Exploration Log Aggregator Agent │
              └─────────────────────────────────────┘
                Input: Raw Logs (URLs, text, files)
               Output: JSON of structured activities
                                   ↓
              ┌───────────────────────────────────────┐
              │ 2. Intent & Theme Inference Agent (RAG)│
              └───────────────────────────────────────┘
                  Input: Aggregated Activities JSON
                  Output: Inferred themes + intents
                                   ↓
              ┌──────────────────────────────────────┐
              │ 3. Knowledge Graph Mapper Agent      │
              └──────────────────────────────────────┘
                   Input: Themes + Intents
              Output: Skill-concept-topic Graph JSON
                                   ↓
              ┌────────────────────────────────────────┐
              │ 4. Outcome Potential Generator Agent   │
              └────────────────────────────────────────┘
             Input: Knowledge Graph + Inferred Themes
         Output: Actionable learning outcome suggestions
                                   ↓
              ┌──────────────────────────────────────┐
              │ 5. Retro-OKR Generator Agent (RAG)  │
              └──────────────────────────────────────┘
         Input: Outcomes + Knowledge Graph + Intents
                Output: Final Retrospective OKRs
                                   ↓
           ┌───────────────────────────────────────┐
           │     UI Dashboard (Frontend)           │
           │   - Submit Logs                       │
           │   - Visualize Knowledge Graph         │
           │   - View Retrospective OKRs           │
           └───────────────────────────────────────┘



## Agent Tasks

### 1. Exploration Aggregator Agent
- **Purpose:** Aggregates raw exploration logs (e.g., URLs, documents) into a structured JSON format describing activities with type, title, and metadata.
- **Input:** List of exploration logs (strings).
- **Output:** JSON object with structured activities.

### 2. Intent and Theme Inference Agent
- **Purpose:** Infers learning themes and intent from the structured activities JSON.
- **Input:** List of activity JSON objects.
- **Output:** Inferred themes and intents as JSON.

### 3. Knowledge Graph Mapper Agent
- **Purpose:** Maps the inferred themes to a knowledge graph representing concepts and skills.
- **Input:** Themes JSON (list or dict).
- **Output:** Knowledge graph nodes and links as JSON.

### 4. Outcome Generator Agent
- **Purpose:** Suggests 3-5 actionable learning outcomes based on the knowledge graph.
- **Input:** Knowledge graph JSON.
- **Output:** List of actionable learning outcomes with specific skills, activities, and expected improvements.

### 5. Retro-OKR Generator Agent
- **Purpose:** Generates 3-5 specific, measurable OKRs based on the learning outcomes.
- **Input:** Learning outcomes JSON.
- **Output:** List of OKRs with objectives and key results.

## Running the Backend

### Prerequisites
- Python 3.8+
- Install dependencies:
  ```bash
  pip install -r backend/requirements.txt
  ```

### Start the Backend Server
From the `Final Hackathon/reverse-okr` directory, run:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
This will start the FastAPI backend server on `http://localhost:8000`.

## Running the Frontend

### Prerequisites
- Node.js and npm or yarn installed

### Install Dependencies
Navigate to the frontend directory and install dependencies:
```bash
cd frontend
npm install
# or
yarn install
```

### Start the Frontend Development Server
```bash
npm run dev
# or
yarn dev
```
The frontend will be available at `http://localhost:3000` (or the port shown in the terminal).

## Test Flow Script

The `backend/test_flow.py` script demonstrates the full pipeline by sequentially calling the backend API endpoints:

1. Aggregates exploration logs into structured activities.
2. Infers intent and themes from activities.
3. Maps themes to a knowledge graph.
4. Generates actionable learning outcomes.
5. Generates retrospective OKRs.

Run the script with:
```bash
python backend/test_flow.py
```
Ensure the backend server is running before executing the script.

## Backend API Endpoints

| Endpoint           | Method | Description                          |
|--------------------|--------|----------------------------------|
| `/api/aggregate`       | POST   | Aggregates exploration logs       |
| `/api/infer-intent`    | POST   | Infers intent and themes          |
| `/api/map-graph`       | POST   | Maps themes to knowledge graph    |
| `/api/generate-outcomes` | POST   | Generates learning outcomes       |
| `/api/generate-okr`    | POST   | Generates retrospective OKRs      |

## Contact

For questions or contributions, please contact the project team.

---
