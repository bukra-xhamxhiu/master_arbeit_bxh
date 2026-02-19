from env.coffee_env import CoffeePlaywrightEnv
from agents.random_agent import RandomAgent
from generation.test_plan_builder import TestPlanBuilder
from generation.playwright_code_generator import PlaywrightCodeGenerator
import os

BASE_URL = "http://localhost:5500/dist/index.html"

env = CoffeePlaywrightEnv(BASE_URL, headless=False, max_steps=10)
agent = RandomAgent(env, steps=10)
trace = agent.run()

builder = TestPlanBuilder()
test_plan = builder.build_test_plan(trace)

print("Generated Test Plan:", test_plan)

output_file = os.path.join("tests", "generated", "test_generated_ui.py")

generator = PlaywrightCodeGenerator()
generator.generate_python_test(test_plan, output_file)

print("Test saved to:", output_file)
