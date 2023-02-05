from random_agent import RandomAgent
from game import Game
from ai_tabu_agent import AIAgent1
from tabu_with_improvedSpy import AIAgent


def init():
    global spy_win_num
    global mine_win_num1
    global mine_win_num2


init()
spy_win_num = 0
mine_win_num1 = 0
mine_win_num2 = 0
agents = [AIAgent(name='r1'),
          AIAgent1(name='r2'),
          AIAgent(name='r3'),
          AIAgent1(name='r4'),
          AIAgent(name='r5'),
          AIAgent1(name='r6'),
          AIAgent(name='r7')]

# testing
for i in range(1000):
    game = Game(agents)
    game.play()
    print(game)
print(spy_win_num)
print(f'my agent spy win {mine_win_num1/3}, resistant win {mine_win_num2/4}')
