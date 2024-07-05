from pydantic import BaseModel as PydanticBaseModel

class BaseModel(PydanticBaseModel):
    name: str

    @classmethod
    def from_dict(cls, name: str, data: dict):
        return cls(name=name, **data)

    def to_dict(self):
        return self.model_dump(exclude={'name'})