import json
import statistics
import pandas as pd

with open('output.json') as json_file:
    data = json.load(json_file)
    vals = list(map(lambda x: x['value'], data))

a = min(vals)
b = max(vals)

f = list(filter(lambda x: x['value'] == b, data))
#print(f[0])
f = list(filter(lambda x: x['value'] == a, data))
#print(f[0])

vals.sort()
#print(sorted(data, key = lambda i: i['value']))
df = pd.read_json('output1.json')
print(df.head())
df.to_csv('output.csv')
