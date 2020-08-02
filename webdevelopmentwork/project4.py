import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
import random
import matplotlib.pyplot as plt
def read():
    df = pd.read_excel('Farmer.xlsx')
    return df
def read_storage():
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aman@123",
    database = 'mydatabase'
    )
    db_cursor = mydb.cursor()
    db_cursor.execute('SELECT * FROM storage_storage')
    table_rows = db_cursor.fetchall()
    cols = ['id','Avail_wheat','Avail_rice','Avail_maize','Avail_jute','Avail_sugarcane','season','year','TotalJuteCapicity','TotalMaizeCapicity','TotalRiceCapicity','TotalSugarcaneCapicity','TotalWheatCapacity']
    df = pd.DataFrame(table_rows,columns=cols)
    mydb.close()
    return df
def areadetails(df):
    if(st.checkbox('prodcution yield in metric ton')):
        areamap = {'jute':(2.5*df['Area'].values)[0],'wheat':(1.3*df['Area'].values)[0],'sugarcane':(4*df['Area'].values)[0],'rice':(2*df['Area'].values)[0]}
        print(areamap)
        st.write(areamap)
    
def showfarmplan(df):
    st.subheader('FarmPlan')
    imgs = plt.imread('fimg2.jpg')
    st.image(imgs)
    st.table(df.iloc[0])
  
def suggestcrop(df):
    storage = read_storage()
    storage = storage[storage['year']==2019]
    storage = storage[storage['season']=='Kharif']
    cclist =["ajgd3225lgeaei@jdfj@","asibuend235243@jafljd(fdaljfa","tufneuus35lh23h12l4","fasdlfjlasdjfasdf32"]
    cc =random.choice(cclist)
    if(st.checkbox("View Seed Offer")):
        st.write("20% Discount on rice seed and 10% incentive on rice crop. Here is the coupoun code")
        if(st.button("apply","appl")):
            st.write(cc)
            print(cc)


def user(username):
    df = read()
    df = df[df['Farmerid']==username]
    try:
        showfarmplan(df)
    except:
        print("showfarmplan")
    try:
        areadetails(df)
    except:
        print("areadetails")
    try:     
        suggestcrop(df)
    except:
        print("suggest")    
    print("success")

def main():
    Login = st.sidebar.checkbox("Login")

    if(Login):    
        df = read()
        id = df.Farmerid.values
        pw = df.Password.values 
        print(id[0])  ##
   
        try:
            username = int(st.sidebar.text_input('Username: '))
            password = st.sidebar.text_input('Password: ',type = 'password')
            pw = df[df['Farmerid']==username]['Password'].values
            print(pw)
            if st.sidebar.button("login",'login') or Login:
                if(Login):    
                    if(username in id):
                        if(password == pw):
                            st.sidebar.success("Correct Password")
                            user(username)
                        elif(password!=""):
                            st.error("wrong password")
                    elif(username!=""):
                        st.error("wrong username")
        except:
            print("error")
# a=2
# html_code = '''<h1 "background-color:#000000"  >     Admin Login{a} </h1>'''
# st.sidebar.markdown(html_code,unsafe_allow_html=True)    
main()
# suggestcrop(read())
