import random

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """管理所有外星人的类"""

    def __init__(self,ai_game):
        """初始化外星人并设置起始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        #加载外星人图像，获取外接矩形
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #随机外星人位置
        self.rect.bottom = 100
        self.rect.right = random.randint(self.rect.width,self.screen_rect.right)

        #存储精确竖直位置
        self.y = float(self.rect.y)

    def update(self):
        """向下移动外星人"""
        self.y += self.settings.alien_speed
        self.rect.y = self.y