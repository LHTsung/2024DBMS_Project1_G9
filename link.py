import psycopg2

connection = psycopg2.connect(
    user='project_9',
    password='4arh6p',
    host='140.117.68.66',
    port='5432',
    dbname='project_9'
)

cursor = connection.cursor()

