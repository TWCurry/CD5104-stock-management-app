import json, boto3, os

def lambda_handler(event, context):
    #Fetch params
    try:
        action = event["queryStringParameters"]["action"]
        data = event["queryStringParameters"]["data"] #data for updates
    except Exception as e:
        return {
            "statusCode": 400,
            "body": "Missing parameter - " + str(e)
        }
    
    #Establish connection to DynamoDB
    client = boto3.client("dynamodb")

    #Perform actions
    if action == "add":
        return writeToDb(client, data)
    elif action == "remove":
        return removeFromDb(client, data)
    elif action == "setstocklevel":
        return setStockLevel(client, data)
    else:
        logError("Invalid action: " + str(action))
        return {
            "statusCode": 400,
            "body": "Invalid action: " + str(action)
        }

def writeToDb(client, data):
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
        "body": "update successful"
    }

def removeFromDb(client, data):
    try:
        name = data["name"]
    except Exception as e:
        logError("Invalid data for delete. Full error - " + str(e))
        return {
            "statusCode": 400,
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
        "body": "delete successful"
    }

def setStockLevel(client, data):
    #Get params
    try:
        name = data["name"]
        number = data["number"]
    except Exception as e:
        logError("Invalid data for delete. Full error - " + str(e))
        return {
            "statusCode": 400,
            "body": "Invalid data for delete. Full error - " + str(e)
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

def logError(message):
    print("ERROR: " + str(message))