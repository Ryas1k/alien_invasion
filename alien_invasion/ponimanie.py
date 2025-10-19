class Oryshie:
    def __init__(self, name=10, damage=100):
        self.name = name
        self.damage = damage
    def dama(self):
        print(f'{self.name}, {self.damage}')

class Igrok:
    def __init__(self,name):
        self.name_igrok = name
        self.oryshie = Oryshie()

    def got_oryshie(self):
        print(f'{self.name_igrok} взял оружие {self.oryshie.name} и нанес {self.oryshie.damage}')

or1 = Oryshie('пистолет', 10)
igr = Igrok('Игорь')
igr.got_oryshie()