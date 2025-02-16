from crewai import Agent, LLM, Task, Crew
import os
import discord
from dotenv import load_dotenv
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
import json
from crewai_tools import SerperDevTool

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("D")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

llm = LLM(model="gpt-4o-mini",
          api_key=OPENAI_API_KEY)

serper_tool = SerperDevTool()

chat_agent = Agent(
    name = "Discord Chat Agent",
    role="Humanitarian Chat Agent",
    goal="Goal is to check historical data and data about 2022 Floods in Pakistan to help others.",
    backstory="You are an expert in volunteer work and disaster management.",
    llm=llm
    #tools=[serper_tool]
)

def create_emergency_task(message_content):
    """Create a task for processing emergency messages"""
    return Task(
        description=f"""
        Process this message: {message_content}
        Chat with the user as humanly as possible. While also giving small tips on keeping safe during floods.
        """,
        agent=chat_agent,
        expected_output=""""""
    )

async def process_with_crew(message_content):
    """Process message using CrewAI"""
    try:
        task = create_emergency_task(message_content)
        crew = Crew(
            agents=[chat_agent],
            tasks=[task],
            verbose=True
            #planning=True
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

def main():
    try:
        client.run(DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        print("Failed to login: Invalid Discord token")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
