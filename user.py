class User:
    def __init__(self, id):
        '''
        конструктор
        :param id: идентификатор юзера
        '''
        self.id = id
        self.balance = 100
        self.starting_game = False