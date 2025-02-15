import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=api_key)

def test_openai_api():
    try:
        # Make a simple test request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello, can you hear me?"}
            ]
        )
        
        # Print the response
        print("API Test Successful!")
        print("Response:", response.choices[0].message.content)
        return True
        
    except openai.APIError as e:
        print("API Error:", str(e))
        return False
    except Exception as e:
        print("Error:", str(e))
        return False

if __name__ == "__main__":
    test_openai_api()