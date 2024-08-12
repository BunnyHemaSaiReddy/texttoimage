import mysql.connector
con = mysql.connector.connect(
            host='sql12.freesqldatabase.com',
            user='sql12725000',
            passwd='vWBNC74tBJ',
            database='sql12725000'
            
)

'''import streamlit as st
db_config = st.secrets["mysql"]
# Initialize connection.
con = st.connection('mysql', type='sql')'''

cor=con.cursor()
cor.execute("select * from secret;")
r=cor.fetchone()
print(r)
con.close()
api_key=r[0]+'FzBzcZX'
access_id= r[1]+'VKZLQISHY'
app_pass=r[2]+' fpvu uwlr'
app_email=r[3]
