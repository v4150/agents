from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from scout_agent.outputs import (
    FirstDraftPick,
    Prospect,
    ProspectList,
    ProspectReport,
    ProspectReportList,
)

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class ScoutAgent:
    """ScoutAgent crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def scouting_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["scouting_agent"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def prospect_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["prospect_researcher"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def pick_prospect(self) -> Agent:
        return Agent(
            config=self.agents_config["pick_prospect"],  # type: ignore[index]
            verbose=True,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def task_scout(self) -> Task:
        return Task(
            config=self.tasks_config["task_scout"],  # type: ignore[index]
            output_pydantic=ProspectList,
        )

    @task
    def task_researcher(self) -> Task:
        return Task(
            config=self.tasks_config["task_researcher"],  # type: ignore[index]
            output_pydantic=ProspectReportList,
        )

    @task
    def task_pick(self) -> Task:
        return Task(
            config=self.tasks_config["task_pick"],  # type: ignore[index]
            output_pydantic=FirstDraftPick,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ScoutAgent crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        # create the manager agent
        manager = Agent(
            config=self.agents_config["manager"],
            allow_delegation=True,
            verbose=True,
        )

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.hierarchical,
            manager_agent=manager,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
