from enum import Enum
from datetime import datetime
from typing_extensions import Self  # type: ignore

from pydantic import BaseModel, Field  # type: ignore
from pydantic import model_validator, ValidationError  # type: ignore


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=300)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode='after')
    def check_contact(self) -> Self:
        errors: list[str] = []
        if not self.contact_id.startswith("AC"):
            errors.append("contact_id must start with 'AC'")
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            errors.append("Physical contacts must be verified")
        if (self.contact_type == ContactType.TELEPATHIC
                and self.witness_count < 3):
            errors.append("Telepathic contact requires at least 3 witnesses")
        if self.signal_strength > 7.0 and self.message_received is None:
            errors.append("High signal strength requires a message")

        if errors:
            raise ValueError(" - ".join(errors))
        return self


def print_validation_errors(e: ValidationError) -> None:
    for error in e.errors():
        msg = error["msg"].replace("Value error, ", "")
        print(msg)


def main() -> None:
    print("Alien Contact Log Validation")
    try:
        print("======================================")
        print("Valid contact report:")
        contact1 = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime(2024, 1, 1, 12, 0, 0),
            contact_type=ContactType.RADIO,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
        )
        print("ID:", contact1.contact_id)
        print("Type", contact1.contact_type)
        print("Location:", contact1.location)
        print(f"Signal: {contact1.signal_strength}/10")
        print(f"Duration: {contact1.duration_minutes} minutes")
        print("Witness:", contact1.witness_count)
        print("Message:", contact1.message_received)
    except ValidationError as e:
        print_validation_errors(e)
    try:
        print("\n======================================")
        print("Expected validation error:")
        contact2 = AlienContact(
            contact_id="AC_2025_004",
            timestamp=datetime(2025, 1, 3, 3, 0, 0),
            contact_type=ContactType.TELEPATHIC,
            location="Area 49, Texas",
            signal_strength=8.5,
            duration_minutes=50,
            witness_count=2,
            message_received="We will destroy you!",
        )
        print("ID:", contact2.contact_id)
        print("Type", contact2.contact_type)
        print("Location:", contact2.location)
        print(f"Signal: {contact2.signal_strength}/10")
        print(f"Duration: {contact2.duration_minutes} minutes")
        print("Witness:", contact2.witness_count)
        print("Message:", contact2.message_received)
    except ValidationError as e:
        print_validation_errors(e)


if __name__ == "__main__":
    main()
