from helpers.authorizeDeviceHelper import auth

def validation(USERNAME: str, PASSWORD: str, IP_CLIENT: str, LIST_CONTENTS:list):
    LIST_CONTENTS.append("Incorrect username/password")
    # If user is valid auth device for the connect
    auth(IP_CLIENT)
    return False