from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fluid Flow Prediction System - Database Demo")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ========== ROOT ENDPOINT ==========
@app.get("/")
def root():
    return {
        "message": "✅ Backend connected successfully!",
        "database": "SQLite",
        "endpoints": {
            "experiments": "/experiments/",
            "predictions": "/predictions/",
            "demo_data": "/demo/populate"
        }
    }

# ========== EXPERIMENT ENDPOINTS ==========
@app.get("/experiments/", response_model=list[schemas.Experiment])
def read_experiments(db: Session = Depends(get_db)):
    """Get all experiments from database"""
    return crud.get_experiments(db)

@app.post("/experiments/", response_model=schemas.Experiment)
def create_experiment(experiment: schemas.ExperimentCreate, db: Session = Depends(get_db)):
    """Create a new experiment"""
    return crud.create_experiment(
        db=db,
        name=experiment.name,
        params=experiment.parameters,
        desc=experiment.description
    )

@app.get("/experiments/{exp_id}", response_model=schemas.Experiment)
def read_experiment(exp_id: int, db: Session = Depends(get_db)):
    """Get a specific experiment by ID"""
    exp = crud.get_experiment_by_id(db, exp_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@app.delete("/experiments/{exp_id}")
def delete_experiment(exp_id: int, db: Session = Depends(get_db)):
    """Delete an experiment"""
    deleted = crud.delete_experiment(db, exp_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"message": "Experiment deleted successfully"}

# ========== PREDICTION ENDPOINTS ==========
@app.get("/predictions/", response_model=list[schemas.Prediction])
def read_predictions(db: Session = Depends(get_db)):
    """Get all predictions from database"""
    return crud.get_predictions(db)

@app.post("/predictions/", response_model=schemas.Prediction)
def create_prediction(prediction: schemas.PredictionCreate, db: Session = Depends(get_db)):
    """Create a new prediction"""
    return crud.create_prediction(
        db=db,
        exp_id=prediction.experiment_id,
        input_val=prediction.input_value,
        output_path=prediction.output_path
    )

@app.get("/predictions/experiment/{exp_id}", response_model=list[schemas.Prediction])
def read_predictions_by_experiment(exp_id: int, db: Session = Depends(get_db)):
    """Get all predictions for a specific experiment"""
    return crud.get_predictions_by_experiment(db, exp_id)

@app.delete("/predictions/{pred_id}")
def delete_prediction(pred_id: int, db: Session = Depends(get_db)):
    """Delete a prediction"""
    deleted = crud.delete_prediction(db, pred_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return {"message": "Prediction deleted successfully"}

# ========== DEMO DATA ENDPOINT ==========
@app.post("/demo/populate")
def populate_demo_data(db: Session = Depends(get_db)):
    """
    Populate database with sample data for demonstration
    This endpoint creates sample experiments and predictions
    """
    try:
        # Clear existing data (optional - remove if you want to keep data)
        db.query(models.Prediction).delete()
        db.query(models.Experiment).delete()
        db.commit()
        
        # Create sample experiments
        exp1 = crud.create_experiment(
            db, 
            name="Reynolds Number Study", 
            params="Re=1000, viscosity=0.001", 
            desc="Study of flow patterns at low Reynolds numbers"
        )
        
        exp2 = crud.create_experiment(
            db, 
            name="Turbulent Flow Analysis", 
            params="Re=5000, turbulence_model=k-epsilon", 
            desc="Analysis of turbulent flow in a pipe"
        )
        
        exp3 = crud.create_experiment(
            db, 
            name="Laminar Flow Simulation", 
            params="Re=500, channel_width=0.1m", 
            desc="Simulation of laminar flow in rectangular channel"
        )
        
        # Create sample predictions for each experiment
        crud.create_prediction(db, exp1.id, 2.5, "/outputs/exp1_pred1.png")
        crud.create_prediction(db, exp1.id, 3.7, "/outputs/exp1_pred2.png")
        crud.create_prediction(db, exp2.id, 8.2, "/outputs/exp2_pred1.png")
        crud.create_prediction(db, exp2.id, 9.1, "/outputs/exp2_pred2.png")
        crud.create_prediction(db, exp3.id, 1.5, "/outputs/exp3_pred1.png")
        
        return {
            "message": "✅ Demo data populated successfully!",
            "experiments_created": 3,
            "predictions_created": 5,
            "next_steps": [
                "Visit /experiments/ to see all experiments",
                "Visit /predictions/ to see all predictions",
                "Try /experiments/1 to get specific experiment",
                "Visit /docs for interactive API documentation"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error populating data: {str(e)}")

# ========== DATABASE STATS ENDPOINT ==========
@app.get("/stats")
def get_database_stats(db: Session = Depends(get_db)):
    """Get statistics about the database"""
    exp_count = db.query(models.Experiment).count()
    pred_count = db.query(models.Prediction).count()
    
    return {
        "database": "SQLite (fluidflow.db)",
        "total_experiments": exp_count,
        "total_predictions": pred_count,
        "status": "✅ Database connected and operational"
    }