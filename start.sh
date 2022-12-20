#!/bin/bash

# Starting Flask
gunicorn --bind=127.0.0.1:8080 predict:app --daemon

# Starting Streamlit app
streamlit run app.py --server.address 127.0.0.1 --server.port 8051
