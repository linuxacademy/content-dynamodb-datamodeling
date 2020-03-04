import urllib3, boto3, json, argparse

def mutate(batch):
    for i in batch:
        if 'AllCapability' in i.keys():
            starbucks = 0
            cvs = 0
            for val in i['AllCapability']['L']:
                if 'Starbucks' in val.values():
                    starbucks = 1
                if 'CVS pharmacy' in val.values():
                    cvs = 1
            i['Starbucks'] = {'S': str(starbucks)}
            i['CVS'] = {'S': str(cvs)}

        city = list(i['Address.City'].values())
        postalCode = list(i['Address.PostalCode'].values())
        i['CityZip'] = {'S': f"{city[0]}#{postalCode[0]}"}
    
    return batch

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', '--table', required = True, help = "Table name to load data into")
    args = vars(ap.parse_args())
    tableName = args['table']

    URI = "https://dynamodblabs.s3.amazonaws.com/datarelationships/target.json"
    httppool = urllib3.PoolManager()
    response = httppool.request('GET', URI)
    rawData = response.data.decode()

    jsonData = json.loads(rawData)
    mutatedData = mutate(jsonData)
    chunks = [mutatedData[i * 25:(i+1) * 25] for i in range((len(mutatedData) + 25 - 1) // 25)]
    
    counter = 0
    for chunk in chunks:
        chunk = [{"PutRequest": {"Item": i}} for i in chunk]

        dynamodb = boto3.client('dynamodb')
        response = dynamodb.batch_write_item(
            RequestItems={tableName: chunk}
        )

        counter += 25
        if counter % 100 == 0:
            print(f'Items Loaded: {counter}')

if __name__ == "__main__":
    main()
