import boto3

def handler(event, context):
    # event contains the records    
    # Get current relevent metadata objects
    # Determine if the 0 version (latest) needs to be updated if yes determine what the current version number in sequence is
    # Write new 0 and 1 versions of first commit for file OR update 0 version and newest version

    # Collect timestamp, and put item
    record = event['Records'][0]
    timeStamp = int(record['dynamodb']['ApproximateCreationDateTime'])
    item = record['dynamodb']['NewImage']
    
    if "ID" in item.keys():    
        ddb = boto3.client('dynamodb')
        
        # Collect any existing metadata 
        currentMeta = ddb.query(
            TableName = 'PrometheusMeta',
            ExpressionAttributeNames = {'#PART': 'Partition'},
            ExpressionAttributeValues = {':part': {'S': f'meta_{item["Partition"]["S"]}'}},
            KeyConditionExpression = '#PART = :part'
        )['Items']

        # Determin if 0 needs updating
        updateZed = False
        if len(currentMeta) == 0:
            version = 1
        else:
            versions = []
            for i in currentMeta:
                versions.append(int(i['Sort']['S']))
            versions.sort(reverse = True)
            version = versions[0] + 1
            updateZed = True

        # Initialize metadata record
        metaItem = {
            'Partition': {'S': f'meta_{item["Partition"]["S"]}'},
            'Sort': {'S': str(version)},
            'CommitId': {'S': item['ID']['S']},
            'CommitParent': {'S': item['Parent']['S']},
            'Timestamp': {'N': str(timeStamp)}
        }

        # If zero record requires updating, put new record, and update 0
        if updateZed:
            response = ddb.put_item(
                TableName = 'PrometheusMeta',
                Item = metaItem
            )
            print(response)
            response = ddb.update_item(
                TableName = 'PrometheusMeta',
                Key = {
                    'Partition': {'S': f'meta_{item["Partition"]["S"]}'},
                    'Sort': {'S': '0'}
                },
                ExpressionAttributeNames = {'#ID': 'CommitId', '#PARENT': 'CommitParent', '#TS': 'Timestamp'},
                ExpressionAttributeValues = {':id': {'S': metaItem['CommitId']['S']}, ':par': {'S': metaItem['CommitParent']['S']}, ':ts': {'N': metaItem['Timestamp']['N']}},
                UpdateExpression = 'SET #ID = :id, #PARENT = :par, #TS = :ts'
            )
            print(response)
        # Otherwise put new record, and first 0 record
        else:
            response = ddb.put_item(
                TableName = 'PrometheusMeta',
                Item = metaItem
            )
            print(response)
            metaItem['Sort']['S'] = '0'
            response = ddb.put_item(
                TableName = 'PrometheusMeta',
                Item = metaItem
            )
            print(response)