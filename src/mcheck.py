import validate_email_address
import dns.resolver

def check_email_exists(email):
    result = ""
    try:
        # Validate email format
        is_valid_format = validate_email_address.validate_email(email, verify=False)
        if not is_valid_format:
            result = f'The email address {email} is not in a valid format.'
            return result
        # Check MX records for the domain
        domain = email.split('@')[1]
        mx_records = dns.resolver.resolve(domain, 'MX')
        if mx_records:
            result = f'The email address {email} is valid.'
        else:
            return f'The email address {email} is not valid. No MX records found for the domain.'
    except Exception as e:
        result = f'An error occurred: {e}'
        return result
    return result
