from __future__ import annotations
from datetime import  datetime
from bson.objectid import ObjectId as BsonObjectId
from typing import Annotated, List, Union, Optional
import json
from pydantic import BaseModel, Field, validator
from re import findall


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return BsonObjectId(v)
        except Exception:
            raise ValueError(f"{v} is not a valid ObjectId")
        return str(v)


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError("ObjectId required")
        return str(v)


class Provenance(BaseModel):
    email: Optional[str]  # email retrieved from JWT
    affiliation: Optional[str]  # affiliation retrieved from JWT
    createdAt: Annotated[
        datetime, Field(default_factory=lambda: datetime.now().utcnow())
    ]
    updatedAt: Annotated[
        datetime, Field(default_factory=lambda: datetime.now().utcnow())
    ]


class Project(BaseModel):
    name: str
    label: str
    description: Optional[str]


class Parameter(BaseModel):
    name: str
    value: Union[float, str]


class Agent(BaseModel):
    name: str
    version: str


class ChemicalCompositionItem(BaseModel):
    element: str
    percentage: str


class Lattice(BaseModel):
    a: str
    b: str
    c: str
    alpha: str
    beta: str
    gamma: str


class InputMaterial(BaseModel):
    lattice: Optional[Lattice]
    sites: List[List[float]]
    species: List[str]
    cell: List[List[float]]


class OutputMaterial(BaseModel):
    lattice: Optional[Lattice]
    sites: List[List[float]]
    species: List[str]
    cell: List[List[float]]


class Material(BaseModel):
    formula: str
    elements: Optional[List[str]]  # List[Union[str, str]]
    input: Optional[InputMaterial]
    output: Optional[OutputMaterial]

    @validator("elements", always=True)
    def composite_name(cls, v, values, **kwargs):
        elements = [
            x
            for x in findall("[A-Z][a-z]?|[0-9]+", values["formula"])
            if not x.isnumeric()
        ]
        return elements


class PropertyFile(BaseModel):
    fullpath: str


class Property(BaseModel):
    name: str
    value: Union[float, str]
    file: Optional[PropertyFile]


class Process(BaseModel):
    isExperiment: bool
    method: str
    agent: Optional[Agent]


class FileProject(BaseModel):
    hash: Optional[str]
    name: str
    extention: str
    size: Optional[str]
    createdAt: Annotated[
        datetime, Field(default_factory=lambda: datetime.now().utcnow())
    ]
    updatedAt: Annotated[
        datetime, Field(default_factory=lambda: datetime.now().utcnow())
    ]

    class Config:
        use_enum_values = True


def validate_datetime(cls, values):
    """
    Reusable validator for pydantic models
    """
    return values or datetime.now().utcnow()


class newProject(BaseModel):
    identifier: Optional[str]
    provenance: Optional[Provenance]
    project: Project
    process: Process
    material: Material
    parameters: List[Parameter]
    properties: List[Property]
