import boto3, time, json
from datetime import datetime

def handler(event, context):
    print("event")
    print(event)
    profileName = event['queryStringParameters']['uid']
    request = event['queryStringParameters']['request']
    
    calls = {
        'all': getAll(profileName),
        'profile': getProfile(profileName),
        'collections': getCollections(profileName),
        'recent': getRecent(profileName),
        'lastadd': getLastAdded(profileName),
        'friends': getFriends(profileName)
    }
    
    return {'isBase64Encoded': False,'statusCode': 200,'body': json.dumps(calls[request]), 'headers': {"Access-Control-Allow-Origin": "*"}}

def getData(profileName, request):
    dynamoDB = boto3.client('dynamodb')

    queries = {
        'profile': {
            'KeyConditionExpression': f'uid = :pN AND #t = :p',
            'ExpressionAttributeValues': {
                ':pN': {'S': f'{profileName}'},
                ':p': {'S': 'profile'}
            },
            'ExpressionAttributeNames': {
                '#t': 'type'
            },
            'TableName': 'collectors',
            'IndexName': 'type-index'
        },
        'collections': {
            'KeyConditionExpression': f'uid = :pN AND #t = :i',
            'ExpressionAttributeValues': {
                ':pN': {'S': f'{profileName}'},
                ':i': {'S': 'item'}
            },
            'ExpressionAttributeNames': {
                '#t': 'type'
            },
            'TableName': 'collectors',
            'IndexName': 'type-index'
        },
        'recent':{
            'KeyConditionExpression': 'uid = :pN',
            'ExpressionAttributeValues': {
                ':pN': {'S': f'{profileName}'}
            },
            'TableName': 'collectors',
            'IndexName': 'date-index'
        },
        'last': {
            'KeyConditionExpression': 'uid = :pN',
            'ExpressionAttributeValues': {
                ':pN': {'S': f'{profileName}'}
            },
            'TableName': 'collectors',
            'IndexName': 'date-index'
        },
        'friends': {
            'KeyConditionExpression': f'uid = :pN AND #t = :p',
            'ExpressionAttributeValues': {
                ':pN': {'S': f'{profileName}'},
                ':p': {'S': 'profile'}
            },
            'ExpressionAttributeNames': {
                '#t': 'type'
            },
            'ProjectionExpression': 'friends',
            'TableName': 'collectors',
            'IndexName': 'type-index'
        }
    }

    return dynamoDB.query(**queries[request])['Items']

def getProfile(profileName):
    profileData = {
        'picture': '',
        'fullName': '',
        'location': '',
        'icons': []
    }

    data = deserialize(getData(profileName, 'profile'))[0]

    profileData['picture'] = data['picture']
    profileData['fullName'] = data['full_name']
    profileData['location'] = data['location']
    profileData['icons'] = data['collections']

    return profileData

def getCollections(profileName):
    collectionsData = {
        'collections': {}
    }
    
    # Web frontend is expecting the above to be structured as:
    # 'collections': {
    #     'collection_id': {
    #         'icon': 'string',
    #         'items': [{},{},{}]
    #     }
    # }

    data = deserialize(getData(profileName, 'collections'))

    for i in data:
        if i['collection_id'] not in collectionsData['collections']:
            collectionsData['collections'][i['collection_id']] = {'icon': i['collection_id'].split('_')[1], 'items': []}
        collectionsData['collections'][i['collection_id']]['items'].append(i)
    
    return collectionsData

def getRecent(profileName):
    recentData = deserialize(getData(profileName, 'recent'))

    # Need to add icon key to each item in the recent activity return as it is expected by the front end. 
    for r in recentData:
        r['icon'] = r['collection'].split('_')[1]
    
    return recentData

def getLastAdded(profileName):
    lastData = {
        'lastAddition': {}
    }

    recent = deserialize(getData(profileName, 'recent'))

    activityToSort = []
    
    # Sort recent by date converted to Unix Epoch timestamp
    for i in recent:
        activityToSort.append(( convertToUnix(i['date']), i['itemname'] ))
    activityToSort.sort(key = lambda x: x[0], reverse=True)
    mostrecent = activityToSort[0][1]

    # Reference items in profile collections to match most recent activity to full item from collection.
    collections = getCollections(profileName)
    for value in collections.values():
        for v in value.values():
            for i in v['items']:
                if mostrecent in i['item_name']:
                    lastData['lastAddition'] = i

    return lastData

def getFriends(profileName):
    friendsData = {
        'friends': []
    }
    # Collect friend names for the current profile
    thisProfile = deserialize(getData(profileName, 'friends'))[0]

    # For each friend we need to collect information from their profile to satisfy the front end website display.
    fullFriends = []
    for f in thisProfile['friends']:
        profile = deserialize(getData(f, 'profile'))[0]
        if isinstance(profile['collections'], str):
            profile['collections'] = [profile['collections']]
        fullFriends.append({'uid': profile['uid'], 'fullName': profile['full_name'], 'icons': profile['collections'], 'picture':  profile['picture']})
    friendsData['friends'] = fullFriends

    return friendsData

def getAll(profileName):
    allData = {
        'picture': '',
        'fullName': '',
        'location': '',
        'icons': [],
        'collections': getCollections(profileName)['collections'],
        'recentActivity': getRecent(profileName),
        'lastAddition': getLastAdded(profileName)['lastAddition'],
        'friends': getFriends(profileName)['friends']
    }

    profileData = getProfile(profileName)
    allData['picture'] = profileData['picture']
    allData['fullName'] = profileData['fullName']
    allData['location'] = profileData['location']
    allData['icons'] = profileData['icons']

    return allData

def convertToUnix(date):
    return int(time.mktime(datetime.strptime(date, '%Y-%m-%d').timetuple()))

def deserialize(items):
    data = []

    for item in list(items):
        record = {}
        for k,v in item.items():
            for value in v.values():
                if isinstance(value, list):
                    record[k] = []
                    for li in value:
                        for s in li.values():
                            if '.' in value:
                                try:
                                    record[k].append(float(s))
                                except ValueError:
                                    record[k].append(s)
                            else:
                                try:
                                    record[k].append(int(s))
                                except ValueError:
                                    record[k].append(s)
                elif '.' in value:
                    try:
                        record[k] = float(value)
                    except ValueError:
                        record[k] = value
                else:
                    try:
                        record[k] = int(value)
                    except ValueError:
                        record[k] = value
        data.append(record)
    
    return data