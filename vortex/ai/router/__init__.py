#%%
from datetime import datetime

from semantic_router import Route, RouteLayer
from semantic_router.encoders import OpenAIEncoder


# Define response strategies for each route
class RouteResponseStrategy:
    def execute(self):
        raise NotImplementedError("Subclasses should implement this method")

class MathResponse(RouteResponseStrategy):
    def execute(self):
        return "This is a math-related inquiry. Let's dive into formulas and calculations!"

class BiologyResponse(RouteResponseStrategy):
    def execute(self):
        return "Biology is fascinating! Let's explore the wonders of life and living organisms."

class PoliticsResponse(RouteResponseStrategy):
    def execute(self):
        return "Discussing politics can be sensitive. Let's ensure we maintain a respectful and open dialogue."

# Factory for creating routes
class RouteFactory:
    @staticmethod
    def create_route(name, utterances):
        return Route(name=name, utterances=utterances)

# RouteManager to manage routes and responses
class RouteManager:
    def __init__(self, encoder):
        self.encoder = encoder
        self.routes = []
        self.response_strategies = {}

    def add_route(self, name, utterances, response_strategy):
        route = RouteFactory.create_route(name, utterances)
        self.routes.append(route)
        self.response_strategies[name] = response_strategy()

    def get_response(self, query):
        rl = RouteLayer(encoder=self.encoder, routes=self.routes)
        route = rl(query)
        strategy = self.response_strategies.get(route.name)
        if strategy:
            return strategy.execute()
        else:
            pass
        return query



# Initialize RouteManager with an encoder
encoder = OpenAIEncoder()
route_manager = RouteManager(encoder)


# Define routes and their corresponding response strategies
math_utterances = [
    "can you explain the concept of a derivative?",
    "What is the formula for the area of a triangle?",
    # Additional utterances...
]

biology_utterances = [
    "what is the process of osmosis?",
    "can you explain the structure of a cell?",
    # Additional utterances...
]

politics_utterances = [
    "isn't politics the best thing ever",
    "why don't you tell me about your political opinions",
    # Additional utterances...
]

# Adding routes to the RouteManager
route_manager.add_route("mathematics", math_utterances, MathResponse)
route_manager.add_route("biology", biology_utterances, BiologyResponse)
route_manager.add_route("politics", politics_utterances, PoliticsResponse)

# Function to process queries using the semantic layer
def semantic_layer(query: str):
    response = route_manager.get_response(query)
    return response

# Example Query
# query = "can you explain the concept of a derivative?"
# print(semantic_layer(query))

# %%
