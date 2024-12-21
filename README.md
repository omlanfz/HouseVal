# HouseVal: House Price Prediction Using Machine Learning

HouseVal is a machine learning project that predicts real estate prices based on various features such as location, property characteristics, total area (sqft), and more. The goal is to assist buyers, sellers, and real estate professionals in making informed decisions with accurate property valuations.

## Features
- Predict house prices by providing location, total area, number of bedrooms, and bathrooms.
- Backend powered by a Flask API and a trained Gradient Boosting Regressor model.
- User-friendly frontend built with HTML, CSS, and JavaScript.

## Dataset
The dataset was sourced from **bproperty.com**, containing details on various properties in Dhaka, Bangladesh.

## Project Workflow
1. **Data Collection**: Gathered real estate data.
2. **Data Preprocessing & Feature Engineering**: Cleaned and transformed data, encoded categorical variables, and created new features like price per square foot.
3. **Model Training & Evaluation**: Trained multiple models and selected the Gradient Boosting Regressor for its superior performance.
4. **Deployment**: Developed a Flask API to serve predictions.
5. **Frontend Development**: Built an intuitive interface to interact with the API.

## Tools and Libraries
- **Python**: Pandas, NumPy, Scikit-learn, Matplotlib, Flask
- **Frontend**: HTML, CSS, JavaScript

## How to Run
Follow the instructions below to set up and run the project locally:

### Prerequisites
- Python 3.8 or above
- pip (Python package manager)

### Setup
1. **Clone this repository**
   git clone https://github.com/<your-username>/HouseVal.git

2. **Navigate to the project directory**
   cd HouseVal

3. **Install dependencies**
   pip install -r requirements.txt

4. **Prepare artifacts**
   Ensure columns.json and house_prices_model.pickle are in the artifacts/ folder.

5. **Run the server** 
   python server.py

6. Access the application: Open http://127.0.0.1:5000 in your web browser.
