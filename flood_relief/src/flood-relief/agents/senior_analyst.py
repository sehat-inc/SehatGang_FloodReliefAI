import requests
from bs4 import BeautifulSoup
import openai
import json
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

class SeniorAnalystAgent:

    def scrape_and_analyze(self, url):
        """
        Scrapes flood-related data from the given URL and extracts key details using OpenAI.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch data: {e}"}

        # Extract text from webpage
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        article_text = " ".join([p.text for p in paragraphs])

        # Send to OpenAI for analysis
        prompt = f"""
        You are an expert in disaster relief. Extract key flood-related data from this news.
        Provide JSON output with:
        - "Location"
        - "Roads Situation Summary"
        - "Emergencies"
        
        Article: {article_text}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=300
        )

        try:
            gpt_output = json.loads(response["choices"][0]["message"]["content"])
            return gpt_output
        except json.JSONDecodeError:
            return {"error": "Failed to parse OpenAI response"}

# Example Usage
if __name__ == "__main__":
    agent = SeniorAnalystAgent()
    test_url = "https://en.wikipedia.org/wiki/2010_Pakistan_floods"  # Replace with real URL
    result = agent.scrape_and_analyze(test_url)
    print(json.dumps(result, indent=2))
