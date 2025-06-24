"""
@author: chillcicada
@date: 2025-06-23

@description: calculate UUIDs based on usernames.
"""

import uuid


def preprocess_username(username: str) -> str:
    """
    Preprocess the username by removing leading and trailing whitespace.

    Args:
        username (str): The username to preprocess.

    Returns:
        str: The preprocessed username.
    """
    assert ' ' not in username, 'Username must not contain spaces.'

    return username.lower()


def calculate_genuine_uuid(username: str) -> uuid.UUID:
    """
    Calculate a UUID based on the provided username.

    Args:
        username (str): The username to base the UUID on.

    Returns:
        UUID: A UUID.
    """
    # TODO: fix the namespace to a valid one
    NAMESPACE_URL = uuid.UUID('00000000-0000-0000-0000-000000000000')

    # Generate a UUID based on the username
    return uuid.uuid3(NAMESPACE_URL, preprocess_username(username))


def calculate_offline_uuid(username: str) -> uuid.UUID:
    """
    Calculate an offline UUID based on the provided username.

    Args:
        username (str): The username to base the UUID on.

    Returns:
        UUID: A UUID.
    """
    NAMESPACE_DNS = uuid.UUID('00000000-0000-0000-0000-000000000000')

    return uuid.uuid3(NAMESPACE_DNS, 'OfflinePlayer:' + preprocess_username(username))
