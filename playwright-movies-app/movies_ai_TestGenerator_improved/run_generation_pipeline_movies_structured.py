# run_generation_pipeline_movies_structured.py
from env.movies_env import MoviesPlaywrightEnv
from agents.structured_movies_agent import StructuredMoviesAgent
from generation.structured_test_plan_builder import StructuredTestPlanBuilder
from generation.multi_file_code_generator import MultiFileCodeGenerator


def main() -> None:
    # Use the URL that already shows movies; in this app it's usually Popular page
    base_url = "http://localhost:3000/?category=Popular&page=1"

    env = MoviesPlaywrightEnv(base_url=base_url, headless=False, max_steps=40)
    agent = StructuredMoviesAgent(env)
    builder = StructuredTestPlanBuilder()
    codegen = MultiFileCodeGenerator()

    try:
        trace = agent.run()

        grouped_plans = builder.build(trace)

        print("\n=== GROUPED TEST PLANS ===")
        for group_name, steps in grouped_plans.items():
            print(f"  {group_name}: {len(steps)} steps")

        output_dir = "tests/generated"
        codegen.generate_tests_by_group(grouped_plans, base_url=base_url, output_dir=output_dir)

    finally:
        env.close()


if __name__ == "__main__":
    main()
