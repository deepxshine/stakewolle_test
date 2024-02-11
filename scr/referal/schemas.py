from fastapi_users import schemas
from pydantic import BaseModel

from datetime import datetime

from auth.schemas import UserRead


class EmailUser(schemas.BaseUser[int]):
    email: str


class ReferalCodeRead(BaseModel):
    id: int
    creator: UserRead
    referal_code: str
    is_active: bool
    date_of_createion: datetime
    lifetime: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "creator": 1,
                    "id": 24,
                    "is_active": True,
                    "lifetime": "2025-01-01T02:02:00",
                    "date_of_createion": "2024-02-11T11:46:43.644450",
                    "referal_code": "1"
                 }
            ]
        }
    }
