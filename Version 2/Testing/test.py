import json
x = {
        "name": "john",
        "age": 30,
        "city": "here"
        }

print(x["name"])
y = json.dumps(x)
x['age'] = 10
print(x)
print(y)
