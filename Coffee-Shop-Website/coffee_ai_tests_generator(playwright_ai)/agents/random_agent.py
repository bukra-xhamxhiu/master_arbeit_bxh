import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from env.coffee_env import CoffeePlaywrightEnv
from env.actions import get_clickable_elements, create_click_action
import random


class RandomAgent:
    def __init__(self, env: CoffeePlaywrightEnv, steps: int = 300):
        self.env = env
        self.steps = steps

    def run(self):
        state = self.env.reset()

        for step in range(self.steps):
            clickable = get_clickable_elements(self.env.page)

            if not clickable:
                break

            choice = random.choice(clickable)
            action = create_click_action(choice["selector"])

            next_state, reward, done, info = self.env.step(action)

            if done:
                break

        self.env.close()
        return self.env.trace
