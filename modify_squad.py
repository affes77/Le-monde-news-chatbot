import json

with open('formatted_squad_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

new_data = []

for item in data['data']:
    context = item['context']
    qas_list = []
    for qa in item['qas']:
        qas_list.append({
            'question': qa['question'],
            'id': qa['id'],
            'answers': qa['answers']
        })
    
    # check if context already exists
    context_exists = False
    for d in new_data:
        if d['context'] == context:
            d['qas'].extend(qas_list)
            context_exists = True
            break
    
    # if context doesn't exist, create new item
    if not context_exists:
        new_item = {
            'context': context,
            'qas': qas_list
        }
        new_data.append(new_item)

with open('formatted_squad_dataset.json', 'w', encoding='utf-8') as f:
    json.dump({'data': new_data}, f, ensure_ascii=False, indent=4)