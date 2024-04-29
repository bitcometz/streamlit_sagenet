import streamlit as st
<<<<<<< HEAD
from streamlit import session_state as ss
import json

def binaryswitch(session_state, key):

    if session_state[key] is True:
        session_state[key] = False
    else:
        session_state[key] = True
    st.write("binaryswitch:")
    st.write(key)
    st.write(session_state[key])


def binaryswitch2(session_state, celltype, key):

    if session_state[celltype][key] is True:
        session_state[celltype][key] = False
    else:
        session_state[celltype][key] = True
    st.write("binaryswitch:")
    st.write(key)
    st.write(session_state[celltype][key])

def binaryswitch3(session_state, celltype, key):

    if session_state[celltype][key] is True:
        session_state[celltype][key] = False
    else:
        session_state[celltype][key] = True

if "celltype_colours" not in ss:
    ss["celltype_colours"] = {}
    ss["celltype_chosen"] = {}
    with open("celltype_colours.json", 'r') as json_file:
        ss.celltype_colours = json.load(json_file)
        ss.celltype_chosen = {key: False for key in ss.celltype_colours}

    ss.celltype_chosen = {
      "Epiblast": True,
      "Primitive Streak": True
    }


name = "Epiblast"

st.write(ss["celltype_chosen"][name])

st.checkbox(name, value=ss.celltype_chosen[name], on_change=binaryswitch3, args = (ss, "celltype_chosen", name,))

st.write(ss["celltype_chosen"][name])


=======
import scarches as sca
import scanpy as sc # for plotting
import anndata as ad # for handling the spatial and single-cell datasets
import random # for setting a random seed
import numpy as np
import copy
import squidpy as sq
import pandas as pd
from scarches.models.sagenet.utils import glasso
from matplotlib import *
import patchworklib as pw
import functools


import pkg_resources

# 获取已安装包的列表
installed_packages = pkg_resources.working_set

# 遍历每个已安装的包并输出其名称和版本号
for package in installed_packages:
    st.write(f"{package.key}=={package.version}")
>>>>>>> e8d75d659a65c3a1a52b972c3e799434c53deb4a
