"""Streamlit app module"""

import streamlit as st

import predict

TITLE = "Brain Stroke Detector"
STROKE_STYLE = "padding: 20px; background-color: #f44336; color: white; margin-bottom: 15px; text-align: center; text-style: bold; font-size: 24px;"
STROKE_MESSAGE = "Stroke"
HEALTHY_STYLE = "padding: 20px; background-color: #4cbb17; color: white; margin-bottom: 15px; text-align: center; text-style: bold; font-size: 24px;"
HEALTHY_MESSAGE = "Healthy"
ERROR_STYLE = "padding: 20px; background-color: #ffc300; color: white; margin-bottom: 15px; text-align: center; text-style: bold; font-size: 24px;"


def print_outcome(outcome):
    """Outcome printing function"""
    if outcome:
        st.write(f'<div style="{STROKE_STYLE}">{STROKE_MESSAGE}</div>', unsafe_allow_html=True)
    else:
        st.write(f'<div style="{HEALTHY_STYLE}">{HEALTHY_MESSAGE}</div>', unsafe_allow_html=True)


def print_error(error):
    """Error print function"""
    st.write(f'<div style="{ERROR_STYLE}">Error: {error}</div>', unsafe_allow_html=True)


def main():
    """Main function"""
    st.set_page_config(page_title=TITLE)
    st.title(TITLE)

    st.write("This code is open source and available [here](https://github.com/Peco602/brain-stroke-detector) on GitHub.")

    uploaded_img = st.file_uploader("Upload a CT scan to be analyzed")
    if uploaded_img is not None:
        try:
            stroke = predict.predict(uploaded_img)
            print_outcome(stroke)
            st.image(uploaded_img, caption='Uploaded CT scan')
        except Exception as e:
            print_error(e)


if __name__ == '__main__':
    main()
