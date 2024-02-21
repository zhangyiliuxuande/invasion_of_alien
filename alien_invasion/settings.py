class Settings:
    """存储游戏中所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255,255,255)
        self.frame_rate = 60

        #飞船设置
        self.ship_limit = 3

        #子弹设置
        self.bullet_allowed = 5
        
        #以什么速度加快游戏的节奏
        self.speedup_scale = 1.2
        self.alien_num_boundary = 10

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 3
        self.bullet_speed = 2.5
        
        #外星人设置
        self.alien_speed = 1.0
        self.alien_create_rate = 3.0

        #记分设置
        self.alien_points = 10

    def increase_speed(self):
        """提高速度设置的值"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_create_rate /= self.speedup_scale
        self.alien_points = self.alien_points * self.speedup_scale