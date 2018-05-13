import json
import random
pointLst = []
nameLst = ["火锅", "网吧"," 自助餐", "修电脑","通马桶","卖电脑","超市","便利店","理发店","菜场"]
i = 0
while i < 10:
    t = {"x":random.uniform(32.03,32.07),
         "y":random.uniform(118.72,118.78)}
    t["information"] = nameLst[i]

    pointLst.append(t)
    i += 1

menu_json = json.dumps(pointLst, ensure_ascii=False)
print(menu_json)

with open('static/test.json', 'w', encoding='utf-8') as f:
    f.write(menu_json)