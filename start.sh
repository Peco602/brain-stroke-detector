#!/bin/bash

# Starting Flask
gunicorn --bind=0.0.0.0:8080 predict:app --daemon

# Starting Streamlit app
streamlit run app.py --server.address 0.0.0.0 --server.port 8051
