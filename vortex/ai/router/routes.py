import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Type

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class RouteResponseStrategy(ABC):
    """
    Abstract base class for defining response strategies for different routes.
    Subclasses must implement the execute method.
    """

    @abstractmethod
    def execute(self, query: str = None, user_id: str = None) -> str:
        pass


class MathResponse(RouteResponseStrategy):
    def execute(self, query: str = None, user_id: str = None) -> str:
        """Generates a math-related response incorporating the user's query."""
        return "Math Inquiry. You should use the math or wolfram alpha tool"


class BiologyResponse(RouteResponseStrategy):
    def execute(self, query: str = None, user_id: str = None) -> str:
        """Generates a biology-related response incorporating the user's query."""
        return "Biology Inquiry. Try using the wikipedia, wolfram alpha or search tool"


class PoliticsResponse(RouteResponseStrategy):
    def execute(self, query: str = None, user_id: str = None) -> str:
        """Generates a politics-related response incorporating the user's query."""
        return "Politics Inquiry. Avoid the topic and answer that you're not allowed to discuss politics"


class TechnologyResponse(RouteResponseStrategy):
    def execute(self, query: str = None, user_id: str = None) -> str:
        return "Focus on providing the latest technological trends, innovations, and explanations of complex concepts like AI, blockchain, and cybersecurity. Suggest visiting educational platforms for deeper insights."


class HealthFitnessResponse(RouteResponseStrategy):
    def execute(self, query: str = None, user_id: str = None) -> str:
        return "Offer general wellness advice, emphasizing the importance of consulting healthcare professionals for personalized guidance. Suggest resources for diet and exercise plans."


class EntertainmentResponse(RouteResponseStrategy):
    def execute(self, query: str = None, user_id: str = None) -> str:
        return "Recommend popular or critically acclaimed movies, music, books, and games. Use genre-specific knowledge to tailor suggestions and encourage exploration of new content."


class FinanceEconomicsResponse(RouteResponseStrategy):
    def execute(self, query: str = None, user_id: str = None) -> str:
        return "Provide insights into financial literacy, investment strategies, and economic principles. Caution against specific financial advice, place a disclaimer that your response should not be used as financial advice, while suggesting authoritative resources for further learning."


class EnvironmentalScienceResponse(RouteResponseStrategy):
    def execute(self, query: str = None, user_id: str = None) -> str:
        return "Highlight current environmental challenges and sustainable practices. Encourage actions that contribute to sustainability and recommend resources for education on environmental conservation."


class HistoryCultureResponse(RouteResponseStrategy):
    def execute(self, query: str = None, user_id: str = None) -> str:
        return "Share historical facts and cultural insights, promoting an understanding of diverse perspectives. Suggest documentaries, books, and virtual museum tours for comprehensive exploration."


class PsychologyMentalHealthResponse(RouteResponseStrategy):
    def execute(self, query: str = None, user_id: str = None) -> str:
        return "Discuss the importance of mental well-being, offering general advice on managing stress and anxiety. Recommend seeking professional help for serious concerns and suggest mindfulness and support resources."


class SQLResponse(RouteResponseStrategy):
    def execute(self, query: str = None, user_id: str = None) -> str:
        """Generates a SQL-related response incorporating the user's query."""
        if user_id in [os.getenv("ADMIN_USER_ID", "admin")]:
            return "SQL Inquiry. You should use the SQL toolkit"
        return "SQL Inquiry. The current user is not authorized to use the SQL toolkit. Please contact an administrator. Avoid the topic and answer that you're not allowed to run SQL"


class TimeNowResponse(RouteResponseStrategy):
    def execute(self, query: str = None, user_id: str = None) -> str:
        now = datetime.now()
        return (
            f"The current time is {now.strftime('%H:%M')}, use "
            "this information in your response"
        )


class RouteConfig(BaseModel):
    """
    Schema definition for route configuration using Pydantic.
    Validates the structure of each route configuration.
    """

    name: str
    utterances: List[str]
    strategy: Type["RouteResponseStrategy"]


