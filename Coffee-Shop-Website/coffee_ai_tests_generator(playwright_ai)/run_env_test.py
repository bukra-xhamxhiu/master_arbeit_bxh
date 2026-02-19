from env.coffee_env import CoffeePlaywrightEnv

BASE_URL = "https://lchua2314.github.io/Coffee-Shop-Website/dist/index.html"  

env = CoffeePlaywrightEnv(BASE_URL, headless=False)

print("=== RESET ===")
state = env.reset()
print("Initial URL:", state["url"])

# 1) CLICK MENU
print("=== CLICK MENU ===")
action = {"type": "click", "selector": "text=Menu"}
next_state, reward, done, info = env.step(action)

print("Reward:", reward)
print("Info:", info)

# wait so you can SEE the result
env.page.wait_for_timeout(1500)

# 2) SCROLL DOWN
print("=== SCROLL DOWN ===")
scroll_action = {"type": "scroll", "amount": 600}
next_state, reward, done, info = env.step(scroll_action)

print("Reward after scroll:", reward)
print("New URL:", next_state["url"])
print("DOM length:", len(next_state["dom"]))

# wait again to observe
env.page.wait_for_timeout(1500)

# close
env.close()
