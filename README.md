# AI-Powered-Customer-Insights-Forecasting-Web-Application

This project is a full-stack web application that leverages machine learning and generative AI to help businesses understand customer behavior, predict future trends, and generate actionable strategies. It demonstrates end-to-end capabilities from data ingestion → analysis → modeling → deployment → business value delivery.

# Features

- Generative AI Recommendations: Automatically generate customer engagement strategies, personalized marketing copy, and retention plans.

- Churn Risk Prediction: Identify top 50 customers at risk of churning using logistic regression and RFM features.

- Revenue Anomaly Detection: Detect statistically significant revenue spikes and dips using z-score analysis.

- Classification Models: Predict customer churn with Random Forest and Logistic Regression.

- Regression Models: Forecast customer lifetime value and revenue.

- Clustering: Segment customers into meaningful groups using K-Means.

- Forecasting: Predict future sales trends with time-series models (Prophet).

- Data Analysis & Statistics: Explore datasets, visualize correlations, and run hypothesis tests (t-test, chi-square).

- Interactive Dashboard: Frontend built with React.js for real-time insights.

- Cloud Deployment: Containerized with Docker and deployed on Render free tier.

Tech Stack

- Frontend: React, TailwindCSS

- Backend: FastAPI, Python

- ML/AI: scikit-learn, Prophet, Hugging Face Transformers

- Data: Pandas, NumPy, Matplotlib, Seaborn

- Deployment: Docker, Render (Free Tier)

# Getting Started

# Backend Setup

- Clone the repository:

- git clone: https://github.com/jigglewiggle101/AI-Powered-Customer-Insights-Forecasting-Web-Application.git 
- cd ai-customer-insights/AI-Powered-Customer-Insights-Forecasting-Web-Application
- terminal command to run backend: python -m uvicorn backend.app:app --reload --port 8000
- cd ai-customer-insights/AI-Powered-Customer-Insights-Forecasting-Web-Application 
- terminal command to run seed: python -m backend.seed    
- cd ai-customer-insights/AI-Powered-Customer-Insights-Forecasting-Web-Application/backend 
- terminal command to install backend requirements.txt:
python -m uvicorn backend.app:app --reload --port 8000

# Build and run with Docker (Backend):

- terminal command: cd AI-Powered-Customer-Insights-Forecasting-Web-Application
- docker build -t ai-insights -f backend/Dockerfile .
- docker run -p 8000:8000 ai-insights - to run
- cd AI-Powered-Customer-Insights-Forecasting-Web-Application then docker run ai-insights python -m backend.seed - for seed

# Build and run with Docker (Frontend):

- terminal command: cd AI-Powered-Customer-Insights-Forecasting-Web-Application
docker build -t ai-frontend -f Dockerfile . (to build frontend)

- docker run -p 5173:5173 ai-frontend (run frontend)

# Access the API at:

http://localhost:8000

# Frontend Setup

Navigate to frontend:

- cd AI-Customer-Insights-App/AI-Powered-Customer-Insights-Forecasting-Web-Application
- cd frontend
- npm install
- npm run dev

Visit http://localhost:3000 in your browser.

# Example Use Cases

Telecom company predicting churn and generating retention strategies.

E-commerce platform forecasting monthly sales and segmenting customers.

Marketing teams creating AI-powered campaign copy tailored to customer clusters.

# Why This Project Matters

# This application showcases:

- Generative AI integration for real business value.

- Machine learning models across classification, regression, clustering, and forecasting.

- Cloud-native deployment with Docker + Render.

📜 License

This project is licensed under the MIT License - see the LICENSE file for details.