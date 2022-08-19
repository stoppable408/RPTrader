from modules import db, Transaction


class Player():
    currentRP = 0
    name = None
    player_id = None

    def __init__(self, player_tuple):
        self.currentRP = player_tuple[2]
        self.name = player_tuple[1]
        self.player_id = player_tuple[0]


    def modify(self, number, transaction=None):
        print(number)
        try:
            rp = self.currentRP
            if (rp + number) < 0:
                raise Exception("There is not enough RP to perform this transaction")
            self.currentRP += number
            if not transaction:
                current_transaction = Transaction.Transaction(self.player_id, number, "Approved")
                current_transaction.addTransaction()
            else:
                transaction.update()
        except Exception as e:
            raise Exception(e)

    def add(self, number, transaction=None):
        try:
            self.modify(number, transaction)
            self.update()
        except Exception as e:
            raise Exception(e)

    def subtract(self, number):
        try:
            self.modify(-number)
            self.update()
        except Exception as e:
            raise Exception(e)

    def update(self):
        database = db.db()
        player_info = database.getUserByID(self.player_id)
        database.updateUser(self)

