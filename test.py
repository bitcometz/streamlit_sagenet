import streamlit as st
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
