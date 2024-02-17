
from flask import Flask, render_template, request
import asyncio
import aiohttp

app = Flask(__name__)

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
openai_api_key = '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'
prompt =  """
    Prompt #3 Famous Innovators 

Act as an innovation expert 

Imagine tackling our specific business challenge {challengev1} while  adhering to the constraints and restrictions outlined. Please consider how renowned innovators or successful business leaders from various industries would approach this challenge while staying within our constraints and restrictions 

 

Consider how  renowned innovators or successful business leader from a different industries would approach our current business challenge. Please offer insights into their potential strategies and solutions. 

 

How to do this 

1. Create a list of 20 renowned innovators, successful business leader 

2. For each person provide 2 ways our {challengev1} could be reformulated 

 

Offer two unique reformulations of the challenge for each figure, 

 

This will lead to 40 insights 

 

Please automatically continue until you have generated all the insights requested. It is OK if this takes some time 

 

Important note: in your work please ensure each insight provided is unique. This can be measured by cosine similarity between ideas., Unique is no other insight with a cosine similarity higher than .85 

 

  

Please Structure the output as follows  

 

**The Method:** <a brief description of the method being used> 

**Insights:** 

<answer to the prompt> 

 

After this output please suggest 3-5 ways this prompt could be improved to deliver on these objectives 1/  clarify the business challenge 2. identify potential solutions 3. identify things to include in our strategy 
 

 

Please think like an innovation expert trying to find meaningful and unique ideas for our innovation challenge 

 

Create 1 list of 10 stimuli related to {challengev2} focused on problems we might solve = List #1 

Choose 10 TRIZ inventive principles that might to be useful to solve our challenge = list #2 

Choose 10 Famous inventors | innovators that might be succesful solving our challenge = List #3 

 

Create one  idea for our innovation challenge {challengev2} for each combination of these stimuli  

 

This means there will be 1000  combinations possible  

 

Please automatically continue until you have generated all the ideas requested. It is OK if this takes some time. Stop executing this prompt when you reach the requested number of ideas.  

 

Important note: in your work please ensure each idea provided is unique. This can be measured by cosine similarity between ideas.  Unique is no other ideas with a cosine similarity higher than .85 

 

please include the <stimulus> generated from this method at the end of the idea description 

 

the stimulus is the information from list #1 , #2 and #3 combined as a stimulus for this challenge 

XXX Please Structure the output as follows 

 

Please first provide a method description 

 

**Method description** <method name> : <A short description of the method being used> 

 

Then provide a description of the ideas in a single line format like this 

 

“##idea” | <method name> |   <a sequential number> |<idea name> | <idea description> |  utility | <utility> | novelty | <novelty> | idea score | <idea score>| <what objective will this idea help deliver> | <what contradiction will this help resolve> | <stimulus>  

 

We need this format to  evaluate ideas in the future 

 

How to build this output 

 

Step 1: please create an <idea name> and include the following the following text BEFORE the <idea name>   

 

“##idea” | <method name> |   <a sequential number> 

 

This means the output will look like this  

<method name>| “##idea” | <a sequential number> |<idea name> 

 

Step 2: please create an idea description 

1. A short idea description - 40 to 80 words <idea description> 

 

2. an evaluation of the idea on these criteria  

Utility 0-10 [for clarity this is the ability of the idea to solve a real problem] <utility> 

Novelty 0-10 [for clarity this is the degree to which the idea is original] <novelty> 

<idea score> = <utility score> *,6 + <novelty score> *,4 

Format | <utility> | <novelty>| <idea score>| 

 

Step 3: identify the objectives and constraints the idea delivers on 

<what objective will this idea help deliver> | <what contradiction will this help resolve>  

 

Step 4: Combine all of this into a SINGLE LINE OUTPUT 

 

“##idea” | <method name> |   <a sequential number> |<idea name> | <idea description> |  utility | <utility> | novelty | <novelty> | idea score | <idea score>| <what objective will this idea help deliver> | <what contradiction will this help resolve> | <stimulus>  

 

THIS IS IMPORTANT to avoid reworks the final output needs to be in this format “##idea” | <method name> |   <a sequential number> |<idea name> | <idea description> |  utility | <utility> | novelty | <novelty> | idea score | <idea score>| <what objective will this idea help deliver> | <what contradiction will this help resolve> | <stimulus> 
    """

async def generate_idea(prompt):
    async with aiohttp.ClientSession() as session:
         headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    response = await session.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json={
            "model": "gpt-3.5-turbo",  # Ensure this is the correct model identifier
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    if response.status == 200:
        data = await response.json()
        return data['choices'][0]['message']['content'].strip()
    else:
        error_message = await response.text()
        print(f"Error from OpenAI: {error_message}")
        return None

async def get_ideas(prompt):
    idea = await generate_idea(prompt)
    return idea

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        inputs = [request.form.get(f'input{i}', '') for i in range(1, 9)]
        user_input = ', '.join(inputs)
        prompt_template = prompt.format(challengev1=user_input, challengev2=user_input)  # Adjusted to use both placeholders

        # Run the asynchronous function and wait for the result
        try:
            ideas = asyncio.run(get_ideas(prompt_template))
            for i in ideas:
                print(i)
        except RuntimeError as e:
            ideas = f"Error running async code: {e}"

        return render_template('clarifychallenge.html', ideas=ideas)
    else:
        return render_template('clarifychallenge.html')

if __name__ == '__main__':
    app.run(debug=True)
