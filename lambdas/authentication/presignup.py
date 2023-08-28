
def lambda_handler(event, context):
    print(f"{event = }")
    email = event['request']['userAttributes']['email']
    allowed_domains = ['shadhinlab.com', 'gmail.com']  # allowed domains list

    if any(email.endswith(domain) for domain in allowed_domains):
        # event['response']['autoConfirmUser'] = True
        return event
    else:
        raise Exception("::PRESIGNUP::Invalid email domain")
