import streamlit as st
import numpy as np
import pyedflib
import os
import glob



def figure_contianer(name):
    with st.container():
        st.write(name)

        st.bar_chart(np.random.randn(50, 3))

def load_file():
    uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)

    for uploaded_file in uploaded_files:
        st.write("File:", uploaded_file.name)

def load_model():
    path_code_running = os.getcwd()
    path_env = os.path.dirname(path_code_running)  # code文件夹的上一级，即ASAT
    path_model = os.path.join(path_env, 'model')  # 模型文件夹
    model_file = glob.glob(path_model + '\*.h5')[0]

    print(model_file)




if __name__ == '__main__':

    pass
