import os
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf 
import keras 
from keras.models import Sequential
from keras import layers
from keras.layers import Dense,Conv2D, MaxPool2D, Flatten, GlobalAveragePooling2D, InputLayer
import cv2
import random
import PIL.Image as Image
import time 
import io
import warnings 
warnings.filterwarnings(action='ignore')
st.set_option('deprecation.showfileUploaderEncoding', False)
random.seed(0)
np.random.seed(0)
def resize_image(image_array):
    return cv2.resize(image_array,(224,224))
def read_image(image_path):
    return plt.imread(image_path)
def rescale_image(image_array):
    return image_array*1./255
def plot_image(image_array):
    try:
        plt.imshow(image_array)
    except:
        plt.imshow(image_array[0])
def preprocess_image(image_path,reshape = True,read=True):
    if(read==True):
        image = read_image(image_path)
    else:
        image = image_path    
    image = resize_image(image)
    image = rescale_image(image)
    if(reshape ==  True):
        image = image.reshape(-1,image.shape[0],image.shape[1],image.shape[2])    
    return image
def preprocess_imageslist(image_list):
    imagelist = np.array([preprocess_image(img,reshape=False) for img in image_list])
    return imagelist

def streamlit_predict(imgarr):
    pimg = preprocess_image(imgarr,read=False)
    model = build_model()
    prediction = model.predict(pimg) 
    pred_dict = {0:"jute",1:"maize",2:"rice",3:"sugarcane",4:"wheat"}
    pred = pred_dict[np.argmax(prediction)]
    with st.spinner('Wait for prediction...'):
            time.sleep(2)
            st.success('Done!')
    st.write("model prediction")
    st.write(pred)

def build_model():
    keras.backend.clear_session()
    vgg = keras.applications.VGG19(input_shape=(224,224,3),include_top=False,weights='imagenet',pooling='avg')
    vggmodel = keras.Sequential([vgg
                             ,Dense(1000,activation='tanh'),Dense(1000,activation='tanh'),Dense(1000,activation='tanh'),Dense(5,activation='softmax')])

    vggmodel.compile(optimizer = 'adam',loss = 'categorical_crossentropy',metrics=['accuracy'])
    
    vggmodel.load_weights('C:\\Users\\dell\\Downloads\\vggmodelweight.h5')
    vggmodel.trainable=False
    
    return vggmodel

def predict_and_plot(image,model,plot=True):
    pred_dict = {0:"jute",1:"maize",2:"rice",3:"sugarcane",4:"wheat"}
    if(plot==True):
        plt.imshow(image[0])
    prediction = model.predict(image) 
    pred = pred_dict[np.argmax(prediction)]
    if(plot==True):
        plt.title(pred)
    st.write(pred)    

def predict_and_plot5(imagelist,model):
    pred_dict = {0:"jute",1:"maize",2:"rice",3:"sugarcane",4:"wheat"}
    plt.figure(figsize=(20,10))
    for num,image in enumerate(imagelist):
        plt.subplot(1,5,num+1)
        plt.imshow(image)
        prediction = model.predict(image.reshape(-1,224,224,3)) 
        pred = pred_dict[np.argmax(prediction)]
        plt.title(pred)

      
def read_excel_data():
    path = os.path.join("D:\SIH","Ann-Aztecs","satellliteimage.xlsx")
    ex_df = pd.read_excel(path)
    return ex_df
def farmer_data():
    path = os.path.join("D:\SIH","Ann-Aztecs","Farmlanddatabase.xlsx")
    farmer_df = pd.read_excel(path)
    return farmer_df

def search_all_images(ex_df):
    main_path = os.path.join("D:\SIH","Ann-Aztecs","satimage")
    df = ex_df.copy()
    imagelist = [os.path.join(main_path,(str(df['ImageId'][i])+".jpeg")) for i in range(df.shape[0])]
    df['imagelist']=imagelist
    return df
def read_farmer_production(df):
    path = os.path.join("D:\SIH","Ann-Aztecs","Farmlanddatabase.xlsx")
    farmer_df = pd.read_excel(path)
    new_df = pd.merge(df,farmer_df,on = ['LandRecordNo'],how = 'left')
    record_used = ['LandRecordNo','ImageId','LandArea(in Acre)','imagelist']
    new_df = new_df[record_used]
    return new_df
def predictimage(imagelist,model):
    pred_dict = {0:"jute",1:"maize",2:"rice",3:"sugarcane",4:"wheat"}
    image_prediction = []
    for num,image in enumerate(imagelist):
        image = preprocess_image(image)
        prediction = model.predict(image.reshape(-1,224,224,3)) 
        pred = pred_dict[np.argmax(prediction)]
        image_prediction.append(pred)
    return image_prediction  
def cropwisearea(area,crop):
    croplist = ['jute','maize','rice','sugarcane','wheat']
    cropdict = {'jute':0,'maize':0,'rice':0,'sugarcane':0,'wheat':0}
    for a,c in zip(area,crop):
        if(not (np.isnan(a))):
            cropdict[c]+=a
    croparea = list(cropdict.values())    
    new_df = pd.DataFrame()
    new_df['croplist'] = croplist
    new_df['croparea'] = croparea
    return new_df
    

