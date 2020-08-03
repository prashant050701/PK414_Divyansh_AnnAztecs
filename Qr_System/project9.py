import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import re
import os

def search(fid):
    qrfiles = os.listdir('sampleQR1')
    for num,qr in enumerate(qrfiles):
        sp = qr.split('.')[0]
        if(str(sp)==fid):
            return qr
def main():
    fid = st.sidebar.text_input("Farmer id : ")
    if(st.sidebar.button("Check","check")):    
        qr = search(fid)
        path = os.path.join('sampleQR1',qr)
        img = plt.imread(path)
        img = cv2.resize(img,(224,224))
        st.image(img)
        st.subheader("scan for details of farmer")

main()        
