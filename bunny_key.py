import mysql.connector
config = {
    'user': 'avnadmin',
    'password': 'AVNS_Jw69kwe1u00p9FJrgAH',
    'host': 'mysql-38e489bf-bunnyhemasaireddy-8196.b.aivencloud.com',
    'port': 13610,
    'database': 'defaultdb', 
    'auth_plugin': 'mysql_native_password'
}
con = mysql.connector.connect(**config)
cor=con.cursor()
cor.execute("select * from secret;")
r=cor.fetchone()
con.close()
api_key=r[0]+'FzBzcZX'
access_id= r[1]+'VKZLQISHY'
app_pass=r[2]+' fpvu uwlr'
app_email=r[3]