ROUTES_CONFIGURATIONS = [
    RouteConfig(
        name="mathematics",
        utterances=[
            "what is the value of pi?",
            "what is the square root of 16?",
            "can you solve this equation? 2x + 5 = 13",
            "what is the area of a circle with radius 5?",
            "what is 3**2?",
            "can you calculate the derivative of x^2?",
            "how do you find the integral of x^2?",
            "what is the Pythagorean theorem?",
            "explain the Fibonacci sequence",
            "what is the difference between permutations and combinations?",
        ],
        strategy=MathResponse,
    ),
    RouteConfig(
        name="biology",
        utterances=[
            "what is the process of osmosis?",
            "can you explain the structure of a cell?",
            "what is the function of mitochondria?",
            "how do plants perform photosynthesis?",
            "what are the basics of genetics?",
            "explain the theory of evolution",
            "what are the different types of cells?",
            "how do vaccines work?",
        ],
        strategy=BiologyResponse,
    ),
    RouteConfig(
        name="politics",
        utterances=[
            "what do you think about the current political situation?",
            "can you give me your opinion on political leaders?",
            "how do you see the future of [Country/Region]'s politics?",
            "what's your take on the upcoming election?",
            "do you believe political reform is needed?",
            "what are your thoughts on government policies?",
            "how should we address political polarization?",
            "what can be done about political corruption?",
            "how do political ideologies impact society?",
            "is there a solution to political deadlock?",
        ],
        strategy=PoliticsResponse,
    ),
    RouteConfig(
        name="sql",
        utterances=[
            "query the database",
            "show the results in the table",
            "select data from the table",
            "how do you join two tables?",
            "what is the difference between INNER JOIN and OUTER JOIN?",
            "explain the use of GROUP BY clause",
            "how can I use SQL to filter data?",
            "query the table",
            "sql query",
            "query",
        ],
        strategy=SQLResponse,
    ),
    RouteConfig(
        name="get_time",
        utterances=[
            "what time is it?",
            "can you tell me the time?",
            "what's the current time?",
            "what year is it?",
            "what is the date today?",
            "how many days until next month?",
            "can you give me the time in London?",
        ],
        strategy=TimeNowResponse,
    ),
    RouteConfig(
        name="technology_computing",
        utterances=[
            "What's the difference between AI and machine learning?",
            "How does blockchain technology work?",
            "Can you explain quantum computing?",
            "What are the latest trends in cybersecurity?",
            "What is the future of cloud computing?",
            "How do I protect my privacy online?",
            "What are the basics of coding for beginners?",
        ],
        strategy=TechnologyResponse,
    ),
    RouteConfig(
        name="health_fitness",
        utterances=[
            "What are the benefits of a plant-based diet?",
            "How often should I exercise each week?",
            "What's the best way to lose weight?",
            "Can you recommend home exercises for beginners?",
            "How do I manage stress through diet and exercise?",
            "What are the health risks of sitting all day?",
            "What supplements should I consider for general health?",
        ],
        strategy=HealthFitnessResponse,
    ),
    RouteConfig(
        name="entertainment",
        utterances=[
            "What are some must-watch classic films?",
            "Recommend a book that's similar to Harry Potter.",
            "What new music genres are emerging?",
            "Best video games for stress relief?",
            "What are the top streaming shows right now?",
            "Can you suggest a playlist for studying?",
            "What board games are fun for two players?",
        ],
        strategy=EntertainmentResponse,
    ),
    RouteConfig(
        name="finance_economics",
        utterances=[
            "How do I start investing in stocks?",
            "What is cryptocurrency and should I invest in it?",
            "Can you explain how inflation affects savings?",
            "What are the best budgeting apps available?",
            "How can I improve my credit score?",
            "What are the basics of personal financial planning?",
            "How do interest rates affect the economy?",
        ],
        strategy=FinanceEconomicsResponse,
    ),
    RouteConfig(
        name="environmental_science",
        utterances=[
            "What are simple actions to reduce my carbon footprint?",
            "How does recycling actually help the environment?",
            "Can you explain the impact of climate change on oceans?",
            "What are renewable energy sources?",
            "How can urban areas contribute to sustainability?",
            "What is biodiversity and why is it important?",
            "Are electric cars really better for the environment?",
        ],
        strategy=EnvironmentalScienceResponse,
    ),
    RouteConfig(
        name="history_culture",
        utterances=[
            "What were the causes of World War II?",
            "Can you explain the significance of the Renaissance?",
            "What is the cultural impact of the Silk Road?",
            "How did ancient Egyptians build the pyramids?",
            "What are key moments in the civil rights movement?",
            "How do cultural differences affect global business?",
            "What are some traditional cuisines from around the world?",
        ],
        strategy=HistoryCultureResponse,
    ),
    RouteConfig(
        name="psychology_mental_health",
        utterances=[
            "What are effective strategies for coping with anxiety?",
            "How does social media impact mental health?",
            "Can you explain the stages of grief?",
            "What are the signs of burnout and how can I prevent it?",
            "How does exercise benefit mental health?",
            "What are the benefits of mindfulness meditation?",
            "How can I build resilience in tough times?",
        ],
        strategy=PsychologyMentalHealthResponse,
    ),
]
