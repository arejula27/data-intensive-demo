# Real-Time Sentiment Analysis Project

## Overview
This project is part of the ID2221 Data-Intensive Computing course. It involves designing and implementing a real-time data streaming system for sentiment analysis on political tweets. The system utilizes Hugging Face's transformer library to perform sentiment analysis and Apache Spark to handle a data stream.

This repository contains a demo of a data intensive application. The application is a complete data pipeline that ingests data from a source, processes it, and stores it in a database. The application is implemented in Python and uses the following technologies:
- [Kafka](https://kafka.apache.org/) for the message broker
- [Spark](https://spark.apache.org/) for the data processing
- [Transformer](https://huggingface.co/docs/transformers/en/index) for sentiment analysis
- [MongoDB](https://www.mongodb.com/) for the database

### Project Structure

```
data-intensive-demo/  
├── dashboard/ # Component to display the final results.  
├── mongo/ # Stores streaming processing results. 
├── src/
│    ├── producer/ # Component to set up and feed the data stream.
│    ├── sentiment_analysis/ # Component to process and classify tweets' sentiment.
│    ├── stream/ # Component to handle and process the data stream.
│    ├── twitter_scraper # Component to scrape Twitter and collect data for the demo.
│    └── main.py # Entrypoint to run the demo.
├── .dockerignore
├── .gitignore
├── docker-compose.yml # Docker Compose configuration.
├── Makefile # Targets to set up and run the project.
├── README.md # Project documentation. 
└── requirements.txt # Python dependencies.
```

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Docker and Docker Compose installed on your machine
- Python 3.10

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/arejula27/data-intensive-demo.git
   cd data-intensive-demo
   ```

2. **Install dependencies**:
    ```sh
   make install
   ```

3. **Set up environment**:
    ```sh
   make up
   ```

Wait for all of the services to be up and running. 

2. **Launch the demo**:
    ```sh
   make start
   ```

2. **To shut down**:
    ```sh
   make down
   ```