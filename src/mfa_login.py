import os
import json
import boto3

client = boto3.client("cognito-idp")


# def authenticate(username, password):
#     response = client.initiate_auth(
#         ClientId=os.environ.get("COGNITO_USER_CLIENT_ID"),
#         AuthFlow="USER_PASSWORD_AUTH",
#         AuthParameters={"USERNAME": username, "PASSWORD": password},
#     )
#     # print(response)
#     return response


def get_user_attributes(username):
    response = client.admin_get_user(
    UserPoolId=os.environ.get("COGNITO_USERPOOL_ID"),
    Username=username
    )
    return response

def lambda_handler(event, context):
    print(f"{event = }")
    body = json.loads(event["body"])
    session = body["session"]
    mfa_code = body["mfa_code"]
    username = body["username"]
    # password = body["password"]

    try:
        # authenticated = authenticate(username, password)
        # print(f"authenticated response: {authenticated}")

        user_attributes = get_user_attributes(username)
        print(f"{user_attributes = }")

        # if authenticated["ChallengeName"] == "SOFTWARE_TOKEN_MFA":
        mfa_response = client.respond_to_auth_challenge(
            ChallengeName="SOFTWARE_TOKEN_MFA",
            ClientId=os.environ.get("COGNITO_USER_CLIENT_ID"),
            Session=session,
            ChallengeResponses={
                "USERNAME": username,
                "SOFTWARE_TOKEN_MFA_CODE": mfa_code,
            },
        )
        print(f"{mfa_response = }")

        # print(f"{verified_response = }")

        response = {
            'AccessToken' : mfa_response['AuthenticationResult']['AccessToken'],
            'RefreshToken' : mfa_response['AuthenticationResult']['RefreshToken'],
            'IdToken' : mfa_response['AuthenticationResult']['IdToken'],
        }
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json",
            },
            "body": json.dumps(
                {
                    "error": False,
                    "code": "LOGIN_SUCCESSFULL",
                    "message": "login is successful.",
                    "token": response,
                }
            ),
        }
    except client.exceptions.UserNotConfirmedException as e:
        print(e)
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "error": True,
                    "code": "USER_NOT_CONFIRMED",
                    "message": "User not confirmed yet. Please check email for confirmation code",
                }
            ),
        }
    except client.exceptions.UserNotFoundException as e:
        print(e)
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "error": True,
                    "code": "USER_NOT_FOUND",
                    "message": "User could not be found.Please Sign up first.",
                }
            ),
        }
    except client.exceptions.NotAuthorizedException as e:
        print(e)
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "error": True,
                    "code": "USER_NOT_AUTHORIZED",
                    "message": "Username or password is incorrect.Please try again.",
                }
            ),
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "error": True,
                    "code": "UNKNOWN_ERROR",
                    "message": "Some error occured. Please try again.",
                }
            ),
        }
