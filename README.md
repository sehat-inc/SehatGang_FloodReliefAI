# FloodRelief AI

## Project Overview
This project is designed for flood disaster management. It integrates several components:
- A Flask-based frontend for user interaction.
- A FastAPI backend handling GIS operations, Postgres integration, and resource allocation.
- A CrewAI-based agent workflow communicating via Discord to analyze and process flood data from multiple agents.

## Technologies Used
- Python
- Flask (Frontend)
- FastAPI (Backend)
- SQLAlchemy & GeoAlchemy2 (Database & GIS operations)
- PostgreSQL (Database)
- Or-Tools (Optimization for resource allocation)
- Geopy (Geocoding)
- CrewAI (Agent-based workflow and Discord communication)

## Running the Project
1. Ensure you have all Python dependencies installed (use requirements.txt or pip install).
2. Set up environment variables including `DATABASE_URL`, `OPENAI_API_KEY`, and Discord configuration needed for CrewAI.
3. Start the backend server:
   - Navigate to `flood-relief-ai/flood_relief/backend`
   - Run: `uvicorn main:app --reload`
4. Start the Flask frontend:
   - Navigate to `flood-relief-ai/flood_relief/frontend`
   - Run: `python app.py`
5. For agent workflows, run the CrewAI agents (located under `flood-relief-ai/flood_relief/crewai`) to connect to Discord and execute tasks.

## Experimenting with our Emergency Agent
1. You can join our [Test Discord Server](https://discord.gg/GXZSAbQj) to recieve emergency alerts. These agents have been connected with our Geospatial OR Tools.
