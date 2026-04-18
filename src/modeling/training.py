import argparse
from datetime import datetime
import shutil

from ultralytics import YOLO

from src.config import MODELS_DIR, PROCESSED_DATA_DIR, REPORTS_DIR


def train_model(yolo_model: str, data_yaml: str, epochs: int, project_name: str, run_name: str, batch_size: int):
    model = YOLO(yolo_model)
    model.train(data=data_yaml,
                epochs=epochs,
                project=REPORTS_DIR / project_name,
                name=run_name,
                batch=batch_size)
    metrics = model.val()
    print(f"Validation metrics: {metrics}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLO model training for bottle sorting system")
    
    parser.add_argument("--model", type=str, default="yolov8s.pt", help="Name of the YOLO model to use (e.g., yolov8s.pt, yolov8m.pt, etc.)")
    parser.add_argument("--epochs", type=int, default=75, help="Number of training epochs")
    parser.add_argument("--batch", type=int, default=4, help="Batch size")

    args = parser.parse_args()

    project_name = args.model.split('.')[0] + "-" + str(args.epochs) + "e-" + str(args.batch) + "b"
    print(project_name)
    
    current_datetime = datetime.now()
    date_string = current_datetime.strftime('%Y-%m-%d_%H:%M:%S')

    train_model(
        yolo_model=args.model,         
        data_yaml=str(PROCESSED_DATA_DIR / "data.yaml"),
        epochs=args.epochs,          
        project_name=project_name, 
        run_name=date_string,
        batch_size=args.batch          
    )

    WEIGTH_DIR = REPORTS_DIR / project_name / date_string / "weights"
    print(f"Best model weights saved at: {WEIGTH_DIR / '.pt'}")

    shutil.copy(WEIGTH_DIR / 'best.pt', MODELS_DIR / f'{project_name}.pt')
    print(f"Best model weights copied to: {MODELS_DIR / f'{project_name}.pt'}")