def predict_production(df):
    imagelist = df.imagelist.values
    cropdict = {'jute':0,'maize':0,'rice':0,'sugarcane':0,'wheat':0}
    prediction = predictimage(imagelist,model=build_model())
    df['prediction_images'] = prediction
    each_crop_area_df = cropwisearea(df['LandArea(in Acre)'].values,df['prediction_images'].values)
    area_production_relation = {'jute':2.5,'maize':2.8,'rice':1.6,'sugarcane':4,'wheat':2.1}
    each_crop_area_df['production'] = [a*area_production_relation[c] for c,a in
                     zip(each_crop_area_df['croplist'].values,each_crop_area_df['croparea'].values)]   
    return each_crop_area_df

def plot_bar(result):
    x = result['croplist'].values
    a = result['croparea'].values
    p = result['production'].values
    plt.figure(figsize=(10,8))
    plt.subplot(2,1,1)
    sns.barplot(a,x)
    plt.xlabel('Area in hectare')
    plt.subplot(2,1,2)
    sns.barplot(p,x)
    plt.xlabel('Production in thousands metric tonnes')
    st.pyplot()

# crop damage detection
def dpreprocess_image(image_path,reshape = True,read=True):
    if(read==True):
        image = read_image(image_path)
    else:
        image = image_path        
    image = resize_image(image)
    image = rescale_image(image)
    if(reshape ==  True):
        image = image.reshape(-1,image.shape[0],image.shape[1],image.shape[2])    
    return image
def dbuild_model():
    keras.backend.clear_session()
    vgg = keras.applications.VGG16(input_shape=(224,224,3),include_top=False,weights='imagenet',pooling='avg')
    vggmodel = keras.Sequential([vgg
                             ,Dense(120,activation='relu'),Dense(120,activation='relu'),Dense(1,activation='sigmoid')])

    vggmodel.compile(optimizer = 'adam',loss = 'binary_crossentropy',metrics=['accuracy'])
    vggmodel.load_weights('floodmodel.h5')
    vggmodel.trainable=False
    
    
    return vggmodel

# crop damage detection end

def data2020():
    ex_df = read_excel_data()
    df = search_all_images(ex_df)
    df = read_farmer_production(df)
    result = predict_production(df)
    st.write(result)
    plot_bar(result)

def user():
    st.title('Production yeild prediction')
    st.sidebar.title('Predict production')
    st.sidebar.subheader('choose year')
    year = st.sidebar.radio("", ('2020','2021'),key='yearA')
    if(year=='2021'):
        if(st.sidebar.button("Predict",'predict')):
            st.warning('data unavailable')

    elif(year=='2020'):
        if(st.sidebar.button("Predict",'predict')):
            data2020()

    if st.sidebar.checkbox("Show Farmer data", False):
        st.header('Farmer database')
        farmer_id = st.sidebar.text_input('Farmer Id:')
        if(st.sidebar.button("Show",'show')):
            try:
                farmer_id = int(farmer_id)
                data = farmer_data()
                farmer = data[data['FarmerId']==farmer_id]
                st.write(farmer)    
            except:
                st.subheader("Wrong Farmer Id")    

def main():    
    html_code = '''<h1 "background-color:#000000"  >     Admin Login </h1>'''
    st.sidebar.markdown(html_code,unsafe_allow_html=True)
    Login = st.sidebar.checkbox("Login")

    if(Login):    
        username = st.sidebar.text_input('Username: ')
        password = st.sidebar.text_input('Password: ',type = 'password')
        if st.sidebar.button("login",'login') | Login:    
            if(username=='root'):
                if(password=='root'):
                    st.sidebar.success("Correct Password")
                    user()
                elif(password!=""):
                    st.error("wrong password")
            elif(username!=""):
                st.error("wrong username")
    html_code = '''<h1 "background-color:#000000"  >  Predict crop type </h1>'''
    st.sidebar.markdown(html_code,unsafe_allow_html=True)
    if(st.sidebar.checkbox("Check crop type")):
        uploaded_file = st.file_uploader("Upload jpeg images",type = ["jpeg","jpg"]  )
        if uploaded_file is not None:
            st.image(uploaded_file)
            img = Image.open(uploaded_file)
            arr = np.array(img)
            streamlit_predict(arr)
    html_code = '''<h1 "background-color:#000000"  > predict crop damage or not </h1>'''
    st.sidebar.markdown(html_code,unsafe_allow_html=True)
    if(st.sidebar.checkbox("Check Damage or not")):
        duploaded_file = st.file_uploader("Upload jpeg images",type = ["jpeg","jpg"]  )
        if duploaded_file is not None:
            st.image(duploaded_file)
            dimg = Image.open(duploaded_file)
            arr = np.array(dimg)
            dmodel = dbuild_model()
            dproc = dpreprocess_image(arr,read=False)
            dpred = int(dmodel.predict(dproc)[0] >0.5)
            print(dpred)
            with st.spinner('Wait for prediction...'):
                time.sleep(2)
                st.success('Done!')
            st.write("prediction")
            if(dpred==1):
                st.write("damage")
            else:
                st.write("not damage")    
main()

