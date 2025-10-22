from sqlalchemy import Column, Integer, String, Float, Text
from database import Base

class Experiment(Base):
    __tablename__ = "experiments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    parameters = Column(Text)
    description = Column(Text)

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer)
    input_value = Column(Float)
    output_path = Column(String)
