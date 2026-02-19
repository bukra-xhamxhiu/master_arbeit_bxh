from playwright.sync_api import Page


BASE_URL = "http://localhost:3000"


def test_generated_kanban_flow(page: Page):
    page.goto(BASE_URL, wait_until="networkidle")

    # Step 0: button:+ Add New Task
    page.get_by_role("button", name="+ Add New Task").click()
    # Step 1: button:+ Add New Subtask
    page.get_by_role("button", name="+ Add New Subtask").click()
    # Step 2: button:Create Task
    page.get_by_role("button", name="Create Task").click()
    # Step 4: button + Add New Subtask
    page.locator("button.add-column-btn").first.click()
    # Step 5: button Create Task
    page.locator("button.create-btn").first.click()

    # Basic smoke assertion: page is still on the app
    assert "http://localhost:3000" in page.url
