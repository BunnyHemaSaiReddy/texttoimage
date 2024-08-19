import mysql.connector
config = {
    'user': 'avnadmin',
    'password': 'AVNS_dw-GhEn5H2OmZl82p_a',  
    'host': 'mysql-38e489bf-bunnyhemasaireddy-8196.b.aivencloud.com',
    'port': 13610,
    'database': 'secret_keys'
}

cor=con.cursor()
cor.execute("select * from secret;")
r=cor.fetchone()
con.close()
api_key=r[0]+'FzBzcZX'
access_id= r[1]+'VKZLQISHY'
app_pass=r[2]+' fpvu uwlr'
app_email=r[3]
