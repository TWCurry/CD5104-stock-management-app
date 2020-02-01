import json, boto3, os

def lambda_handler(event, context):
    #Fetch params
    try:
        action = event["queryStringParameters"]["action"]
        data = event["queryStringParameters"]["data"] #data for updates
    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin" : "*"},
            "body": "Missing parameter - " + str(e)
        }
    
    #Establish connection to DynamoDB
    client = boto3.client("dynamodb")
    #Perform actions
    print("Action performed: \""+action+"\"")
    if action == "add":
        return writeToDb(client, data)
    elif action == "remove":
        return removeFromDb(client, data)
    elif action == "setstocklevel":
        return setStockLevel(client, data)
    elif action == "getdata":
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin" : "*"},
            "body": json.dumps(fetchItems(client))
        }
    else:
        logError("Invalid action: " + str(action))
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin" : "*"},
            "body": "Invalid action: " + str(action)
        }

def writeToDb(client, data):
    data = json.loads(data)
    #Check correct params
    try:
        name = data["name"]
        price = data["price"]
        numberInStock = data["numberinstock"]
        productType = data["producttype"]
        manufacturer = data["manufacturer"]
    except Exception as e:
        logError("Invalid data for write. Full error - " + str(e))
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin" : "*"},
            "body": "Invalid data for write. Full error - " + str(e)
        }
    response = client.put_item(
        TableName=os.environ["ddbTableName"],
        Item={
            "productName": {
                "S": name
            },
            "price": {
                "S": price
            },
            "numberInStock": {
                "S": numberInStock
            },
            "productType": {
                "S": productType
            },
            "manufacturer": {
                "S": manufacturer
            }
        }
    )
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin" : "*"},
        "body": "update successful"
    }

def removeFromDb(client, data):
    data = json.loads(data)
    try:
        name = data["name"]
    except Exception as e:
        logError("Invalid data for delete. Full error - " + str(e))
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin" : "*"},
            "body": "Invalid data for delete. Full error - " + str(e)
        }
    response = client.delete_item(
        TableName=os.environ["ddbTableName"],
        Key={
            "productName": {
                "S": name
            }
        }
    )
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin" : "*"},
        "body": "delete successful"
    }

def setStockLevel(client, data):
    #Get params
    try:
        data = json.loads(data)
        name = data["name"]
        number = data["number"]
    except Exception as e:
        logError("Invalid data to update stock level. Full error - " + str(e))
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin" : "*"},
            "body": "Invalid data to update stock level. Full error - " + str(e)
        }
    response = client.get_item(
        TableName=os.environ["ddbTableName"],
        Key={
            "productName": {
                "S": name
            }
        }
    )
    item = response["Item"]
    item["numberInStock"]["S"] = str(number)
    response = client.put_item(
        TableName=os.environ["ddbTableName"],
        Item=item
    )
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin" : "*"},
        "body": "update successful"
    }

def fetchItems(client):
    response = client.scan(
        TableName=os.environ["ddbTableName"],
    )
    rawData = response["Items"]
    returnData = []
    for item in rawData:
        returnItem = {}
        returnItem["name"] = item["productName"]["S"]
        returnItem["price"] = item["price"]["S"]
        returnItem["number"] = item["numberInStock"]["S"]
        returnItem["type"] = item["productType"]["S"]
        returnItem["manufacturer"] = item["manufacturer"]["S"]
        returnData.append(returnItem)
    return returnData

def logError(message):
    print("ERROR: " + str(message))