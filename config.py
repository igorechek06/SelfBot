from os import environ

session_name = environ["sessionName"]
api_id = environ["apiId"]
api_hash = environ["apiHash"]


__all__ = [
    "session_name",
    "api_id",
    "api_hash",
]
