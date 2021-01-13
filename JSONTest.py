import json
# result=dict()
# result1=dict()
# result["key"]="你好"
# result["value"]="你好啊ccc aa sdf"
# result1["key"]="你好啊ccc aa sdf"
# result1["value"]="你好啊ccc aa sdf"
# l=[]
# l.append(result)
# l.append(result1)
# with open("test.json","w",encoding="utf-8") as f:
#     json.dump(l,f)
with open("result_5.json","r",encoding="gbk") as f:
    print(json.load(f))
# with open("result2.json","r",encoding="gbk") as f:
#     t=json.load(f)
# print(t)
# print(len(t))

