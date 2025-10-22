from pydantic import BaseModel
from typing import Optional

# ---- Experiment Schemas ----
class ExperimentBase(BaseModel):
    name: str
    parameters: str
    description: str

class ExperimentCreate(ExperimentBase):
    pass

class Experiment(ExperimentBase):
    id: int

    class Config:
        from_attributes = True  # Updated for Pydantic v2


# ---- Prediction Schemas ----
class PredictionBase(BaseModel):
    experiment_id: int
    input_value: float
    output_path: str

class PredictionCreate(PredictionBase):
    pass

class Prediction(PredictionBase):
    id: int

    class Config:
        from_attributes = True  # Updated for Pydantic v2