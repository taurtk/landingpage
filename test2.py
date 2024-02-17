from flask import Flask, jsonify, request,render_template
import aiohttp
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from dotenv import load_dotenv
import os
app = Flask(__name__)


# Load environment variables from .env file
load_dotenv()

# Now you can access environment variables using os.getenv
openai_api_key = os.getenv('SECRET_KEY')
# DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__)
app.config['SECRET_KEY'] = openai_api_key

@app.route('/')
def index():
    return render_template('clarifychallenge.html')

#  = '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'
prompt =  """
  Please think like an innovation expert trying to find meaningful and unique ideas for our innovation challenge 

  

Please generate 80  ideas based on TRIZ inventive principles. for our challenge  {challengev2}  

  

How 

For each of the 40 TRIZ inventive principles propose 2 ideas 

  

Please automatically continue until you have generated all the ideas requested. It is OK if this takes some time. Stop executing this prompt when you reach the requested number of ideas.  

  

Important note: in your work please ensure each idea provided is unique. This can be measured by cosine similarity between ideas.  Unique is no other ideas with a cosine similarity higher than .85 

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

  

Here is our {challengev2} written in TRUE NORTH format 

  

------------------------------------- 

  

The format of a TRUE NORTH is the following: 

  

TRUE | Truly Simple | A headline  that is suggestive of the mission. 

N | Narrative. Why it is important (the story) | WHY this  is VERY IMPORTANT . The Story should be so clear, people will understand the why, want to get started and know enough to get the "how" right… 

O | Objective | Finish the sentence with ONE mission, “We need ideas for _______” 

R | Restrictions: We are not interested in | We are not interested in 

T | Tactical Constraints: | Design, time, resources, investment, regulations, people, etc., etc. 

H | Here is the place to start | Areas to look for ideas to accomplish the mission including any relevant live project work that is already going on. 

  

Assets/Opportunities (that will help us achieve our goals) 

Blockers (that might make things difficult): 

  

-------------------------------------------------- 

  

Truly Simple: New products to sell to college students 

  

Narrative (the story of our business) : I am young entrepreneur looking to generate new product ideas for a successful business targeting university students.  To be successful I need big ideas that are both meaningful and unique. 

  

For now, the ideas are just ideas. The product need not yet exist, nor may it necessarily be clearly feasible. What I need is inspiration for new business ideas 

  

Objectives:  We are looking for products to sell to university  students in the United States. It should be a physical good, not a service or software that solves a real need and is unique or special in some way 

  

Restrictions (we are not interested in): Anything with a retail price over $ 50.This means the product cost should be less than $30. We are also NOT interested in services or software.  

  

IMPORTANT: WE ARE NOT LOOKING FOR IDEAS FOR SERVICES OR SOFTWARE, an APP, PLATFORMS, RENTAL SERVICES, SUBSCRIPTION SERVICES, PRODUCT SHARING PLATFORMS.  

  

THE PRODUCT IDEA NEEDS TO BE A PHYSICAL  PRODUCT.  

  

LET ME REPEAT... NO APPS NO SOFTWARE - WE NEED IDEAS FOR PHYSICAL PRODUCTS AND A RETAIL PRICE LESS THAN $50 

  

Tactical Constraints:  The product needs to be physical product of interest to university student 

  

Here are the places to start  : Here are some ideas we have had already. To give you an idea of the type of ideas we are looking for 

  

Compact Printer | Solar-Powered Gadget Charger | QuickClean Mini Vacuum Noise-Canceling Headphones | StudyErgo Seat Cushion | Multifunctional Desk Organizer Reusable Silicone Food Storage Bags | Portable Closet Organizer 

Dorm Room Chef [oven, microwave and toaster) | Collegiate Cookware Collapsible Laundry Basket | On-the-Go Charging Pouch | GreenEats Reusable Containers |HydrationStation [bottle with filter]* | Reusable Shopping Bag Set | CollegeLife Collapsible | Laundry Hamper| Adaptiflex [cord extension to fit big adapters)* |SpaceSaver Hangers | Dorm Room Air Purifier |Smart Power Strip | CampusCharger Pro 

Kitchen Safe Gloves | Nightstand Nook [charging, cup holder] |Mini Steamer CollegeCare First Aid Kit StudySoundProof [soundproofing panels]* FreshAir Fan 

StudyBuddy Lamp [portable, usb charging]* Bluetooth Signal Merger [share music]’ Adjustable Laptop Riser EcoCharge [solar powered charger]* 

Smartphone Projector 

Grocery Helper [hook to carry multiple bags]* 

FitnessOnTheGo [portable gym equipment]* 

Multipurpose Fitness Equipment 

CollegeCooker 

Multifunctional Wall Organizer 

DormDoc Portable Scanner 

Mobile Charging Station Organizer 

StudyMate Planner 

DormChef Kitchen Set 

LaundryBuddy [laundry basket]’ 

  

Assets/Opportunities (that will help us achieve our goals) 

We have easy access to students 

  

Blockers (that might make things difficult): 

We need ideas in 1 week 

  

Reference on methods - if not included in the prompt - Method name = Triz Inventive principles | objectives: Ideas | Triz """
async def generate_idea(session, prompt):
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
        return f"Error from OpenAI: {error_message}"

async def generate_ideas_async(num_ideas, user_prompt):
    async with aiohttp.ClientSession() as session:
        tasks = [generate_idea(session, user_prompt) for _ in range(num_ideas)]
        return await asyncio.gather(*tasks)

@app.route('/traditional_Methods', methods=['POST'])
async def traditional_Methods():
    user_prompt = request.form.get('user_prompt')
    num_ideas_requested = int(request.form.get('num_ideas', 6))  # Default to 4 if not specified
    prompt.format(challengev2=user_prompt)
    if user_prompt is None:
        return jsonify({'error': 'Missing user_prompt in the request'}), 400

    ideas = await generate_ideas_async(num_ideas_requested, prompt)
    
    # Format the responses into a JSON object
    responses = {f'response_{i}': idea for i, idea in enumerate(ideas)}
    print(responses)
    return jsonify(responses)

if __name__ == '__main__':
    # Note: Flask's default server does not support asyncio. You will need to use an ASGI server like Hypercorn.
    # app.run(debug=True)  # This won't work with async routes
    print("Use an ASGI server like Hypercorn to run this application.")
    config = Config()
    config.bind = ["0.0.0.0:8000"]
    # Note: Running serve directly like this is just for testing; use CLI for production
    import asyncio
    asyncio.run(serve(app, config))