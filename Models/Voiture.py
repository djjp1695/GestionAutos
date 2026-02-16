from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class Voiture(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    marque: str
    modele: str
    annee: int
    couleur: str
    actif: bool = Field(default=True)


class VoitureOut(BaseModel):
    id: int
    marque: str
    modele: str
    annee: int
    couleur: str
    actif: bool


class VoitureCreate(BaseModel):
    marque: str
    modele: str
    annee: int
    couleur: str
    actif: bool = True
