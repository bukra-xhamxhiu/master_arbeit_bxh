from typing import List

from env.movies_env import MoviesPlaywrightEnv


class HeuristicMoviesAgent:
    """
    Assumes MoviesPlaywrightEnv.reset() returns an already logged-in state.

    Scenario:
      1) Open user profile menu
      2) Create a new list
      3) Open the list under "My Lists"
      4) Open "Add/Remove Movies"
      5) Try to add one or more movies by title
    """

    def __init__(self, env: MoviesPlaywrightEnv):
        self.env = env

    def run(self) -> list[dict]:
        # 1) Start from a logged-in state (handled by env.reset + localStorage)
        state = self.env.reset()
        print(f"Initial URL: {state['url']}")

        # 2) Run the fixed scenario
        self._create_list_and_add_movies(
            list_name="my favorite movies",
            list_description="here is a list of my favorite movies",
            movie_titles=["Twisters", "Bad Boys: Ride or Die"],
        )

        # 3) Return the trace for test generation
        return self.env.trace

    # ------------------------------------------------------------------ #
    #  Main scenario
    # ------------------------------------------------------------------ #
    def _create_list_and_add_movies(
        self,
        list_name: str,
        list_description: str,
        movie_titles: List[str],
    ) -> None:
        """
        Perform:
          - open profile menu
          - create new list
          - open list from "My Lists"
          - open "Add/Remove Movies"
          - add movies
        """

        print("\n=== CREATE LIST & ADD MOVIES SEQUENCE ===")

        # Open user profile menu in the header
        # (Adjust "User Profile" to whatever aria-label is used in your app)
        self.env.step(
            {
                "type": "click_by_label",
                "label": "User Profile",
            }
        )

        # Click "Create New List"
        self.env.step(
            {
                "type": "click_by_role",
                "role": "link",
                "name": "Create New List",
            }
        )

        # Fill list name and description
        self.env.step(
            {
                "type": "fill_by_label",
                "label": "Name",
                "text": list_name,
            }
        )
        self.env.step(
            {
                "type": "fill_by_label",
                "label": "Description",
                "text": list_description,
            }
        )

        # Submit the list creation
        self.env.step(
            {
                "type": "click_by_role",
                "role": "button",
                "name": "Continue",
            }
        )

        # Go to "My Lists"
        self.env.step(
            {
                "type": "click_by_role",
                "role": "link",
                "name": "My Lists",
            }
        )

        # Open the specific list
        self.env.step(
            {
                "type": "click_by_role",
                "role": "link",
                "name": list_name,
            }
        )

        # Open "Add/Remove Movies"
        self.env.step(
            {
                "type": "click_by_role",
                "role": "button",
                "name": "Add/Remove Movies",
            }
        )

        # Add each movie by title
        for title in movie_titles:
            print(f"  -> Try to add movie: {title}")

            # Type into the search field in the Add/Remove dialog
            # Adjust placeholder text to what your app actually uses
            self.env.step(
                {
                    "type": "fill_by_placeholder",
                    "placeholder": "Search for a movie",
                    "text": title,
                }
            )

            # Press Enter to trigger the search (if applicable)
            self.env.step(
                {
                    "type": "press_key",
                    "key": "Enter",
                }
            )

            # Click an "Add" button for that movie
            # You may need to adjust 'name' depending on the real button text.
            # Option 1: "Add <title>"
            self.env.step(
                {
                    "type": "click_by_role",
                    "role": "button",
                    "name": f"Add {title}",
                }
            )

            # If your UI only shows "Add", use this instead:
            # self.env.step(
            #     {
            #         "type": "click_by_role",
            #         "role": "button",
            #         "name": "Add",
            #     }
            # )
