import stocktwits
import json

ids = []

while True:
    try:
        j = stocktwits.get_stock_stream('googl')
        msgs = j['messages']
        for msg in msgs:
            if msg['id'] not in ids:
                ids.append(msg['id'])
                with open('stocktwits_7-4-18.json', 'a') as f:
                    f.write(json.dumps(msg))
    except Exception:
        continue
