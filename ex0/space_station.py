from datetime import datetime

from pydantic import BaseModel, Field  # type: ignore
from pydantic import ValidationError  # type: ignore


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=13)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxigen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def main() -> None:
    try:
        station1 = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxigen_level=92.3,
            last_maintenance=datetime(2300, 12, 23),
        )
        print("========================================")
        print("Valid station created:")
        print("ID:", station1.station_id)
        print("Name:", station1.name)
        print("Crew:", station1.crew_size)
        print("Power:", station1.power_level)
        print("Oxygen:", station1.oxigen_level)
        print("Status: Operational")
        print("\n========================================")
        print("Expected validation error:")
        station2 = SpaceStation(
            station_id="muf",
            name="Follis",
            crew_size=39,
            power_level=50.0,
            oxigen_level=89.7,
            last_maintenance=datetime(2300, 12, 23),
        )
        print("Valid station created:")
        print("ID:", station2.station_id)
        print("Name:", station2.name)
        print("Crew:", station2.crew_size)
        print("Power:", station2.power_level)
        print("Oxygen:", station2.oxigen_level)
        print("Status: Operational")
    except ValidationError:
        print("Input should be " +
              "less than or equal to 20")


if __name__ == "__main__":
    main()
