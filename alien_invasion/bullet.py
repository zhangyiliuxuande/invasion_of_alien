import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理飞船所有子弹的类"""

    def __init__(self,ai_game):
        """创建子弹对象"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #加载子弹图像，获取外接矩形
        self.image = pygame.image.load('images/bullet.bmp')
        self.rect = self.image.get_rect()

        #self.rect = pygame.Rect(0,0,self.settings.bullet_width,
            #self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #用浮点数表示子弹位置
        self.y = float(self.rect.y)

    def  update(self):
        """向上移动子弹"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        self.screen.blit(self.image,self.rect)
