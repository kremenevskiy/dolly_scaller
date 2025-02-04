import enum

from pydantic import BaseModel


class FormatType(enum.Enum):
    format_1_1 = '1:1'
    format_2_3 = '2:3'
    format_3_4 = '3:4'
    format_9_16 = '9:16'


class PhotoFormat(BaseModel):
    id: int
    format: FormatType = FormatType.format_1_1
    height: int
    width: int

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row['id'],
            format=row['format'],
            height=row['height'],
            width=row['width'],
        )


class UserProfile(BaseModel):
    user_id: str
    format_id: int
