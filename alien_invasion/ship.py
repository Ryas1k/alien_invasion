import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Класс для управления кораблем"""
    def __init__(self, ai_game):
        """Инициализируем корабль и создаем его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect() #прямоугольник соответствует экрану 

        """Загружаем изображение и получаем прямоугольник"""
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect() #изображение помещается в прямоугольник такое же как изображеие

        """Каждый новый корабль появляется внизу по центру"""
        self.rect.midbottom = self.screen_rect.midbottom #середина корабля = середине экрана

        """Сохранения вещественной координаты центра корабля."""
        self.x = float(self.rect.x)

        #Флаг перемещения начинаем с неподвижного корабля
        self.moving_right = False
        self.moving_left = False
    def update(self):
        #обновление позиции корабля с учетом флагов
        """Обновляем атрибут х обьекта ship, не rect"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x  += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x  -= self.settings.ship_speed  
    #обновляем атрибут rect на основание self.x
        self.rect.x = self.x 
    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """Размещение корабля в центре экрана внизу"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
