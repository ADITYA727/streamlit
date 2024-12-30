import streamlit as st

# Title
st.title('EVON TECH')

# Sidebar input
st.sidebar.header('User Input')
name = st.sidebar.text_input('Enter your name:')
age = st.sidebar.slider('Select your age', 18, 100)

# Button for interaction
if st.button('Submit'):
    st.write(f'Hello, {name}, you are {age} years old!')

# Display a chart
import pandas as pd
data = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9]})
st.line_chart(data)
