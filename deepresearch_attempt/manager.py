import asyncio
from typing import List

from models import GPT_4_1_MINI, LLAMA_3_2
from output_types import PrepareData, Questions, Report, SearchPlan

from agents import Agent, Runner, WebSearchTool, function_tool, trace

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

        # create agents
        display_agent = self._create_display_agent()
        reporter_agent = self._create_report_agent(display_agent)
        self._create_preparer_agent(reporter_agent)

    def _create_search_planner_agent(self):
        search_planner_instructions = f"You are a helpful research assistant. Given a topic, come up with {self.num_search_strings} web search strings;  Do not actually search the web, just tell me what you would search for on the web"

        return Agent(
            name="search_planner",
            instructions=search_planner_instructions,
            model=GPT_4_1_MINI,
            output_type=SearchPlan,
        )

    def _create_question_agent(self):
        questioner_agent_instructions = f"You are given a topic and are tasked with generating {self.num_questions} difficult questions pertaining to that topic. Generate the number of questions you are asked for."
        return Agent(
            name="questioner",
            instructions=questioner_agent_instructions,
            model=GPT_4_1_MINI,
            output_type=Questions,
        )

    def _create_preparer_agent(self, reporter_agent):
        # first, prepare search_planner_agent and question_agent
        sp_agent = self._create_search_planner_agent()
        q_agent = self._create_question_agent()

        # create tools from agents
        sp_tool = sp_agent.as_tool(
            tool_name="search_planner_tool",
            tool_description="generates search strings to use for researching a specific topic",
        )
        q_tool = q_agent.as_tool(
            tool_name="questioner_tool",
            tool_description="generates questions for a specific topic",
        )

        # compile a list of tools for the preparer_agent
        tools = [sp_tool, q_tool]

        # configure handoffs
        handoffs = [
            reporter_agent,
        ]
        preparer_agent_instructions = """
You are an assistant preparing your worker to perform some deep research on a topic.
You are tasked with the following:
    1. Use your tools and request difficult questions pertaining to the topic
    2. Use your tools and request queries to search for.  Do not actually perform a websearch for these queries; provide the queries only.
Rules:
    1. You must only use tools to complete these tasks
    2. You can only call each tool one time.
After you've received a response from both tools, handoff the data to the reporter agent.
"""
        self.preparer_agent = Agent(
            name="preparer_agent",
            instructions=preparer_agent_instructions,
            model=GPT_4_1_MINI,
            tools=tools,
            handoffs=handoffs,
            output_type=PrepareData,
        )

    def _create_websearch_tool(self):
        @function_tool
        def custom_websearch_tool():
            """Custom WebSearchTool"""
            return WebSearchTool(search_context_size="low")

        return custom_websearch_tool

    def _create_web_search_agent(self):
        # create the websearch tool
        custom_websearch_tool = self._create_websearch_tool()

        tools = [custom_websearch_tool]
        web_search_agent_instruction = "You are researcher.  You are provided a query to search and are required to use your websearch tool to search the web and gather all the information you can find in the results"

        self.web_search_agent = Agent(
            name="search_agent",
            instructions=web_search_agent_instruction,
            tools=tools,
            model=LLAMA_3_2,  # openai is very expensive when using WebSearchTool; opt for running ollama locally, instead
        )

    def _create_report_generator_agent(self):
        report_generator_instructions = "You are a well known journalist.  You are tasked with taking as input a some data and generating a long, detailed report with atleast 1000 words.  Make this formal, as if millions of people are going to read it; you must maintain your reputation as an excellent journalists who publishes the best reports"
        self.report_generator_agent = Agent(
            name="report_generator",
            instructions=report_generator_instructions,
            model=GPT_4_1_MINI,
            output_type=Report,
        )

    def _create_report_agent(self, display_agent):

        # create agents for tooling
        self._create_report_generator_agent()
        self._create_web_search_agent()

        # define function tool to explicitly orchestrate order of operations
        @function_tool
        async def reporter_tool(searches: List[str]) -> Report:
            """Report Generator Tool will execute Searches asychronously first, after which it will generate the actual report"""
            # run all searches asynchronously
            coroutines = [
                Runner.run(self.web_search_agent, search) for search in searches
            ]
            result = await asyncio.gather(
                *coroutines,
            )

            search_results = "\n\n".join([r.final_output for r in result])
            # generate the report
            result = await Runner.run(
                self.report_generator_agent,
                "generate a report using the details below: " + search_results,
            )
            return result

        # define the report agent
        report_agent_instructions = """
        You are tasked with two things: researching the provided input strings and generating a report with your findings;  Use your tool, reporter_tool, to complete your task.
        Once you have completed your tasks, handoff the document to the display_agent tool.
        """
        return Agent(
            name="report_agent",
            instructions=report_agent_instructions,
            model=GPT_4_1_MINI,
            handoffs=[display_agent],
            handoff_description="Take the input data and generate an actual report",
            tools=[reporter_tool],
        )

    def _create_markdown_agent(self):
        markdown_agent_instructions = "You are a glorified Markdown Formatter.  You are tasked with converting the input document to Markdown Format.  While you are at it, add a table of contents page along with hyperlinks to each section of the document"

        return Agent(
            name="markdown_agent",
            instructions=markdown_agent_instructions,
            model=GPT_4_1_MINI,
        )

    def _create_display_agent(self):
        # markdown agent
        md_agent = self._create_markdown_agent()
        md_tool = md_agent.as_tool(
            tool_name="markdown_tool",
            tool_description="converts a document into markdown format",
        )

        # display function_tool
        @function_tool
        def display_tool(md: str):
            """Tool to display the final report"""
            print(md)

        tools = [md_tool, display_tool]
        display_agent_instructions = """
        The following are your tasks:
            1. Convert the input document to Markdown Format and add a table of contents containing hyperlinks to every section.
            2. Display Markdown formatted document to the screen
        Note, you can only use your provided tools to perform these tasks.
        """

        return Agent(
            name="display_agent",
            instructions=display_agent_instructions,
            model=GPT_4_1_MINI,
            tools=tools,
            handoff_description="format and display",
        )

    async def run(self):
        with trace("prepare-test"):
            result = await Runner.run(self.preparer_agent, "Basketball")
        print(result.is_complete)
