from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start, router
from web_analyst import Webcrew
import discord
from discord_final import DiscordCrew
from wiki_chat import main_
import os

DISCORD_TOKEN = os.getenv("D")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

class ChatState(BaseModel):
    chat: str = ""
    emergency: bool = False

class ChatFlow(Flow[ChatState]):

    @start
    def generate_summary(self):
        print("Generating summary")
        result = Webcrew.kickoff()
        return result
    
    @listen(generate_summary)
    async def discord_emergency(self):
        print("emergency")
        result = DiscordCrew.kickoff()
        return result
    
    @listen("chat")
    def chat(self):
        print("chat")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", 'quit']:
                print("Exiting Chat")
                break
            response = main_()

            return response

# Register Discord event handlers only once at the module level
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # Prevent the bot from responding to its own messages
    if message.author == client.user:
        return
    try:
        # Process the message using DiscordCrew logic
        response = await DiscordCrew.kickoff()
        await message.channel.send(response)
    except Exception as e:
        await message.channel.send(f"An error occurred: {str(e)}")

flow = ChatFlow()
flow.kickoff()

