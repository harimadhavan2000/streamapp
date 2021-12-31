import streamlit as st
import numpy as np
import pandas as pd
from bittu import gethu
import matplotlib.pyplot as plt

df1 = pd.read_csv('zhavli.csv')
lists = df1['Course']

choices = st.multiselect('Select Courses', lists, None)
tablex = gethu(choices)
if(type(tablex)!=list):
	st.pyplot(tablex, 0)
else:
	st.write("Course Clash! The following courses clash:")
	tablex = [list(t) for t in set(tuple(element) for element in tablex)]
	for i in tablex:
		st.write(i[0] + " and " + i[1])
	choices = choices[:-1]
	tablex1 = gethu(choices, 1)
	st.empty()
	st.write("Showing timetable without last added course")
	st.pyplot(tablex1)
