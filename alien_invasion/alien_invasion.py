import sys
import time

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import ScoreBoard

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

        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.create_flag = True
        self.stats.alien_collision = 0
        self.stats.last_alien_collision = 0

        #创建记分牌
        self.scorebord = ScoreBoard(self)

        #游戏启动后处于活动状态
        self.game_active = False

        #创建Play按钮
        self.play_button = Button(self, "PLAY")

    def run_game(self):
        """开始游戏的主循环"""
        start_time = time.time()
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._create_new_alien(start_time)
                self._update_bullets()
                self._update_aliens()
                self._speed_up()
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
            #按下鼠标
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
        """在玩家单击Play按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #还原游戏设置
            self.settings.initialize_dynamic_settings()
            
            #重置游戏的统计信息
            self.stats.reset_stats()
            self.game_active = True

            #清空外星人和子弹列表
            self.bullets.empty()
            self.aliens.empty()

            #将飞船放在底部中央
            self.ship.center_ship()

            #隐藏光标
            pygame.mouse.set_visible(False)

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
        mod = time_passed % self.settings.alien_create_rate

        if mod <= 0.1 and self.create_flag:
            alien = Alien(self)
            self.aliens.add(alien)
            self.create_flag = False
        elif mod > 0.1  :
            self.create_flag = True

    def _update_aliens(self):
        """更新外星人位置并删除碰到飞船和到达底边的外星人"""
        self.aliens.update()

        #外星人与飞船碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        #外星人到达底边和碰到飞船一样处理
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break



    def _update_bullets(self):
        """更新子弹位置并删除已消失的子弹"""
        self.bullets.update()

        #删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0: 
                self.bullets.remove(bullet)

        #删除击中外星人的子弹和飞船
        if pygame.sprite.groupcollide(self.bullets,self.aliens,True,True):
            self.stats.alien_collision += 1
            self.stats.score += self.settings.alien_points
            self.scorebord.prep_score()

    def _update_screen(self):
        """更新屏幕上的图像，并切换至新屏幕"""
        #重绘屏幕
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets:
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        #显示得分
        self.scorebord.show_score()
        
        #如果游戏处于非活动状态，就绘制Play按钮
        if not self.game_active:
            self.play_button.draw_button()

        #使更新的屏幕可见
        pygame.display.flip()

    def _ship_hit(self):
        """响应外星人和飞船的碰撞"""
        if self.stats.ships_left > 0:
            #将ship_left减1
            self.stats.ships_left -= 1

            #清空外星人列表
            self.aliens.empty()

            #将飞船放在屏幕底部中央
            self.ship.center_ship()

            #暂停
            time.sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _speed_up(self):
        """加快游戏的速度"""
        print(self.stats.alien_collision)
        if self.stats.alien_collision % 10 == 0 and self.stats.alien_collision > self.stats.last_alien_collision:
            self.settings.increase_speed()
            self.stats.last_alien_collision = self.stats.alien_collision


#if __name__ == 'main':
    #创建游戏实例并运行游戏
ai = AlienInvasion()
ai.run_game()