import json
text = []
with open('./student_file.json', 'r') as f:
    json_data = json.load(f)

count = 0

for i in json_data["textAnnotations"]:
    text.append(i['boundingPoly']['vertices'])
    # for j in range(0,4):
    #     print(text[count][j]['x'],text[count][j]['y'])
    count = count + 1
    # print()

for x in range(0,count):
    print(text[x][0]['x'],text[x][0]['y'],text[x][2]['x'],text[x][2]['y'])
