import urllib3, boto3, json

def mutate(batch):
    nameMutes = ['name', 'title', 'game', 'itemname', 'full_name']

    for i in batch['collectors']:
        collKey = None
        for k in i['PutRequest']['Item'].keys():
            if k == 'collection' or k == 'collection_id':
                collKey = k
        if collKey:
            i['PutRequest']['Item']['uid'] = {'S': i['PutRequest']['Item'][collKey]['S'].split('_')[0]}
        
        for nM in nameMutes:
            if nM in i['PutRequest']['Item'].keys():
                i['PutRequest']['Item']['item_name'] = {'S': f"{i['PutRequest']['Item'][nM]['S']}_{i['PutRequest']['Item']['type']['S']}"}
        
    return batch

def getFile(URI):
    urlbase = "https://dynamodblabs.s3.amazonaws.com/collectors/data/"
    httppool = urllib3.PoolManager()
    response = httppool.request('GET', f'{urlbase}{URI}')
    return response.data.decode()

def handler(event, context):
    dynamodb = boto3.client('dynamodb')
    
    files = [
        "profiles.json",
        "activity.json",
        "adam/movies.json",
        "adam/boardgames.json",
        "corey/books.json",
        "craig/instruments.json",
        "john/comics.json",
        "john/movies.json"
    ]

    for f in files:
        rawData = getFile(f)
        jsonData = json.loads(rawData)
        mutatedData = mutate(jsonData)
        print(f'Writing: {f}')
        response = dynamodb.batch_write_item(
            RequestItems=mutatedData
        )
        print(f'Response: {response}')
