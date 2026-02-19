from env.coffee_env import CoffeePlaywrightEnv
from agents.random_agent import RandomAgent

BASE_URL = "http://localhost:5500/dist/index.html" 

env = CoffeePlaywrightEnv(BASE_URL, headless=False, max_steps=20)

agent = RandomAgent(env, steps=10)
agent.run()
