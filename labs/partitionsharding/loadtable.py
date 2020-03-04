import boto3, json, os
from botocore.config import Config
from multiprocessing import Process, Queue

def transform(data):
    for d in data:
        if "asin" in d.keys():
            d['Partition']['S'] = f"{d['Partition']['S']}_{d['asin']['S'][:5]}"
    return data

def loader(filename, unprocessed):
    configuration = Config(retries = dict(max_attempts = 1))
    items = json.loads(''.join(open(f'./dataload/{filename}', 'r').readlines()))
    while len(items) > 0:
        if len(items) >= 25:
            chunk = items[:25]
            del items[:25]
        else:
            chunk = items
            del items[:]

        unprocessedItems = []
        chunk = transform(chunk)
        chunk = [{"PutRequest": {"Item": i}} for i in chunk]

        dynamodb = boto3.client('dynamodb', config = configuration)
        try:
            response = dynamodb.batch_write_item(
                RequestItems={"AmazonBins": chunk}
            )
            if isinstance(response['UnprocessedItems'], dict):
                for i in response['UnprocessedItems'].values():
                        unprocessedItems.append(i)
        except Exception as e:
            unprocessed.put(e)
        
    unprocessed.put(unprocessedItems)

def main():
    processes = []
    unprocessed = Queue()
    files = os.listdir('./dataload')
    
    for filename in files:
        vars()[filename] = Process(target=loader, args=(filename, unprocessed))
        processes.append(vars()[filename])
    
    for p in processes:
        p.start()

    lostItems = []
    while True:
        try:
            result = unprocessed.get(False, 0.01)
            lostItems.append(result)
        except Exception:
            pass
        allExited = True
        for p in processes:
            if p.exitcode is None:
                allExited = False
                break
        if allExited and unprocessed.empty():
            break

    for p in processes:
        p.join()

    for lI in lostItems:
        try:
            print(json.dumps(lI, sort_keys = True, indent = 4, separators = (',', ': ')))
        except Exception:
            print(lI)

if __name__ == "__main__":
    main()