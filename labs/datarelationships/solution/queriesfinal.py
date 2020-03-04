import boto3, json

'''
Given ID return all attributes for store
Return all stores that do not observe daylight savings time return just state and store ID
Given a phone area code return all stores formatted addresses and phone numbers
Return all attributes for all stores with Starbucks and CVS 
Given state return all attributes for all stores
Given state and city return all attributes for all stores
Given state city and zip  return all attributes for all stores

reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.query
'''

def main():
    queries = {
        'ID': {
            'TableName': 'TargetStores',
            'IndexName': 'ID-index',
            'ExpressionAttributeNames': {'#I': 'ID'},
            'ExpressionAttributeValues': {':id': {'N': '1957'}},
            'KeyConditionExpression': '#I = :id'
        },
        'DaylightSavingsNo': {
            'TableName': 'TargetStores',
            'IndexName': 'IsDaylightSavingsTimeRecognized-index',
            'ExpressionAttributeNames': {'#DLS': 'IsDaylightSavingsTimeRecognized'},
            'ExpressionAttributeValues': {':dls': {'S': 'FALSE'}},
            'KeyConditionExpression': '#DLS = :dls'
        },
        'PhoneArea': {
            'TableName': 'TargetStores',
            'IndexName': 'Phone-index',
            'ExpressionAttributeNames': {'#LOC': 'X.locale', '#PHONE': 'PhoneNumber'},
            'ExpressionAttributeValues': {':locale': {'S': 'en-US'}, ':area': {'S': '(206)'}},
            'KeyConditionExpression': '#LOC = :locale AND begins_with(#PHONE, :area)'
        },
        'StarbucksCVS': {
            'TableName': 'TargetStores',
            'IndexName': 'Starbucks-CVS-index',
            'ExpressionAttributeNames': {'#STAR': 'Starbucks', '#CVS': 'CVS'},
            'ExpressionAttributeValues': {':star': {'S': '1'}, ':cvs': {'S': '1'}},
            'KeyConditionExpression': '#STAR = :star AND #CVS = :cvs'
        },
        'State': {
            'TableName': 'TargetStores',
            'ExpressionAttributeNames': {'#STATE': 'Address.Subdivision'},
            'ExpressionAttributeValues': {':state': {'S': 'WA'}},
            'KeyConditionExpression': '#STATE = :state'
        },
        'StateCity': {
            'TableName': 'TargetStores',
            'IndexName': 'City-Zip-index',
            'ExpressionAttributeNames': {'#STATE': 'Address.Subdivision', '#CITYZIP': 'CityZip'},
            'ExpressionAttributeValues': {':state': {'S': 'WA'}, ':city': {'S': 'Seattle'}},
            'KeyConditionExpression': '#STATE = :state AND begins_with(#CITYZIP, :city)'
        },
        'StateCityZip': {
            'TableName': 'TargetStores',
            'IndexName': 'City-Zip-index',
            'ExpressionAttributeNames': {'#STATE': 'Address.Subdivision', '#CITYZIP': 'CityZip'},
            'ExpressionAttributeValues': {':state': {'S': 'WA'}, ':cityzip': {'S': 'Seattle#98125'}},
            'KeyConditionExpression': '#STATE = :state AND begins_with(#CITYZIP, :cityzip)'
        }
    }

    for k, q in queries.items():
        attribPer = []
        print(f'\nRunning query {k}')
        items = query(q)
        #print(f'Returned Items:\n{items}')
        itemCount = len(items)
        for i in items:
            attribPer.append(len(i))
        avgAttribs = sum(attribPer) // itemCount
        print(f'Query {k} returned {itemCount} items with an average of {avgAttribs} attributes')

def query(params):
    dynamodb = boto3.client('dynamodb')
    return dynamodb.query(**params)['Items']

if __name__ == "__main__":
    main()