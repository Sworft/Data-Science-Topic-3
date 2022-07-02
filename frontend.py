import streamlit as st
import pandas as pd
import numpy as np
import T3
import random

st.set_page_config(layout="wide")
st.title('Visualization of EEG data & Bloom Filter', "Topic 3")

if "init" not in st.session_state:
    st.session_state.BloomAF3 = T3.BloomAF3
    st.session_state.BloomF7 = T3.BloomF7
    st.session_state.BloomF8 = T3.BloomF8
    st.session_state.S1 = T3.S1
    st.session_state.S2 = T3.S2
    st.session_state.S3 = T3.S3
    st.session_state["init"] = 1

st.write("EEG data from three channels")

left_column, middle_column, right_column = st.columns(3)

left_column.line_chart(T3.AF3)
left_column.caption("AF3 Channel")
middle_column.line_chart(T3.F7)
middle_column.caption("F7 Channel")
right_column.line_chart(T3.F8)
right_column.caption("F8 Channel")

left_column.number_input("Desired key to check:", key="left_item", step=1, min_value=0, value=4000)
left_number = st.session_state.left_item
left_column.write("The key " + str(left_number) + " is" + " not" * (not st.session_state.BloomAF3.check(left_number)) + " in S for channel AF3 according to the filter.")
left_column.write("The key " + str(left_number) + " is" + " not" * (not (left_number in st.session_state.S1)) + " in S for channel AF3 according to the in-function.")

middle_column.number_input("Desired key to check:", key="middle_item", step=1, min_value=0, value=4000)
middle_number = st.session_state.middle_item
middle_column.write("The key " + str(middle_number) + " is" + " not" * (not st.session_state.BloomF7.check(middle_number)) + " in S for channel F7 according to the filter.")
middle_column.write("The key " + str(middle_number) + " is" + " not" * (not (middle_number in st.session_state.S2)) + " in S for channel F7 according to the in-function.")

right_column.number_input("Desired key to check:", key="right_item", step=1, min_value=0, value=4000)
right_number = st.session_state.right_item
right_column.write("The key " + str(right_number) + " is" + " not" * (not st.session_state.BloomF8.check(right_number)) + " in S for channel F8 according to the filter.")
right_column.write("The key " + str(right_number) + " is" + " not" * (not (right_number in st.session_state.S3)) + " in S for channel F8 according to the in-function.")

st.write("Bloom Filter Settings")

left_column, middle_column, right_column = st.columns(3)

left_column.number_input("Set size n of bitmap:", key="bitmap_size", step=1, min_value=1, value=15000)

middle_column.number_input("Set number of hash functions k:", key="k", step=1, min_value=1, max_value=100, value=10)

right_column.slider("Set number of entries in S:", key="S_size", step=1, min_value=1, max_value=1000, value=100)

if st.button("Re-initialize Bloom"):
    st.session_state.S1 = [random.choice(T3.AF3) for i in range(0, st.session_state.S_size)]
    st.session_state.S2 = [random.choice(T3.F7) for i in range(0, st.session_state.S_size)]
    st.session_state.S3 = [random.choice(T3.F8) for i in range(0, st.session_state.S_size)]
    st.session_state.BloomAF3 = T3.BloomFilter(st.session_state.bitmap_size, st.session_state.S1, hash_number=st.session_state.k)
    st.session_state.BloomF7 = T3.BloomFilter(st.session_state.bitmap_size, st.session_state.S2, hash_number=st.session_state.k)
    st.session_state.BloomF8 = T3.BloomFilter(st.session_state.bitmap_size, st.session_state.S3, hash_number=st.session_state.k)

left_column, middle_column, right_column = st.columns(3)

left_column.write("Number of distinct entries guessed: " + str(st.session_state.BloomAF3.Flajolet_Martin(T3.AF3)))
left_column.write("Number of actual distinct entries: " + str(len(set(T3.AF3))))

middle_column.write("Number of distinct entries guessed: " + str(st.session_state.BloomF7.Flajolet_Martin(T3.F7)))
middle_column.write("Number of actual distinct entries: " + str(len(set(T3.F7))))

right_column.write("Number of distinct entries guessed: " + str(st.session_state.BloomF8.Flajolet_Martin(T3.F8)))
right_column.write("Number of actual distinct entries: " + str(len(set(T3.F8))))

S = st.radio(
     "Which S-keys to show?",
     ('AF3', 'F7', 'F8'))

if S == 'AF3':
    st.write(st.session_state.S1)
elif S == "F7":
    st.write(st.session_state.S2)
else:
    st.write(st.session_state.S3)

