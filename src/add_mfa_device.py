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
    # print(response)
    return response

# def verify_mfa_code()
def lambda_handler(event, context):
    print(f"{event = }")
    body = json.loads(event['body'])
    username = body["username"]
    password = body["password"]
    try:
        authenticated = authenticate(username, password)
        print(f"authenticated response: {authenticated}")
        if authenticated["ChallengeName"] == "MFA_SETUP":
            mfa_response = client.associate_software_token(
                Session=authenticated["Session"]
            )
            print(f"{mfa_response = }")
            
            # verified_response = client.verify_software_token(
            #     Session=mfa_response["Session"],
            #     UserCode=mfa_code
            # )
            # print(f"{verified_response = }")
            
        response = {
            'SecretCode' : mfa_response['SecretCode'],
            'Session' : mfa_response['Session']
        }
        return{
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
            'body': json.dumps({
            'error': False,
            'code':'MFA_DEVICE_ADDED',
            'message': 'mfa device add successful.',
            'response': response
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
