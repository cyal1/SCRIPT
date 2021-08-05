import requests
import json
import sys



keywords=["url","path","pass","dir","link","file","name","cmd","command","exec","upload","download","Upload","上传","文件","读取","导出","导入"]

# res = set()

with open(sys.argv[1]) as f:
   j = json.load(f)
# print(j)
apiList = j["paths"]

# print(apiList)
for api in apiList:
    router = api
    # print(router)

    for key in apiList[api]:
        method = key
        # print(method)
        # if method == 'get':
        # ct = apiList[api][key]["consumes"] # content-type
        # apiList[api][key]
        tag = apiList[api][key]["tags"]
        desc = apiList[api][key]["summary"]

        for search in keywords:
            if search in router or search in desc: # or "multipart" in ct or "www" in ct:
                # print(search+": ")
                print(router,desc,method,tag,search)
                # print("--------")
                # print(apiList[api])
                # print("-----")


        # print(ct,tag,desc)
        # print("描述:",desc)
        for parm in apiList[api][key]:
            if parm == "parameters":
                for p in apiList[api][key][parm]:
                    # print(p['name'],p['in'],p['required'])
                    for search in keywords:
                        if search in p['name']:
                            # print(search+": ")
                            print(router,desc,method,p,tag,search)
                            # print("--------")
                            # print(apiList[api])
                            # print("-----")
                # print(parm)

    # print("")
    # break