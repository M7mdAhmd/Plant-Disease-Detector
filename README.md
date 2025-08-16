# Plant Disease Detector

## Overview

It is a web application that allows users to upload images of plant leaves and receive a prediction of the disease affecting the plant or confirmation that it is healthy. The application provides an easy and intuitive interface for rapid plant disease detection.

## Features

- Detects and classifies 38 different plant diseases.
- Provides a web interface for image upload and disease prediction.
- Visualizes model training progress through accuracy and loss plots.
- High accuracy with efficient model architecture.

## Model

- Pretrained EfficientNetB0 base model for feature extraction.
- Additional fully connected layers for multi-class classification.
- Trained on an augmented plant disease dataset with high accuracy (>99% on train and validation).
- Preprocessing applied using `preprocess_input` for optimal performance.

## Web Application

- Built using Flask for serving the model predictions.
- HTML, CSS, and minimal JavaScript interface for image upload.
- Returns predicted disease class for uploaded images.

## Notebook

The model training and dataset exploration were done in a Kaggle notebook.
You can view the full notebook [here](https://www.kaggle.com/code/mhmdelshoraky/efficientnetb0-plant-disease-detection).

## Dependencies

- Python 3.x
- TensorFlow
- OpenCV
- NumPy
- Matplotlib
- Flask
