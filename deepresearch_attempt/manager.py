import asyncio

from models import GPT_4_1_MINI
from output_types import PrepareData, Questions, SearchPlan

from agents import Agent, Runner, trace

DEFAULT_NUM_QUESTIONS = 3
DEFAULT_NUM_SEARCH_STRINGS = 5


class Manager:
    def __init__(
        self,
        num_questions=DEFAULT_NUM_QUESTIONS,
        num_search_strings=DEFAULT_NUM_SEARCH_STRINGS,
    ):
        self.num_questions = num_questions
        self.num_search_strings = num_search_strings

        self._create_preparer()

    def _create_search_planner_agent(self):
        search_planner_instructions = "You are a helpful research assistant. Given a topic, come up with a web search string;  Do not actually search the web, just tell me what you would search for on the web"

        return Agent(
            name="search_planner",
            instructions=search_planner_instructions,
            model=GPT_4_1_MINI,
            output_type=SearchPlan,
        )

    def _create_question_agent(self):
        questioner_agent_instructions = "You are given a topic and are tasked with generating a very diffiult question pertaining to that topic."
        return Agent(
            name="questioner",
            instructions=questioner_agent_instructions,
            model=GPT_4_1_MINI,
            output_type=Questions,
        )

    def _create_preparer(self):
        # first, prepare search_planner_agent and question_agent
        sp_agent = self._create_search_planner_agent()
        q_agent = self._create_question_agent()

        # create tools from agents
        sp_tool = sp_agent.as_tool(
            tool_name="search_planner_tool",
            tool_description="finds search strings to use for researching a specific topic",
        )
        q_tool = q_agent.as_tool(
            tool_name="questioner_tool",
            tool_description="generates questions for a specific topic",
        )

        # compile a list of tools for the preparer_agent
        tools = [sp_tool, q_tool]
        preparer_agent_instructions = f"""
You are an assistant preparing your worker to perform some deep research on a topic.
You are tasked with coming up with {self.num_questions} very difficult questions related to this topic. 
In addition, you are also tasked with preparing {self.num_search_strings} search strings for your worker to use during their research.
Use your tools to complete these tasks.
"""
        # After you've received all questions and search strings, handoff the data to the reporter agent.
        self.preparer_agent = Agent(
            name="preparer_agent",
            instructions=preparer_agent_instructions,
            model=GPT_4_1_MINI,
            tools=tools,
            output_type=PrepareData,
        )

    async def run(self):
        with trace("prepare-test"):
            result = await Runner.run(self.preparer_agent, "Mustang Shelby GT500")
        print(result.final_output)
