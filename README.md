# 🍾 Bottle Sorting System

An intelligent, real-time computer vision system designed to detect and classify 'brand' bottles (Coca-Cola, Pepsi, Fanta, Sprite).

## ❓ How and Where this project is used?

This project simulates an industrial environment where a conveyor belt transports bottles, and a robotic arm sorts them into different containers/bins based on their brand.

## 📁 Project Organization

```
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- Project documentation
├── data
│   ├── processed      <- The final dataset ready for YOLO (Train/Val/Test)
│   └── raw            <- The original images, labels and classes.txt
│
├── models             <- Trained models
│
├── notebooks          <- Jupyter notebooks.
    │
    ├── image_predictions.ipynb  <- Visualization of detections in 'test_set'
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         src and configuration for tools like black
│
├── reports            <- YOLO savings after training (Training Logs, confusion matrices, plots, etc.)
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment
│
├── main.py            <- Main file to run the script/system
│
└── src   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes src a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── detector.py             <- Code for detections on camera
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── dataset.py          <- Scripts to download or generate data       
    │   └── training.py         <- Code to train models


```

## ⚙️ Workflow

### 1. Data Collection and Labeling

```
Before training, you must prepare your "dataset":
    - Take photos of necessary bottles (e.g. Cola, Pepsi, Fanta, Sprite);
    - Use a labeling tool like Label Studio, CVAT, or Robotflow;
    - Annotate the objects using the YOLO format and add it in `data/raw` directory;
    - Ensure `data/raw` contains: `images/`, `labels/` and `classes.txt`.
```

### 2. Dataset Generation

````
Organize your raw data into structured folders for training. This script handles shuffling and splitting (Train, Validation, and Test sets), e.g:

```bash
make data VAL_SIZE=0.1 TEST_SIZE=0.1
```

This creates `data/processed` folder with the required YOLO directory structure.
````

### 3. Model Training

````
Train the YOLO model using the provided Makefile. You can override default parameters directly from the terminal, e.g.:

```bash
make train MODEL=yolov8s.pt EPOCHS=75 BATCH=4
```

**Logs**: Training progress is saved in `reports/`;
**Weights**: The best performing weights (`best.pt`) are automatically copied to `models/`.
````

### 4. Evaluation and Testing

```
To verify the model's performance on 'test_set' or unseen images in the training session before deployment, navigate to `notebooks/image_predictions.ipynb`, which allows you to load the model and to visualize detections on those images.
```

### 5. Live Detection

````
Once you have the "perfect" model, launch it in a real-time sorting system:

```bash
make run
```

**Features**: Includes an auto-reconnect login for the camera and a "Camera Not Found" safety UI;
**Controls**: Press `q` to safely exist the stream and release hardware resources.
````

## Used Technology:

```
* YOLO *: Core object detection and tracking;
* OpenCV *: Video stream handling;
* Pytonh 3.12 *: Main login and backend;
* GNU Make *: Task automation
```

## VIDEO! HOW THIS PROJECT WORKS
