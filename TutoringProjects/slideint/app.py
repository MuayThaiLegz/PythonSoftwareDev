import pandas as pd  
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import numpy as np
import hashlib
from streamlit_option_menu import option_menu

import sklearn
import plotly.express as px 
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Portfolio Creation & Backtesting", page_icon=":bar_chart:", layout="wide")

import plotly.graph_objs as go        



 
st.cache(suppress_st_warning=True)

def main(**state):
    st.header("This is a header")
    
    choice = ['(Filspari)RE-021','TVT-058', 'Chenodal','Cholbam', 'Thiola']
    
    choice = option_menu(
        menu_title="Tech Opps",
        options= choice,
        menu_icon = "cast",
        default_index = 0,
        orientation = "horizontal"
    )
    
    #if choice == '(Filspari)RE-021':
    
    
    st.sidebar.text('Here')        
    
    if choice == '(Filspari)RE-021':
        tab1, tab2, tab3, tab4, tab = st.tabs(['(Filspari)RE-021','TVT-058', 'Chenodal','Cholbam', 'Thiola'])

        
        inputone = st.text_input('Enter Something')
        
        st.write(inputone)
        
        st.text_area('tiple')
        st.text_area('mul')
        st.expander("APP")
        
        
    if choice == 'TVT-058':
        tab1, tab2, tab3, tab4, tab = st.tabs(['(Filspari)RE-021','TVT-058', 'Chenodal','Cholbam', 'Thiola'])

        st.expander("APP")

        pass
        

    
    if choice == 'Chenodal':
        tab1, tab2, tab3, tab4, tab = st.tabs(['(Filspari)RE-021','TVT-058', 'Chenodal','Cholbam', 'Thiola'])

        if tab1:
            st.write("""
Clinical Supplies (RESTORE)

Fully supports patient enrollment targets to complete study – US and BRAZIL sites

Drug Product

Commercial inventory (>12 months on hand, 2 lots)

        Drug Substance (CDCA)

Dipharma CDCA
                
        MOQ deliveries in 2021 have provided ample supply to produce Chenodal (>2 years)
EP monograph recently updated with new impurity, later detected in Dipharma CDCA with current process
Minor manufacturing changes at Dipharma identified to control impurity level below monograph limit, fulfilling compliance requirements for European DS manufacturer
Travere & LGM notified of planned changes, including validation batches and DMF amendments
Considered low risk to Chenodal commercial & clinical supplies, as EP monograph not referenced
Next MOQ delivery planned for 2Q2023
 """)
                
                
    #st.image('1536801749740.jpg')
    
    if st.button('Drop down'):
        st.text('Select something')    
        st.expander("Appendix")

        
        
    if choice == 'Cholbam':
        tab1, tab2, tab3, tab4, tab = st.tabs(['Here','We', 'Place','values', 'that go in tabs'])

        st.expander("Appendix")
        
        st.text_area('tiple')
        
        
            
        
main()