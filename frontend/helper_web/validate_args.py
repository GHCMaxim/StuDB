def validate_args(message_body, required_args) -> tuple[bool, dict, tuple[str]]:
    """
    Validate the arguments passed in the message body.

    :param message_body: The message body to validate.
    :param required_args: The required arguments.
    :return:
        - True if all required arguments are present in the message body.
        - The message body.
        - A tuple of missing arguments.
    """
    if message_body is None:
        return False, {}, tuple()
    missing_args = [arg for arg in required_args if arg not in message_body]
    if len(missing_args) > 0:
        return False, {}, tuple(missing_args)
    return True, message_body, tuple()
