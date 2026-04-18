# Bottle Sorting System

An intelligent bottle sorting system (Coca-Cola, Pepsi, Fanta, Sprite)

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── models             <- Trained models
│
├── notebooks          <- Jupyter notebooks.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         src and configuration for tools like black
│
├── reports            <- YOLO saving after training
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── main.py            <- Main file to run the script/system
│
└── src   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes src a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── detector.py            <- Code for detections on camera
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── dataset.py          <- Scripts to download or generate data       
    │   └── training.py         <- Code to train models


```

--------

