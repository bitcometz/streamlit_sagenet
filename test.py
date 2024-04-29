import streamlit as st
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


