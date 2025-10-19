class GameStats:
    """Отслеживает статистику для игры Инопланетное вторжение"""

    def __init__(self, ai_game):
        """инициализируем статистику"""
        self.settings = ai_game.settings
        self.reset_stats()
        #Рекорд не должен сбрасываться
        self.high_score = 0
        

    def reset_stats(self):
        """инициализирует статистику, изменяющуюся в ходе игры"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1