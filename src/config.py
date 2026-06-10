from pathlib import Path

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODELS_DIR = PROJ_ROOT / "models"

REPORTS_DIR = PROJ_ROOT / "reports"

# Detection PARAMETERS
MODEL_PATH = MODELS_DIR / "best_ncnn_model"  # change 'best.pt' to your model name if different   
CONFIDENCE_THRESHOLD = 0.75

OBJECTS_COLOUR = {
    "pepsi": (252, 40, 3),  
    "fanta": (3, 136, 252),
    "cola": (11, 3, 252),   
    "sprite": (78, 252, 3)   
}

#Camera parameters
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_ID = 0

#Sorting parameters
PIN_LED_1 = 17
PIN_LED_2 = 27

PIN_MOTOR_DC_1 = 23
PIN_MOTOR_DC_2 = 24

PIN_MOTOR_STEPPER_DIR = 16
PIN_MOTOR_STEPPER_STEP = 20

