import pygame

class Ship:
    """管理飞船的类"""

    def __init__(self,ai_game):
        """初始化飞船及其初始位置"""
        #显示窗口位置范围
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        #加载飞船图象，获取外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #新飞船在底部中央
        self.rect.midbottom = self.screen_rect.midbottom

        #在飞船属性x中存储一个浮点数
        self.x = float(self.rect.x)

        #移动标志
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """绘制飞船"""
        self.screen.blit(self.image,self.rect)

    def update(self):
        """根据移动标志调整飞船位置"""
        #更新浮点数属性x的值
        if self.moving_right and self.rect.right <= self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left >=self.screen_rect.left:
            self.x -= self.settings.ship_speed

        #根据self.x更新rect对象
        self.rect.x = int(self.x)