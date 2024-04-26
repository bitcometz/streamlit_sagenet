import streamlit as st
import pkg_resources

# 获取已安装包的列表
installed_packages = pkg_resources.working_set

# 遍历每个已安装的包并输出其名称和版本号
for package in installed_packages:
    st.write(f"{package.key}=={package.version}")
