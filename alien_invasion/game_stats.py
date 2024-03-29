class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self,ai_game):
        """初始化统计信息"""
        self.high_score = 0
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """初始化游戏运行时可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.alien_collision, self.last_alien_collision = 0, 0
        self.score = 0