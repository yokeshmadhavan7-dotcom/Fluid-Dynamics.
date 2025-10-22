from sqlalchemy.orm import Session
import models

# ---- Experiments ----
def create_experiment(db: Session, name: str, params: str, desc: str):
    exp = models.Experiment(name=name, parameters=params, description=desc)
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

def get_experiments(db: Session):
    return db.query(models.Experiment).all()

def get_experiment_by_id(db: Session, exp_id: int):
    return db.query(models.Experiment).filter(models.Experiment.id == exp_id).first()

def delete_experiment(db: Session, exp_id: int):
    exp = get_experiment_by_id(db, exp_id)
    if exp:
        db.delete(exp)
        db.commit()
        return True
    return False

# ---- Predictions ----
def create_prediction(db: Session, exp_id: int, input_val: float, output_path: str):
    pred = models.Prediction(experiment_id=exp_id, input_value=input_val, output_path=output_path)
    db.add(pred)
    db.commit()
    db.refresh(pred)
    return pred

def get_predictions(db: Session):
    return db.query(models.Prediction).all()

def get_predictions_by_experiment(db: Session, exp_id: int):
    return db.query(models.Prediction).filter(models.Prediction.experiment_id == exp_id).all()

def delete_prediction(db: Session, pred_id: int):
    pred = db.query(models.Prediction).filter(models.Prediction.id == pred_id).first()
    if pred:
        db.delete(pred)
        db.commit()
        return True
    return False