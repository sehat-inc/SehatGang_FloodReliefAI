import faiss
import numpy as np
import pandas as pd
import random
import os
from sentence_transformers import SentenceTransformer
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class FloodDataTool:
    def __init__(self, api_key):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = OpenAI(api_key=api_key)
        self.data = pd.DataFrame({
            'text': [
            "Uh, yeah... so like, in Sindh, there’s a crazy amount of water in Sukkur, Khairpur, Larkana. Roads are kinda shut down? N-5 something? BBC said something about it",
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
            "Jamshoro = WRECKED. Indus Highway? Yeah, don’t even try. Dadu-Sehwan Road? RIP. Express Tribune covered it. ALSO, did y’all know that octopuses have three hearts? Just found out and I’m shook."
        ]})
        
        self.index, self.embeddings = self._build_index()
        
        self.live_updates = [
            {"timestamp": "2022-08-15 12:00", "location": "Sindh", "message": "Severe flooding in Sukkur. Avoid N-5 Highway!"},
            {"timestamp": "2022-08-16 14:30", "location": "Balochistan", "message": "Lasbela heavily flooded. RCD Highway closed."},
            {"timestamp": "2022-08-17 09:15", "location": "Punjab", "message": "Jhang River overflow reported. Roads partially blocked."},
            {"timestamp": "2022-08-18 10:45", "location": "KPK", "message": "Chitral valley flooding. Dangerous road conditions on Karakoram Highway."},
            {"timestamp": "2022-08-19 16:00", "location": "Sindh", "message": "Floodwaters rising in Larkana. Roads leading to Shikarpur submerged!"},
            {"timestamp": "2022-08-20 11:45", "location": "Balochistan", "message": "Heavy rains in Quetta causing flash floods. Avoid Sariab Road!"},
            {"timestamp": "2022-08-21 08:30", "location": "Punjab", "message": "Lahore underpass near Ferozepur Road flooded. Severe traffic congestion."},
            {"timestamp": "2022-08-22 14:20", "location": "KPK", "message": "Swat River overflowing! Mingora at risk of flooding. Stay indoors!"},
            {"timestamp": "2022-08-23 09:10", "location": "Sindh", "message": "Badin district facing extreme waterlogging. Evacuations underway."},
            {"timestamp": "2022-08-24 17:30", "location": "Balochistan", "message": "Harnai floods damaging infrastructure. Travel restrictions in place!"},
            {"timestamp": "2022-08-25 12:40", "location": "Punjab", "message": "Sargodha hit by continuous rainfall. Roads waterlogged."},
            {"timestamp": "2022-08-26 06:55", "location": "KPK", "message": "Landslides in Shangla due to heavy rain. Karakoram Highway blocked!"},
            {"timestamp": "2022-08-27 18:20", "location": "Sindh", "message": "Hyderabad-Mirpurkhas road flooded. Traffic diversions in place."},
            {"timestamp": "2022-08-28 07:15", "location": "Balochistan", "message": "Gwadar coastal areas at risk due to rising water levels!"},
            {"timestamp": "2022-08-29 15:45", "location": "Punjab", "message": "Multan underpass flooded near Nishtar Road. Severe delays expected."},
            {"timestamp": "2022-08-30 10:10", "location": "KPK", "message": "Dir valley experiencing flash floods. Avoid unnecessary travel!"},
            {"timestamp": "2022-08-31 20:30", "location": "Sindh", "message": "Sujawal completely cut off due to rising Indus River levels."}
        ]

    def _extract_structured_data(self, row, location):
        """Extract structured flood data from messy text using an LLM."""
        text = row['text']
        response = self.client.Completion.create(
            model="gpt-4o-mini",
            prompt=f"""
            Extract information about related to flooding in {location} such as blocked roads, 
            affected areas and possible data sources if any.
            """,
            max_tokens=100
        )
        structured_info = response["choices"][0]["text"].strip()
        return structured_info
    
    def _build_index(self):
        texts = self.data.apply(lambda x: f"{x['date']} - {x['location']}: {x['affected_areas']}, Blocked Roads: {x['blocked_roads']}", axis=1)
        embeddings = self.model.encode(texts.tolist(), normalize_embeddings=True)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(np.array(embeddings))
        return index, embeddings

    def query_flood_history(self, query):
        """Retrieve past flood data from FAISS."""
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        _, idx = self.index.search(np.array(query_embedding), 1) 
        result = self.data.iloc[idx[0][0]]
        return f"Date: {result['date']}\nLocation: {result['location']}\nAffected Areas: {result['affected_areas']}\nBlocked Roads: {result['blocked_roads']}\nSource: {result['source']}"

    def get_live_flood_update(self):
        """Retrieve a simulated live flood update."""
        update = random.choice(self.live_updates)
        return f"[{update['timestamp']}] {update['location']} - {update['message']}"

flood_tool = FloodDataTool()

#print("🔍 Retrieving Historical Data:\n", flood_tool.query_flood_history("Flood in Sindh"))
#print("\n🚨 Getting Live Update:\n", flood_tool.get_live_flood_update())
