from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud, gan_model
from ..database import SessionLocal

router = APIRouter(prefix="/predictions", tags=["Predictions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{experiment_id}", response_model=schemas.Prediction)
def create_prediction(experiment_id: int, prediction: schemas.PredictionCreate, db: Session = Depends(get_db)):
    # Run GAN inference
    output_path = gan_model.generate_fluid_flow_image(prediction.input_data)
    # Store result in DB
    return crud.create_prediction(db, experiment_id, prediction, output_path)
