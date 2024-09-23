import psycopg2

conn = psycopg2.connect(host="100.27.237.72", port = 5432, database="ell_proposals", user="db_usr_aiml", password="Db_2024!AiML")

# Create a cursor object
cur = conn.cursor()

cur.execute("""SELECT NOW ()""")
query_results = cur.fetchall()
print(query_results)

cur.close()
conn.close()
