class Settings():
    """Класс для хранения всех настроект игры."""

    def __init__(self):
        """Инициализирует статические настройки игры"""
        # параметры экрана
        self.screen_width = 1000
        self.screen_height = 600
        #Задаем цвет экрана
        self.bg_color = (230,230,230)

        #Настройка корабля
        self.ship_limit = 3
        #Параметры и настройки снаряда
        
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 30
        #Настройка пришельцев
        
        self.fleet_drop_speed = 10 #вниз 
        
        #Темп ускорения игры
        self.speedup_scale = 1.1

        #Темп роста стоимости пришельца
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инизиализирует настройки изменяющиеся в ходе игры"""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0
        # fleet_direction движение вправо = 1, а -1 влево
        self.fleet_direction = 1
        #Подсчет очков
        self.alien_points = 50
        #print(self.alien_points)
    
    def increase_speed(self):
        """Увеличиваем настройки скорости и стоимости пришельца"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)