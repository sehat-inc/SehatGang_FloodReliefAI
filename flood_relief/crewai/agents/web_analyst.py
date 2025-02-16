import os 
from crewai import Agent, Task, Crew, LLM
from crewai_tools import CSVSearchTool
#from tools.flood_data import FloodDataTool
from openai import OpenAI
#from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from dotenv import load_dotenv

load_dotenv()

content = """Uh, yeah... so like, in Sindh, there’s a crazy amount of water in Sukkur, Khairpur, Larkana. Roads are kinda shut down? N-5 something? BBC said something about it",
 "So Balochistan? Man, it's bad. Quetta and uh… Lasbela, Jaffarabad? Can’t even drive! Karachi-Quetta road is totally a mess. RCD Highway, I think? Not sure, but saw it on Dawn News.",
"Dude, Punjab is not doing great either. Multan? Muzaffargarh? Rain is like, EVERYWHERE. Bypass flooded, M-4 highway too. Geo News was talking about it, I think?",
"KPK, wow, Mingora, Malakand? Just chaos. Swat Expressway – blocked? Maybe? Idk, someone was saying something about the Karakoram Highway too. ARY News had a report",
"So, Sindh again? Hyderabad, Mirpurkhas… road situation is kinda crazy. Like, can’t even drive on Hyderabad-Mirpurkhas Road. Tando something Road is just a nightmare too. Heard on Dawn News",
"Balochistan update again: Turbat, Gwadar, Panjgur… just forget about going anywhere. Makran Highway? Not happening. Turbat-Gwadar Road? Mess. BBC said something but not sure exactly.",
"Lahore, Sialkot… even Gujranwala’s drowning in Punjab. GT Road – bad. Lahore Ring Road? No clue if it’s open or not. Think Express Tribune said something about it.",
"Okay so, KPK again. Dir, Chitral, and Kohistan? Flooding’s a whole mood. Lowari Tunnel? Uhh… maybe closed? Can’t say. Geo News mentioned it but no clear updates.",
"KARACHI. It’s bad, man. Thatta, Sujawal – all under water. National Highway? Yea, forget it. Lyari Expressway? Probably not even driveable. ARY News gave a warning about it.",
"Yo, Balochistan again? Zhob, Loralai, Killa Saifullah? Not looking good. Roads? Um, Zhob-DI Khan Road? And N-50 Highway is… I think it’s shut? BBC had something about it",
"Abbottabad, Mansehra, Battagram – it’s looking bad, really bad. N-35? Maybe don’t try driving there? Abbottabad-Mansehra Road? Uh, avoid if possible. Geo News, I think, mentioned it",
"Dadu, Sehwan, Jamshoro in Sindh? Bro, it’s like a swimming pool. Indus Highway’s pretty much useless now. Dadu-Sehwan Road? Yeah, good luck. Express Tribune said something about it.",
" ALSO, why is no one talking about how pineapple on pizza is actually good? Like, y’all need to stop hating.",
"Meanwhile, my friend just got a new car—bad timing, bro, roads are underwater. ALSO, why do cats always sit in boxes? Scientists need to study this ASAP.",
"Jamshoro = WRECKED. Indus Highway? Yeah, don’t even try. Dadu-Sehwan Road? RIP. Express Tribune covered it. ALSO, did y’all know that octopuses have three hearts? Just found out and I’m shook."""

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

string_source = StringKnowledgeSource(
    content=content
)

llm = LLM(model="gpt-4o-mini",
          api_key=OPENAI_API_KEY)

web_analyst = Agent(
    role="Disaster Situation Analyst",
    goal="""
    As an experienced disaster situation analyst, your job is 
    to analyze historical flood data related to Pakistan.
    You will track information on affected areas, blocked roads, 
    and assess the severity of past floods to inform future preparedness.
    """,
    backstory="An expert in analyzing information from reports, documents, and past records.",
    verbose=True,
    llm=llm,
    knowledge_sources=[string_source]
)

fetch_update_task = Task(
    description="""
    You are a disaster situation analyst. Given the following tweets about flood conditions in Pakistan, please:
    1. Organize the information by location specified. In this case it is Sindh.
    2. For the location specified, provide a concise summary of the flood conditions—including details on affected areas and road conditions.
    3. Exclude any off-topic or irrelevant comments.
    """,
    agent=web_analyst,
    expected_output="Provide your answer in a clear, structured format with headers for each location."
)

Webcrew = Crew(
    agents=[web_analyst],
    tasks=[fetch_update_task],
    verbose=True,
    planning=True
)

Webcrew.kickoff()