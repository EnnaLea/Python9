from math import ceil
from enum import Enum
from datetime import datetime
from typing_extensions import Self  # type: ignore

from pydantic import BaseModel, Field  # type: ignore
from pydantic import model_validator, ValidationError  # type: ignore


class Rank(str, Enum):
    CADET = "cadet"
    OFFICIER = "officier"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMADER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def check_mission(self) -> Self:
        errors: list[str] = []
        if not self.mission_id.startswith("M"):
            errors.append("Every mission should start with 'M'")
        if not any(member.rank in (Rank.COMMADER, Rank.CAPTAIN)
                   for member in self.crew):
            errors.append("Mission must have at" +
                          "least one Commander or Captain")
        if self.duration_days > 365:
            senior = sum(1 for member in self.crew
                         if member.years_experience >= 5)
            required = ceil(len(self.crew) / 2)
            if senior < required:
                errors.append(f"Long missions need at "
                              f"least 50% experienced crew "
                              f"({required} of {len(self.crew)}"
                              f"members with 5+ years)")
        if not any(member.is_active for member in self.crew):
            errors.append("All crew members must be active")

        if errors:
            raise ValueError(" - ".join(errors))
        return self


def print_validation_errors(e: ValidationError) -> None:
    for error in e.errors():
        msg = error["msg"].replace("Value error, ", "")
        print(msg)


def main() -> None:
    print("Space Mission Crew Validation")
    try:
        print("=========================================")
        print("Valid mission created:")
        sarah = CrewMember(
            member_id="DIOE32",
            name="Sahara",
            rank=Rank.COMMADER,
            age=47,
            specialization="Mission Comand",
            years_experience=7,
        )
        john = CrewMember(
            member_id="NIO456",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age=38,
            specialization="Navigation",
            years_experience=5,
        )
        alice = CrewMember(
            member_id="ESD907",
            name="Alice Johnson",
            rank=Rank.OFFICIER,
            age=42,
            specialization="Engineering",
            years_experience=5,
        )
        mission1 = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2024, 1, 1, 12, 0, 0),
            duration_days=900,
            crew=[sarah, john, alice],
            budget_millions=2500.0
        )
        print("Mission", mission1.mission_name)
        print("ID", mission1.mission_id)
        print("Destination", mission1.destination)
        print(f"Duration: {mission1.duration_days} days")
        print(f"Budget: ${mission1.budget_millions}M")
        print("Crew size:", len(mission1.crew))
        print("Crew members:")
        for member in mission1.crew:
            print(f"- {member.name} - ({member.rank.value})"
                  f"- {member.specialization}")
    except ValidationError as e:
        print_validation_errors(e)
    try:
        print("\n=========================================")
        print("Expected validation error:")
        bob = CrewMember(
            member_id="CAD001",
            name="Bob Cadet",
            rank=Rank.CADET,
            age=22,
            specialization="Training",
            years_experience=1,
        )
        lisa = CrewMember(
            member_id="OFF002",
            name="Lisa Officer",
            rank=Rank.OFFICIER,
            age=30,
            specialization="Communications",
            years_experience=4,
        )
        mark = CrewMember(
            member_id="LTN003",
            name="Mark Lieutenant",
            rank=Rank.LIEUTENANT,
            age=35,
            specialization="Engineering",
            years_experience=6,
        )
        mission2 = SpaceMission(
            mission_id="M2025_VENUS",
            mission_name="Venus Exploration",
            destination="Venus",
            launch_date=datetime(2025, 6, 15, 9, 0, 0),
            duration_days=200,
            crew=[bob, lisa, mark],
            budget_millions=1500.0,
        )
        print("Mission:", mission2.mission_name)
    except ValidationError as e:
        print_validation_errors(e)


if __name__ == "__main__":
    main()
