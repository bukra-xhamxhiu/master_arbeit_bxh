from env.movies_env import MoviesPlaywrightEnv
from agents.heuristic_movies_agent import HeuristicMoviesAgent
from generation.test_plan_builder import TestPlanBuilder
from generation.playwright_code_generator import PlaywrightCodeGenerator
import os

if __name__ == "__main__":
    base_url = "http://localhost:3000"
    env = MoviesPlaywrightEnv(base_url=base_url, headless=False, max_steps=100)
    agent = HeuristicMoviesAgent(env)

    trace = agent.run()

    builder = TestPlanBuilder()
    test_plan = builder.build_test_plan(trace)
    print("Generated Test Plan:", test_plan)

    os.makedirs("tests/generated", exist_ok=True)
    output_path = "tests/generated/test_movies_ui_heuristic.py"

    generator = PlaywrightCodeGenerator()
    generator.generate_python_test(
        test_plan,
        output_path,
        base_url=base_url,
        test_name="test_movies_ui_heuristic",
    )

    print(f"Test saved to: {output_path}")
    env.close()
