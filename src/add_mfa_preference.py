import os
import json
import boto3

client = boto3.client('cognito-idp')

def set_mfa_preference(username,mfa):
    response = client.admin_set_user_mfa_preference(
        UserPoolId=os.environ.get("COGNITO_USERPOOL_ID"),
        Username=username,
        # SMSMfaSettings={
        #     'Enabled': True|False,
        #     'PreferredMfa': True|False
        # },
        SoftwareTokenMfaSettings={
            'Enabled': mfa,
            'PreferredMfa': mfa
        },
    )
    return response

def get_user_attributes(username):
    response = client.admin_get_user(
    UserPoolId=os.environ.get("COGNITO_USERPOOL_ID"),
    Username=username
    )
    return response

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    username = body["username"]
    mfa = body["mfa"]
    try:
        user_attribute_before = get_user_attributes(username)
        print(f"{user_attribute_before = }")

        mfa_preference = set_mfa_preference(username, mfa)
        print(f"{mfa_preference = }")
        
        user_attribute_after = get_user_attributes(username)
        print(f"{user_attribute_after = }")

        token = {
            # 'access_token' : authenticated['AuthenticationResult']['AccessToken'],
            # 'refresh_token' : authenticated['AuthenticationResult']['RefreshToken'],
            # 'id_token': authenticated['AuthenticationResult']['IdToken']
        }
        return{
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
            'body': json.dumps({
            'error': False,
            'code':'LOG_IN_SUCCESSFUL',
            'message': 'log in successful.',
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