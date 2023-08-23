from logging import Formatter
from logging import getLogger
from logging import INFO
from logging import StreamHandler


logger = getLogger(__name__)
fmt = Formatter(fmt="%(asctime)s - %(levelname)s:%(name)s - %(message)s")
handler = StreamHandler()
handler.setFormatter(fmt)
logger.addHandler(handler)


class Individual:

    def __init__(self, name: str, rate: float = 1500, verbose: bool=False):
        """
        Parameters
        -----
        name: str
            識別子
        rate : float
            elo_rating
        """
        self.name = name
        self.rate = rate

        # logger
        self.verbose = verbose
        self.logger = getLogger(f"{__name__}.{self.name}")

        if self.verbose:
            self.logger.setLevel(INFO)

    def __str__(self):
        return self.name

    def __lt__(self, other: "Individual"):
        return self.rate < other.rate

    def __gt__(self, other: "Individual"):
        return self.rate > other.rate

    def win_rate(self, other: "Individual", h: float=0) -> float:
        """
        レーティング上の勝率を計算

        Parameters
        -----
        other: Individual
            勝率を計算する相手
        h: float, default 0
            環境などに依存する補正項
        """

        return 1 / (10 ** ((other.rate - self.rate + h) / 400) + 1)

    def update_rate(self, other: "Individual", n_wins: float, n_games: int, h: float=0, k: float=32):
        """
        ratingを更新する

        Parameters
        -----
        other: Individual
            対戦相手
        n_wins: float
            対戦相手に対して勝利した回数
        n_games: int
            対戦相手と行ったレーティング試合数
        h: float, default 0
            環境などに依存する補正項
        k: float
            ratingの更新幅

        Notes
        -----
        kが大きいと収束が早いが、収束後も変化が大きい
        kが小さいと収束が遅いが、全体的に安定する
        """

        if self.verbose:
            self.logger.info(
                f"Updating rating of {self.name} bases on results of the match against {other.name}."
            )
            self.logger.info(f"rating {self.name}: {self.rate} - {other.name}: {other.rate}")
        # 現在のratingからの期待値勝率を計算
        win_rate = self.win_rate(other, h)

        if self.verbose:
            self.logger.info(f"Win rate of {self.name}: {win_rate}.")
            self.logger.info(f"The number of games: {n_games}.")
            self.logger.info(f"The number of {self.name} wins: {n_wins} ")

        # ratingの更新
        current_rate = self.rate
        rate_diff = k * (n_wins - n_games * win_rate)
        self.rate = self.rate + rate_diff

        if self.verbose:
            self.logger.info(f"Updated rating of {self.name}.")
            self.logger.info(f"{current_rate: .3f} -> {self.rate: .3f}")

        
        
