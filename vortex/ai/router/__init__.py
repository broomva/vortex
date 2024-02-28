# !pip install -qU semantic-router

from datetime import datetime

from semantic_router import Route, RouteLayer
from semantic_router.encoders import OpenAIEncoder

# we could use this as a guide for our chatbot to avoid political conversations
politics = Route(
    name="politics",
    utterances=[
        "isn't politics the best thing ever",
        "why don't you tell me about your political opinions",
        "don't you just love the president" "don't you just hate the president",
        "they're going to destroy this country!",
        "they will save the country!",
    ],
)

# this could be used as an indicator to our chatbot to switch to a more
# conversational prompt
chitchat = Route(
    name="chitchat",
    utterances=[
        "Did you watch the game last night?",
        "what's your favorite type of music?",
        "Have you read any good books lately?",
        "nice weather we're having",
        "Do you have any plans for the weekend?",
    ],
)

# we can use this to switch to an agent with more math tools, prompting, and LLMs
mathematics = Route(
    name="mathematics",
    utterances=[
        "can you explain the concept of a derivative?",
        "What is the formula for the area of a triangle?",
        "how do you solve a system of linear equations?",
        "What is the concept of a prime number?",
        "Can you explain the Pythagorean theorem?",
    ],
)

# we can use this to switch to an agent with more biology knowledge
biology = Route(
    name="biology",
    utterances=[
        "what is the process of osmosis?",
        "can you explain the structure of a cell?",
        "What is the role of RNA?",
        "What is genetic mutation?",
        "Can you explain the process of photosynthesis?",
    ],
)

# we place all of our decisions together into single list
routes = [politics, chitchat, mathematics, biology]

time_route = Route(
    name="get_time",
    utterances=[
        "what time is it?",
        "when should I eat my next meal?",
        "how long should I rest until training again?",
        "when should I go to the gym?",
    ],
)

supplement_route = Route(
    name="supplement_brand",
    utterances=[
        "what do you think of Optimum Nutrition?",
        "what should I buy from MyProtein?",
        "what brand for supplements would you recommend?",
        "where should I get my whey protein?",
    ],
)

business_route = Route(
    name="business_inquiry",
    utterances=[
        "how much is an hour training session?",
        "do you do package discounts?",
    ],
)

product_route = Route(
    name="product",
    utterances=[
        "do you have a website?",
        "how can I find more info about your services?",
        "where do I sign up?",
        "how do I get hench?",
        "do you have recommended training programmes?",
    ],
)

routes = [time_route, supplement_route, business_route, product_route]


rl = RouteLayer(encoder=OpenAIEncoder(), routes=routes)




def get_time():
    now = datetime.now()
    return (
        f"The current time is {now.strftime('%H:%M')}, use "
        "this information in your response"
    )


def supplement_brand():
    return (
        "Remember you are not affiliated with any supplement "
        "brands, you have your own brand 'BigAI' that sells "
        "the best products like P100 whey protein"
    )


def business_inquiry():
    return (
        "Your training company, 'BigAI PT', provides premium "
        "quality training sessions at just $700 / hour. "
        "Users can find out more at www.aurelio.ai/train"
    )


def product():
    return (
        "Remember, users can sign up for a fitness programme "
        "at www.aurelio.ai/sign-up"
    )


def semantic_layer(query: str):
    route = rl(query)
    if route.name == "get_time":
        query += f" (SYSTEM NOTE: {get_time()})"
    elif route.name == "supplement_brand":
        query += f" (SYSTEM NOTE: {supplement_brand()})"
    elif route.name == "business_inquiry":
        query += f" (SYSTEM NOTE: {business_inquiry()})"
    elif route.name == "product":
        query += f" (SYSTEM NOTE: {product()})"
    else:
        pass
    return query