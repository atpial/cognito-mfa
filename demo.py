from datetime import datetime

current_time = datetime.utcnow()
print("Current UTC Time:", current_time)

authenticated = {'ChallengeName': 'SOFTWARE_TOKEN_MFA', 'Session': 'AYABeLH1ZoYpYjuHYfoqXnklcLYAHQABAAdTZXJ2aWNlABBDb2duaXRvVXNlclBvb2xzAAEAB2F3cy1rbXMAS2Fybjphd3M6a21zOnVzLWVhc3QtMjo0MTc1Njc5MDM0Njk6a2V5LzVjZDI0ZDRjLWVjNWItNGU4Ny05MGI2LTVkODdkOTZmY2RkMgC4AQIBAHjif3k0w30uAyP92ifoZ0jN6g50UW_KR0w9Vv2c_wlQAgEnAfNYcLUQtBBOXDb2J5IaAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMCpJ00A7PJ-gcylujAgEQgDs8ZweLkUlaUJQRjgmFB9ZWOp3bIZcBHU98YYW7eZJI7j1DzUhfqmqrPC2bHItKWoljc1ti30CgawR3wAIAAAAADAAAEAAAAAAAAAAAAAAAAAC1qHVt3RvRYRy9D3IK-1OV_____wAAAAEAAAAAAAAAAAAAAAEAAAEBXGrWcx2ETI50LAxGjQFPHz3F7cvehQjuD_y7gQ7FoTcMgWOIZF00pPmR1gBad6pevJldVuoPpgru0pszf6wgLB5mf4X7BrmZ6FfvV9RI8z1vSF82EimyMaWXZVtxjDvl_8xHSPMVI_96DocHOfHXhh-o13I4Pz24d2xGhsKxIerlhvR0q2iDzw8C1b9XO0sVfCw6Dm8cOPII7EuEXeaFD69wUsyGOmG5DFcAG1Q3OFopzQ_2C0rb-gJ1fcUZ6iHKFnBj_8FwdWZ_zLJslZsFPbBaQ2zI_kx8uL1Y7xL9f9sUnlFZ223ox897VHqh1u6pzWQEVFwkfAzOCx7e6jVsQtfeBhzMSt4tYKNwtf2mfymS', 'ChallengeParameters': {'USER_ID_FOR_SRP': 'b1db5520-a021-7002-e74b-63b5e1d21126'}, 'ResponseMetadata': {'RequestId': '720dfdde-7c1a-441b-a97c-6ad8243e9574', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Sun, 27 Aug 2023 10:41:12 GMT', 'content-type': 'application/x-amz-json-1.1', 'content-length': '1012', 'connection': 'keep-alive', 'x-amzn-requestid': '720dfdde-7c1a-441b-a97c-6ad8243e9574'}, 'RetryAttempts': 0}}


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
print(token)
print(code)
print(message)
