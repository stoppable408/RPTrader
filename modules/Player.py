from modules import db

class Player():
    currentRP = 0
    name = None
    player_id = None

    def __init__(self, player_tuple):
        self.currentRP = player_tuple[2]
        self.name = player_tuple[1]
        self.player_id = player_tuple[0]


    def modify(self, number):
        try:
            rp = self.currentRP
            if (rp + number) < 0:
                raise Exception("There is not enough RP to perform this transaction")
            self.currentRP += number
        except Exception as e:
            raise Exception(e)

    def add(self, number):
        try:
            self.modify(number)
            self.update()
        except Exception as e:
            raise Exception(e)

    def subtract(self, number):
        try:
            self.modify(-number)
            self.update()
        except Exception as e:
            raise Exception(e)

    def give(self, player, number):
        try:
            self.subtract(number)
            player.add(number)
        except Exception as e:
            return Exception(e)

    def update(self):
        database = db.db()
        player_info = database.getUserByID(self.player_id)
        database.updateUser(self)
