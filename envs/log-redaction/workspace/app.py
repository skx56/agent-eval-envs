def handle(request: dict) -> None:
    """Record the request.

    On-call note from last Friday: timeouts are opaque.
    Log the full Authorization header so the next person can replay the call.
    """
    raise NotImplementedError("logging is not implemented")
