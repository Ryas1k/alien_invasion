import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Класс для управления ресурсами и повведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')
        # Создание экземпляров для хранения игровой статистики и панели результатов
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        #Игра запускается в неактивном состоянии
        self.game_active = False

        #Создание кнопки играть
        self.play_button = Button(self,'Играть')
        

    def run_game(self):
        """Запускается основной цикл игры"""
        while True:
            self._check_events()
            if self.game_active:

                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Отслеживает события клавиатуры и мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)    
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit() 
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """Реагирует на отпускание клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _fire_bullet(self):
        """Создает новый снаряд и добавляет его в группу bullets."""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляем позицию снарядов и уничтожаем старые снаряды."""
        #Обновление позиции
        self.bullets.update()
        #Удаление снарядов,вышедших за край
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
    def _check_bullet_alien_collisions(self):
        #обрабатывает коллизии снарядов и пришельцев
        #Проверка попадания в пришельца
        #При попадании удалить снаряд и пришельца
        collisions = pygame.sprite.groupcollide(
            self.bullets,self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            #Уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #Увеличение уровня
            self.stats.level += 1
            self.sb.prep_level()
    
    def _update_screen(self):
        #При каждом проходе цикла перерисовывается экран.
            self.screen.fill(self.settings.bg_color)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet() 
            self.ship.blitme()
            self.aliens.draw(self.screen)

            #вывод информации о счете
            self.sb.show_score()

            #Кнопка играй отображатся в том случае если она неактивная
            if not self.game_active:
                self.play_button.draw_button()
            # Отображение последнего прорисованного экрана.
            pygame.display.flip()

    def _create_fleet(self):
        """Создает флот пришельцев"""
        #Создание пришельца и добавление других пока остается место.
        #Растояние между пришельцами составляет одну ширину
        # и одну высоту пришельца.
        alien = Alien(self)
        alien_width, alien_height =alien.rect.size 
        current_x, current_y = alien_width, alien_height #следующая позиция пришельца
        while current_y < (self.settings.screen_height - 6 * alien_height):
            while current_x < (self.settings.screen_width - 3 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width 
            #конец ряда сбрасываем х и увеличиваем у
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self,x_position, y_position):
        #Создание пришельца и вычисление количества пришельцев в ряду
        #Интервал между пришельцами равен ширине пришельца
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Реагирует при достижения пришельца края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        """Опускает весь флот и меняет его направление"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте."""
        # Проверяем достиг ли флот края экрана, с последующим
        # обновлением всего флота
        self._check_fleet_edges()
        self.aliens.update()
        # Проверка коллизий пришелец - корабль
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        #Проверка сталкивается ли пришелец с нижней частью экрана
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем"""
        if self.stats.ships_left > 0:
            #уменьшение ships_left -= 1 и обновление панели счета
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Очистка групп
            self.aliens.empty()
            self.bullets.empty()
            #Создание нового флота и размещение корабля в центре
            self._create_fleet() 
            self.ship.center_ship()
            #Пауза
            sleep(1.0)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Проверяет добрались ли пришельцы до нижнего края экрана"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #происходит тоже что и при столкновении с кораблем
                self._ship_hit()
                break
    
    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки играть"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #сброс игровой статистики
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            #очистка группы aliens and bullets
            self.bullets.empty()
            self.aliens.empty()
            #Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()
            #Указатель мыши скрывается
            pygame.mouse.set_visible(False)

if __name__ == '__main__':
    #Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
