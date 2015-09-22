def get_token_from_file(path):
    """
    :param path: string, path to a file containing the token
    :return: string, the token
    """

    # Read in the file containing the authorization token.
    f = open(path)
    token = f.read()

    # Get rid of leading and trailing whitespace.
    token = token.strip()
    f.close()

    return token

# ToDo maintain a sqlite db of users and tokens
# ToDo function to create new token
# ToDo function to store tokens under users