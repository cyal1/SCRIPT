from pychrome import Browser
from pychrome.cli import JSONTabEncoder
import json

def getTabById(tabs, tab_id):
    for tab in tabs:
        if tab.id == tab_id:
            return tab
    return None

# 假设你的Chrome浏览器正在运行且远程调试端口为9222
browser = Browser(url="http://localhost:9222")

try:
    tabs = browser.list_tab()
except Exception as e:
    print(e, "\n\nYou need run chrome with debugging mode:\n/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222\n")
    exit(-1)


print("select the tab")
index = 1
tab_map = {}
for tab in json.loads(json.dumps(tabs, cls=JSONTabEncoder, indent=4)):
    print(index, tab.get("id"), tab.get("title"), tab.get("url"))
    tab_map[index] = tab.get("id")
    index += 1

input_num = int(input("select the tab number: "))
target_id = tab_map[input_num]

tab = getTabById(tabs, target_id)

if tab is None:
    print("Not found tab: ", target_id)
    exit(-1)

tab.start()


for i in range(20):
    result = tab.call_method("Runtime.evaluate", expression=f"test2(100,{i})")
    print(result)



