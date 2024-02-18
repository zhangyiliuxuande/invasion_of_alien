class Settings:
    """存储游戏中所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255,255,255)
        self.frame_rate = 60

        #飞船设置
        self.ship_speed = 20.0

        #子弹设置
        self.bullet_speed = 10.0
        self.bullet_width = 10
        self.bullet_height = 50
        self.bullet_color = (0,0,0)
        self.bullet_allowed = 5