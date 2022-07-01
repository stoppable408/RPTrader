# import sqlite3
# from google.cloud import storage



from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
from dotenv import load_dotenv
import os
# initialize Connector object
class db():
    pool = None

    def __init__(self):
        load_dotenv()
        connector = Connector()
        print(os.getenv("db_user"))
        # function to return the database connection
        def getconn() -> pymysql.connections.Connection:
            conn: pymysql.connections.Connection = connector.connect(
                os.getenv('db_conn'),
                "pymysql",
                user=os.getenv('db_user'),
                password=os.getenv('db_pass'),
                db=os.getenv('db_name')
            )
            return conn

        # create connection pool
        self.pool = sqlalchemy.create_engine(
            "mysql+pymysql://",
            creator=getconn,
        )

    def getUserByID(self, user_id):
        with self.pool.connect() as db_conn:
            query = "SELECT * FROM players WHERE id = {}".format(user_id)
            result = db_conn.execute(query).fetchall()
            return result
        
    def insertNewUser(self, member):
        player_id = member.id
        name = member.name
        query = sqlalchemy.text("INSERT INTO players (id, name, rp) VALUES (:id, :name, :rp)",)

        with self.pool.connect() as db_conn:
            try:
                db_conn.execute(query, id=player_id, name=name, rp=0)
                print("Added {} into Database".format(name))
            except Exception as e:
                print(e)
    

    def updateUser(self, member):
        query = sqlalchemy.text('UPDATE players SET name = :name, rp = :rp WHERE id = :id;',)
        with self.pool.connect() as db_conn:
            try:
                db_conn.execute(query, id=member.player_id, name=member.name, rp=member.currentRP)
                print("Updated RP value for {}. The new RP value for this user is {}".format(member.name, member.currentRP))
            except Exception as e:
                print(e)


    def dropTable(self):
        query = "DELETE FROM players"
        with self.pool.connect() as db_conn:
            try:
                db_conn.execute(query)
                print("Removing all players from database")
            except Exception as e:
                print(e)
