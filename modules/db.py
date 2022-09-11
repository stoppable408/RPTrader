

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
            pool_recycle=1800, pool_pre_ping=True
        )


    #User Queries
    def getUserByID(self, user_id):
        with self.pool.connect() as db_conn:
            query = "SELECT * FROM players WHERE id = {}".format(user_id)
            result = db_conn.execute(query).fetchall()
            db_conn.close()
            return result
        
    def insertNewUser(self, member):
        player_id = member.id
        name = member.name.encode('utf8')
        query = sqlalchemy.text("INSERT INTO players (id, name, rp) VALUES (:id, :name, :rp)",)

        with self.pool.connect() as db_conn:
            try:
                db_conn.execute(query, id=player_id, name=name, rp=0)
                print("Added {} into Database".format(name))
            except Exception as e:
                print(e)
            db_conn.close()

    def updateUser(self, member):
        query = sqlalchemy.text('UPDATE players SET name = :name, rp = :rp WHERE id = :id;',)
        with self.pool.connect() as db_conn:
            try:
                db_conn.execute(query, id=member.player_id, name=member.name.encode('utf8'), rp=member.currentRP)
                print("Updated RP value for {}. The new RP value for this user is {}".format(member.name, member.currentRP))
            except Exception as e:
                print(e)
            db_conn.close()
            
    def getAllUsersWithIDs(self):
        query = "SELECT name, id FROM players"
        with self.pool.connect() as db_conn:
            result = db_conn.execute(query).fetchall()
            db_conn.close()
            return result
        
    def deleteUser(self, member_id):
        transaction_query = sqlalchemy.text('DELETE from transactions WHERE player_id = :id;',)
        player_query = sqlalchemy.text('DELETE from players WHERE id = :id;',)
        with self.pool.connect() as db_conn:
            try:
                db_conn.execute(transaction_query, id=member_id)
                db_conn.execute(player_query, id=member_id)
                print("Removing player with ID:{} from Database".format(member_id))
                db_conn.close()
            except Exception as e:
                print(e)
            db_conn.close()


    def dropTable(self):
        query = "DELETE FROM players"
        with self.pool.connect() as db_conn:
            try:
                db_conn.execute(query)
                print("Removing all players from database")
            except Exception as e:
                print(e)
            db_conn.close()

    def getAllUsers(self):
        query = "SELECT name, rp FROM players"
        with self.pool.connect() as db_conn:
            result = db_conn.execute(query).fetchall()
            db_conn.close()
            return result

    #Transaction Queries
    def insertTransaction(self, transaction):
        query = sqlalchemy.text("INSERT INTO transactions (id, player_id, amount, transaction_status, created_on)\
         VALUES (:id, :player_id, :amount, :transaction_status, :created_on)",)
        
        with self.pool.connect() as db_conn:
            try:
                db_conn.execute(query, id=transaction.transaction_id, 
                 player_id=transaction.player_id,
                 amount=transaction.amount, 
                 transaction_status=transaction.status, 
                 created_on=transaction.created_on)
                print("added Transaction")
            except Exception as e:
                print(e)
            db_conn.close()
 
    def getTransaction(self, transaction_id):
        query = sqlalchemy.text("SELECT * FROM transactions WHERE id = :id")
        
        with self.pool.connect() as db_conn:
            try:
                result = db_conn.execute(query, id=transaction_id).fetchall()
                db_conn.close()
                return result
            except Exception as e:
                print(e)
            db_conn.close()

    def listPendingTransactions(self):
        query = sqlalchemy.text("SELECT \
                                t.id, p.name, t.amount, t.transaction_status, t.created_on \
                                FROM\
                                transactions t\
                                JOIN players p ON p.id = t.player_id\
                                WHERE\
                                t.transaction_status = 'Pending'\
                                ORDER BY t.created_on;")
        with self.pool.connect() as db_conn:
            try:
                results = db_conn.execute(query).fetchall()
                db_conn.close()
                return results
            except Exception as e:
                print(e)
            db_conn.close()

    def listPendingTransactions(self):
        query = sqlalchemy.text("SELECT \
                                t.id, p.name, t.amount, t.transaction_status, t.created_on \
                                FROM\
                                transactions t\
                                JOIN players p ON p.id = t.player_id\
                                WHERE\
                                t.transaction_status = 'Pending'\
                                ORDER BY t.created_on;")
        with self.pool.connect() as db_conn:
            try:
                results = db_conn.execute(query).fetchall()
                db_conn.close()
                return results
            except Exception as e:
                print(e)
            db_conn.close()

    def listUserTransactionHistory(self, player_id, lookback=30):
        query = sqlalchemy.text("SELECT\
        t.id, p.name, t.amount, t.transaction_status, t.created_on\
        FROM transactions t\
        JOIN players p \
        ON p.id = t.player_id\
        WHERE t.created_on BETWEEN DATE_SUB(NOW(), INTERVAL {} DAY) AND NOW()\
        AND p.id = {}\
        ORDER BY t.created_on;".format(lookback, player_id))
        with self.pool.connect() as db_conn:
            try:
                results = db_conn.execute(query).fetchall()
                db_conn.close()
                return results
            except Exception as e:
                print(e)
            db_conn.close()

    def updateTransaction(self, transaction):
        query = sqlalchemy.text('UPDATE transactions SET transaction_status = :status WHERE id = :id;',)
        with self.pool.connect() as db_conn:
            try:
                db_conn.execute(query, id=transaction.transaction_id, status=transaction.status)
                print("Updated Transaction")
            except Exception as e:
                print(e)
            db_conn.close()

