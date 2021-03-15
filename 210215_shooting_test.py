import gym
from gym import spaces
import numpy as np
import threading
import time
import sys
from PyQt5.QtWidgets import *
import shooting_210215 as shoot

# Agent 가 학습할 때 사용하는 환경을 제공하는 클래스
# Agent 는 학습을 위해 이 클래스의 멤버변수인 action_space, observation_sapace 를 사용하고
# step(), reset() 함수를 호출할 것이므로 이들 변수와 함수를 통해서 게임이 시작되어 작동하며
# 종료될 수 있어야 한다.
# 이 게임은 step()함수가 1000번 호출되면 1회의 에피소드가 실행된 것으로 작성하였다

class GameEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(GameEnv, self).__init__()

        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        #self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        # Example for using image as input:
        #self.observation_space = spaces.Box(low=0, high=380, shape=
        #(HEIGHT, WIDTH, N_CHANNELS), dtype=np.uint8)

        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0, high=380, shape=(2,), dtype=np.float32)

        self.score = 0
        self.total_scores = 0
        self.done = False
        self.counts = 0

        #게임 클래스에 게임루프(무한루프)가 실행되므로 현재 코드와 동시에 실행하도록 하려면 Thread 가 필요함
        self.game = None
        self.game_thread = threading.Thread(target=self.game_window)
        #self.game_thread.daemon = True   # 여기서는 절대 사용 금지
        self.game_thread.start()

        print('Env 생성')

    # 게임을 쓰레드로 실행하기 위해 함수에 포함
    def game_window(self):
        app = QApplication(sys.argv)
        self.game = shoot.MainWindow()
        self.game.show()
        app.exec_()

    def step(self, action):
        self.score = 0
        if action==0:
            if self.game.whtBall.x > 0:
                self.game.move_left()
                if self.game.redBall.x < self.game.whtBall.x:
                    self.score = 1
        elif action==1:
            if self.game.whtBall.x < 380:
                self.game.move_right()
                if self.game.redBall.x > self.game.whtBall.x:
                    self.score = 1
        elif action==2:
            self.game.fire()
            if (self.game.whtBall.x-10 < self.game.redBall.x) and (self.game.whtBall.x+10 > self.game.redBall.x):
                self.score = 1
        self.counts += 1
        if self.counts == 1000:
            self.done = True
        self.total_scores += self.score
        obs = [self.game.redBall.x, self.game.whtBall.x]
        return obs, self.score, self.done, {}

    def render(self, mode='human'):
        pass

    def reset(self):
        self.total_scores = 0
        self.counts = 0
        self.done = False
        self.game.init_ball()
        obs = [self.game.redBall.x, self.game.whtBall.x]
        return obs

    # Env 작동 테스트
    def test(self):
        while not self.game:
            time.sleep(0.1)
        for i in range(1, 101):  # 100회의 에피소드 테스트
            obs = self.reset()

            while not self.done:
                action = self.action_space.sample()
                obs, score, done, _ = self.step(action)
                print('Episode:', i, 'Step:', self.counts, 'Score:',self.score, 'Total Score:', self.total_scores)
                time.sleep(0.03)


#gameEnv = GameEnv()
#gameEnv.test()



