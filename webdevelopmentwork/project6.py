import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
bihar_data = pd.read_csv('D:\SIH\Ann-Aztecs\Bihar_data.csv')
bihar_data = bihar_data.dropna(axis=0)
bihar_data['Production_per_100000'] = bihar_data['Production']/100000
bihar_data['Area_per_100000'] = bihar_data['Area']/100000
group_data1 = bihar_data.groupby(["District_Name","Crop"])
production_data1 = group_data1['Production_per_100000'].sum()
area_data1 =  group_data1['Area_per_100000'].sum()
unique_district = bihar_data.District_Name.unique()
unique_season = bihar_data.Season.unique()
unique_crop = bihar_data.Crop.unique()
years = bihar_data.Crop_Year.unique()
st.sidebar.subheader("District Wise Production and Area")
rd = st.sidebar.radio("choose district",unique_district)
dmap = {}
num=0
for i in unique_district:
    dmap[i]=num
    num+=1 
i = dmap[rd] 
if(st.sidebar.checkbox("Show")):
    plt.figure(figsize=(22,25))
   
    plt.subplot(2,1,1)
    sns.barplot(production_data1[unique_district[i]].index,production_data1[unique_district[i]])
    plt.ylim(0,50)
    plt.xticks([i for i in range(42)],label=unique_crop,rotation=90)
    plt.xlabel("")
    plt.ylabel("Production in metric ton",fontsize=30)
    plt.subplot(2,1,2)
    sns.barplot(area_data1[list(unique_district)[i]].index,area_data1[list(unique_district)[i]])
    plt.xticks([i for i in range(42)],label=unique_crop,rotation=90)
    plt.ylim(0,5)
    plt.suptitle(list(unique_district)[i])
    plt.xlabel("Crop",fontsize=20)
    plt.ylabel("Area in Hectare ",fontsize=30)
    plt.suptitle(rd,fontsize=50)
    plt.show()
    st.pyplot()
# print(unique_district)    

