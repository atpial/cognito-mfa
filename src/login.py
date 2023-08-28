import os
import json
import boto3

client = boto3.client('cognito-idp')

def authenticate(username, password):
    response = client.initiate_auth(
        ClientId=os.environ.get('COGNITO_USER_CLIENT_ID'),
        AuthFlow = 'USER_PASSWORD_AUTH',
        AuthParameters={
        'USERNAME': username,
        'PASSWORD': password
         }
    )

    return response

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    username = body["username"]
    password = body["password"]
    try:
        authenticated = authenticate(username, password)
        print(f"auth response = {authenticated}")
        if "ChallengeName" in authenticated and authenticated["ChallengeName"] == "SOFTWARE_TOKEN_MFA":
            print("User has mfa enabled. Must provide mfa code")
            token = {
            'ChallengeName' : authenticated['ChallengeName'],
            'Session' : authenticated['Session'],
            }
            code = "MFA_REQUIRED"
            message = "mfa code is required to finish login process"
        else:
            token = {
                'access_token' : authenticated['AuthenticationResult']['AccessToken'],
                'refresh_token' : authenticated['AuthenticationResult']['RefreshToken'],
                'id_token': authenticated['AuthenticationResult']['IdToken']
            }
            code = "LOG_IN_SUCCESSFUL"
            message = "log in successful."
        return{
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
            'body': json.dumps({
            'error': False,
            'code':code,
            'message': message,
            'token': token
            })
        }
    except client.exceptions.UserNotConfirmedException as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps({
            'error': True,
            'code': 'USER_NOT_CONFIRMED',  
            'message': 'User not confirmed yet. Please check email for confirmation code'
            })
    }
    except client.exceptions.UserNotFoundException as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps({
            'error': True,
            'code': 'USER_NOT_FOUND',
            'message': 'User could not be found.Please Sign up first.'
            })
        }
    except client.exceptions.NotAuthorizedException as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps({
            'error': True,
            'code': 'USER_NOT_AUTHORIZED',
            'message': 'Username or password is incorrect.Please try again.'
            })
        }
    except Exception as e:
        print(e)
        return{
            'statusCode': 400,
            'body': json.dumps({
            'error': True,
            'code': 'UNKNOWN_ERROR',
            'message': 'Some error occured. Please try again.'
            })
        }