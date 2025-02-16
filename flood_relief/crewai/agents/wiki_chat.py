from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool
import os
import discord
from dotenv import load_dotenv
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
import json

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("D")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

llm = LLM(model="gpt-4o-mini",
          api_key=OPENAI_API_KEY)
# Create tools
search_tool = SerperDevTool()

# Create the researcher agent
researcher = Agent(
    role="Disaster Researcher",
    goal="Find all information about 2022 Flood in Pakistan",
    backstory="You are a resarcher who has immense knowledege of ccurent and historical disaster facts in Pakistan.",
    tools=[search_tool],
    verbose=True
)


def chat_task(message_content):
    """Chat task"""
    return Task(
        description=f"""
        Process this message: {message_content}
        Reply to the user response. However, make sure it is related to Floods of Pakistan in 2022. 
        Other wise, direct the conversation to volunteering efforts during crises such as floods and earthquakes.
        """,
        agent=researcher,
        expected_output="Try to be as human as possible"
    )


async def process_with_crew(message_content):
    """Process message using CrewAI"""
    try:
        task = chat_task(message_content)
        crew = Crew(
            agents=[researcher],
            tasks=[task],
            verbose=True,
            planning=True
        )
        result = crew.kickoff()
        return result
    except Exception as e:
        return f"Error processing message: {str(e)}"
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return
    
    try:
        # Process the message using CrewAI
        response = await process_with_crew(message)
        await message.channel.send(response)
    except Exception as e:
        await message.channel.send(f"An error occurred: {str(e)}")

def main_():
    try:
        client.run(DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        print("Failed to login: Invalid Discord token")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main_()
