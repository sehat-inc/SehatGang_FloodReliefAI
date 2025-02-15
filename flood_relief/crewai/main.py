from crewai import Crew
from agents import web_analyst, discord_agent


def start_workflow():
    crew = Crew(
    agents=[web_analyst.web_analyst, discord_agent.discord_agent],
    tasks=[web_analyst.fetch_update_task, discord_agent.create_emergency_task],
    verbose=True,
    planning=True
)