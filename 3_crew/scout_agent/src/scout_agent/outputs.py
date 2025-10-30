from typing import List

from pydantic import BaseModel, Field


class Prospect(BaseModel):
    full_name: str = Field("Prospect First and Last Name")
    position: str = Field("Prospects Position")
    college: str = Field("The college the prospect plays for")


class ProspectList(BaseModel):
    prospects: List[Prospect] = Field("A list of Prospects")


class ProspectReport(BaseModel):
    prospect: Prospect = Field("Prospect Info")
    report: str = Field("A full and detailed report about the prospect")


class ProspectReportList(BaseModel):
    prospect_reports: List[ProspectReport] = Field("A list of Prospect Reports")


class FirstDraftPick(BaseModel):
    first_pick: Prospect = Field(
        "The prospect that is predicted to win the first draft"
    )
