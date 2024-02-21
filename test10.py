from flask import Flask, render_template, request, send_file,make_response
import pandas as pd
from io import BytesIO
import asyncio
import aiohttp
import json
from dotenv import load_dotenv
import os
app = Flask(__name__)


load_dotenv()  # This loads the environment variables from .env

# Now you can use the API key
openai_api_key = os.getenv('CHATGPT_API_KEY')

global ideas_df
async def fetch_with_backoff(session, url, payload, headers, retries=5, backoff_factor=1):
    for attempt in range(retries):
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 429:
                wait = backoff_factor * (2 ** attempt)
                print(f"Rate limit hit, retrying in {wait} seconds...")
                await asyncio.sleep(wait)
            elif response.status == 200:
                return await response.json()
            else:
                response_text = await response.text()
                print(f"Error: {response.status}, Body: {response_text}")
                return None
    raise Exception("Request failed after retries with rate limit errors.")

async def generate_idea_async(session, principle, user_inputs):
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": f"Generate a unique idea applying the TRIZ inventive principle of {principle}. After describing the idea for {json.dumps(user_inputs)}, evaluate its utility and novelty on a scale from 1 to 10. Ensure the idea is distinct, with a brief description in 25 words, its utility, novelty, and how it addresses specific objectives and contradictions."},
            {"role":"user","content":"""Combine all of this into a SINGLE LINE OUTPUT 

  

“##idea” | <method name> |   <a sequential number> |<idea name> | <idea description> |  utility | <utility> | novelty | <novelty> | idea score | <idea score>| <what objective will this idea help deliver> | <what contradiction will this help resolve> | <stimulus>  
"""}
        ],
        "max_tokens": 200,
        "temperature": 1,
        "n": 2
    }
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    url = 'https://api.openai.com/v1/chat/completions'
    data = await fetch_with_backoff(session, url, payload, headers)
    ideas = []
    if data:
        for choice in data['choices']:
            response_text = choice['message']['content'].strip()
            ideas.append(response_text)
    return ideas

def run_asyncio_coroutine(coroutine):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(coroutine)
    loop.close()
    return result

def generate_idea(principle, user_inputs):
    async def generate():
        async with aiohttp.ClientSession() as session:
            return await generate_idea_async(session, principle, user_inputs)
    return run_asyncio_coroutine(generate())

@app.route('/', methods=['GET', 'POST'])
def index():
    ideas = []
    if request.method == 'POST':
        user_inputs = request.form.to_dict()
        triz_principles =  [
    "Segmentation",
    "Taking out",
    "Local quality",
    "Asymmetry",
    "Merging",
    "Universality",
    "Nesting",
    "Anti-weight",
    "Preliminary anti-action",
    "Preliminary action",
    "Beforehand cushioning",
    "Equipotentiality",
    "The other way round",
    "Spheroidality - Curvature",
    "Dynamics",
    "Partial or excessive actions",
    "Another dimension",
    "Mechanical vibration",
    "Periodic action",
    "Continuity of useful action",
    "Skipping",
    "Blessing in disguise or Turn lemons into lemonade",
    "Feedback",
    "Intermediary",
    "Self-service",
    "Copying",
    "Cheap short-living objects",
    "Replacing mechanical system",
    "Pneumatics and hydraulics",
    "Flexible shells and thin films",
    "Porous materials",
    "Color changes",
    "Homogeneity",
    "Discarding and recovering",
    "Parameter changes",
    "Phase transitions",
    "Thermal expansion",
    "Accelerated oxidation",
    "Inert atmosphere",
    "Composite materials"
]
        for principle in triz_principles:
            ideas += generate_idea(principle, user_inputs)

        # Convert ideas to DataFrame for Excel download
        global ideas_df
        ideas_df = pd.DataFrame(ideas, columns=['Ideas'])

    return render_template('index.html', ideas=ideas)

@app.route('/download')
def download():
    try:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Ensure ideas_df is defined and not empty
            if 'ideas_df' in globals() and not ideas_df.empty:
                ideas_df.to_excel(writer, index=False)
            else:
                return make_response("No ideas to download", 404)
        output.seek(0)
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', attachment_filename="ideas.xlsx", as_attachment=True)
    except Exception as e:
        # Log the error and return a response indicating an error occurred
        print(f"An error occurred: {e}")
        return make_response("An error occurred while generating the download.", 500)


if __name__ == '__main__':
    app.run(debug=True)
