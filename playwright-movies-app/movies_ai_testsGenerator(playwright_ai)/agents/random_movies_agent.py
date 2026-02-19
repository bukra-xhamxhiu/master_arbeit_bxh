import random
from env.movies_env import MoviesPlaywrightEnv
from env.movies_actions import get_clickable_elements, create_click_action


class RandomMoviesAgent:
    def __init__(self, env: MoviesPlaywrightEnv, steps: int = 12):
        self.env = env
        self.steps = steps

    def run(self):
        state = self.env.reset()

        for _ in range(self.steps):
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
