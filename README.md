# Image Classification Web App

## Overview

This project is a simple web application that allows users to upload images for classification. Using TensorFlow and Flask, the app leverages a pre-trained MobileNetV2 model to classify images into predefined categories (e.g., dogs, cats, etc.).

## Features

- Upload images via a user-friendly web interface
- Classify images using a pre-trained TensorFlow model
- Display top predictions with probabilities

## Prerequisites

- Python 3.x
- Pip

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/image_classifier.git
   cd image_classifier
   ```

2. **Install required libraries**:
   ```bash
   pip install Flask tensorflow pillow numpy
   ```

3. **Create necessary directories**:
   ```bash
   mkdir static/uploads
   ```

## Usage

1. **Run the application**:
   ```bash
   python app.py
   ```

2. **Access the app**:
   Open your web browser and go to `http://127.0.0.1:5000/`.

3. **Upload an image**:
   Use the upload form to select an image file, and click "Upload". The app will display the top predictions for the uploaded image.

## Code Structure

- `app.py`: Main Flask application file
- `model.py`: Contains the image classification logic
- `templates/index.html`: HTML template for the web interface
- `static/uploads/`: Directory to store uploaded images

## Contributing

Feel free to fork the repository and make your contributions. If you find any issues or have suggestions, please open an issue.
