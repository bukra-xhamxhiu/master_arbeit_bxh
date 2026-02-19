from env.coffee_env import CoffeePlaywrightEnv
from  env.actions import get_clickable_elements

env = CoffeePlaywrightEnv("http://localhost:5500/dist/index.html", headless=False)
env.reset()

elems = get_clickable_elements(env.page)
print("Clickable elements found:", len(elems))

for e in elems[:100]:   # show first 10
    print(e)

env.close()
