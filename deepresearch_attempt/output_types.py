from typing import List

from pydantic import BaseModel, Field


# QuestionAgent Output
class Questions(BaseModel):
    questions: List[str] = Field("The questions to be asked and tested for")


# SearchPlannerAgent Output
class Search(BaseModel):
    search_string: str = Field("The suggested string to search for")
    reason: str = Field("Why you think this string is valuable to search for")


class SearchPlan(BaseModel):
    searches: List[Search] = Field(
        "A list of strings used to search the web for learning purposes"
    )


# PreparerAgent Output
class PrepareData(BaseModel):
    search_plan: SearchPlan = Field(
        "The strings to search when conducting your research"
    )

    questions: Questions = Field(
        "Questions used to verify the the details within the final report"
    )


# Report Agent Output
class Report(BaseModel):
    report: str = Field("The Actual Report")
