import random
import string
import datetime
from modules import db


class Transaction():
    transaction_id = None
    player_id = None
    amount = None
    status = None
    created_on = None


    def __init__(self, player_id, amount, status, created_on=None, transaction_id = None):
        self.player_id = player_id
        self.amount = amount
        self.status = status

        if not transaction_id:
            self.transaction_id = ''.join(random.choice((string.ascii_uppercase + string.digits)) for x in range(10))
        else:
            self.transaction_id = transaction_id

        if not created_on:
            self.created_on = datetime.datetime.now()
        else:
            self.created_on = created_on

    def addTransaction(self):
        database = db.db()
        database.insertTransaction(self)

    def update(self):
        database = db.db()
        database.updateTransaction(self)
    
    
