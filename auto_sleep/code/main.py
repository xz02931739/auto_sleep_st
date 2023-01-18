import glob
import os

import keras
import numpy as np
import pandas as pd
import pyedflib
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image


class AutoSleep(object):

    def __init__(self):
        self.n1 = None
        self.data1 = None
        self.table_values = None
        self.table_labels = None
        self.mode = None
        self.title = None
        self.add_boxs = None
        self.load = None
        self.path_r = None
        self.path_env = None
        self.path_code_running = None
        self.fig_path = None

        self.set_title('Auto sleep analysis toolbox')
        self.set_columns()
        self.set_sider()
        self.update()

    def set_title(self, name):
        self.title = st.title(name)

    def set_mode(self):
        st.set_page_config(layout='wide')

    def set_sider(self):
        st.sidebar.subheader("Control panel")
        self.load = st.sidebar.file_uploader("Choose a file", accept_multiple_files=True)

        self.add_boxs = st.sidebar.selectbox("Please select options",
                                             ("Full analysis", "Sleep Scoring", "Arousal Detection",
                                              "Respiratory Events Detection", "Sleep Quality Assessment"))

        self.n1 = st.sidebar.button('Run')

    def sub_path(self, upper_fold_name):
        self.path_code_running = os.getcwd()
        self.path_env = os.path.dirname(self.path_code_running)  # code文件夹的上一级，即ASAT
        self.path_r = os.path.join(self.path_env, str(upper_fold_name))  # 文件夹

        return self.path_r

    def set_bkg_fig(self, fig_name):
        self.fig_path = os.path.join(self.sub_path('resource'), str(fig_name))
        with st.container():
            image = Image.open(self.fig_path)
            st.image(image)

    def set_table(self, values):
        st.subheader('Sleep parameters')

        self.table_labels = ["Sleep Effective(%)", "Total Sleep Hours (min)", "Sleep Latency (min)",
                             "N3 Percentage (%)", "AHI", "ARI"]

        self.table_values = values

        df = pd.DataFrame(self.table_values, index=self.table_labels)
        st.dataframe(df)

    def set_columns(self):
        self.co1, self.co2 = st.columns(2)

        with self.co1:
            st.header('Figures')
            self.set_bkg_fig('Predicted hypnogram.png')
            self.set_bkg_fig('Aro.png')
            self.set_bkg_fig('Res.png')

        with self.co2:
            st.header('f2')
            self.set_bkg_fig('Res.png')
            self.set_table([0, 0, 0, 0, 0, 0])

            values = st.slider(
                'Select a range of values',
                0.0, 100.0, (25.0, 75.0))
            st.write('Values:', values)

    def update(self):
        if self.n1 is True:
            st.write('12')

            with self.co2:
                self.set_table([0, 0, 1, 0, 0, 0])


class ExternalRun(object):
    def __init__(self):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    app = AutoSleep()
