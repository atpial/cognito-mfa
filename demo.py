def lambda_handler(event):
    print(f"{event = }")
    email = event["request"]["userAttributes"]["email"]
    allowed_domains = ["shadhinlab.com", "gmail.com"]  # allowed domains list

    if any(email.endswith(domain) for domain in allowed_domains):
        # event['response']['autoConfirmUser'] = True
        return event
    else:
        raise Exception("Invalid email domain")


event = {
    "version": "1",
    "region": "us-east-2",
    "userPoolId": "us-east-2_rMuvjZkSY",
    "userName": "d18b55c0-20b1-7008-87cc-170ceac0c239",
    "callerContext": {
        "awsSdkVersion": "aws-sdk-unknown-unknown",
        "clientId": "3pi4uhrgtbo8qmeo3nukea6uk4",
    },
    "triggerSource": "PreSignUp_SignUp",
    "request": {
        "userAttributes": {"email": "xawis42729@trazeco.com"},
        "validationData": None,
    },
    "response": {
        "autoConfirmUser": False,
        "autoVerifyEmail": False,
        "autoVerifyPhone": False,
    },
}

lambda_handler(event)
