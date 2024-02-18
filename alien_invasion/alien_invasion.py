import sys
import time

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("外星人入侵")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.create_flag = True
        

    def run_game(self):
        """开始游戏的主循环"""
        start_time = time.time()
        while True:
            self._check_events()
            self.ship.update()
            self._create_new_alien(start_time)
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
            #控制帧率
            self.clock.tick(self.settings.frame_rate)

    def _check_events(self):
        """侦听键盘和鼠标事件"""
        for event in pygame.event.get():
            #关闭
            if event.type == pygame.QUIT:
                sys.exit()
            #按键
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            #松键
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()


    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key ==pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """创建一颗子弹,并将其加入编组bullets"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_new_alien(self , start_time):
        """创建一个外星舰队"""
        #计时创建外星人
        time_passed = time.time() - start_time

        if int(time_passed) % self.settings.alien_create_rate  == 0 and self.create_flag:
            alien = Alien(self)
            self.aliens.add(alien)
            self.create_flag = False
            print(time_passed)
        elif int(time_passed) % self.settings.alien_create_rate != 0:
            self.create_flag = True

    def _update_aliens(self):
        """更新外星飞船位置并删除到达底边的外星人"""
        self.aliens.update()

        #删除到达底边的外星人
        for alien in self.aliens.copy():
            if alien.rect.bottom >= self.settings.screen_height:
                self.aliens.remove(alien)
                sys.exit()


    def _update_bullets(self):
        """更新子弹位置并删除已消失的子弹"""
        self.bullets.update()

        #删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)

        #删除击中外星人的子弹和飞船
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)

    def _update_screen(self):
        """更新屏幕上的图像，并切换至新屏幕"""
        #重绘屏幕
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets:
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        
        #使更新的屏幕可见
        pygame.display.flip()


#if __name__ == 'main':
    #创建游戏实例并运行游戏
ai = AlienInvasion()
ai.run_game()