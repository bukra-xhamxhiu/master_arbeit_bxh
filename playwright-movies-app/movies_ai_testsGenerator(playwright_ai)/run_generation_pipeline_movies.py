from env.movies_env import MoviesPlaywrightEnv
from agents.random_movies_agent import RandomMoviesAgent
from generation.test_plan_builder import TestPlanBuilder
from generation.playwright_code_generator import PlaywrightCodeGenerator
import os

BASE_URL = "http://localhost:3000/"

env = MoviesPlaywrightEnv(BASE_URL, headless=False, max_steps=12)
agent = RandomMoviesAgent(env, steps=12)
trace = agent.run()

builder = TestPlanBuilder()
test_plan = builder.build_test_plan(trace)

print("Generated Test Plan:", test_plan)

output_file = os.path.join("tests", "generated", "test_movies_ui.py")

generator = PlaywrightCodeGenerator()
generator.generate_python_test(test_plan, output_file)

print("Test saved to:", output_file)
