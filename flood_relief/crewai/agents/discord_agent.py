from crewai import Agent, LLM, Task, Crew
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


def read_file_as_string(file_path):
    """
    Reads the content of a file and returns it as a string.

    Parameters:
    file_path (str): The path to the file to be read.

    Returns:
    str: The content of the file as a single string.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        return None
    except IOError:
        print(f"An error occurred while reading the file at {file_path}.")
        return None
    
file_path = "../knowledge/data.txt"
json_content = read_file_as_string(file_path=file_path)
print(json_content)

json_source = StringKnowledgeSource(
    content=json_content)

print(json_content)

discord_agent = Agent(
    name = "Discord Agent",
    role="Discord Agent",
    goal="Send Emergeny Messages in  a concise and clear manner",
    backstory="You can speak multiple languages and seek to help people by making them aware of incoming dangers",
    llm=llm,
    knowledge_sources=[json_source]
)

def create_emergency_task(message_content):
    """Create a task for processing emergency messages"""
    return Task(
        description=f"""
        Process this message: {message_content}
        You will receive a JSON that describes resources available and the demand that is required.
        The JSON includes information of the quantity and the location at which the resource is present currently and
        where the resources will go (demand location).
        Make sure the latitudes and longitudes are converted to a town or city name.
        You are tasked with summarizing this in the form of an emergency message to citizens near the demand location.
        You will ask the citizens to move to the location to receive the resources and if anyone wants to volunteer they are free to do so.
        Make sure the emergency broadcast message is both in ENGLISH and URDU.
        """,
        agent=discord_agent,
        expected_output=""""""
    )

async def process_with_crew(message_content):
    """Process message using CrewAI"""
    try:
        task = create_emergency_task(message_content)
        crew = Crew(
            agents=[discord_agent],
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
        response = await process_with_crew(json_content)
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
