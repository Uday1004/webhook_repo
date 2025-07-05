from datetime import datetime

def get_current_utc_time():
    return datetime.utcnow()

def parse_event(event_type, data):
    """
    Parse GitHub webhook event based on its type.
    Supports: push, pull_request (opened, merged)
    """
    if event_type == "push":
        return {
            "event_type": "push",
            "author": data.get("pusher", {}).get("name", "Unknown"),
            "from_branch": None,
            "to_branch": data.get("ref", "").split("/")[-1],
            "timestamp": get_current_utc_time()
        }

    elif event_type == "pull_request":
        action = data.get("action")
        pr = data.get("pull_request", {})

        if action == "opened":
            return {
                "event_type": "pull_request",
                "author": pr.get("user", {}).get("login", "Unknown"),
                "from_branch": pr.get("head", {}).get("ref"),
                "to_branch": pr.get("base", {}).get("ref"),
                "timestamp": get_current_utc_time()
            }

        elif action == "closed" and pr.get("merged"):
            return {
                "event_type": "merge",
                "author": pr.get("user", {}).get("login", "Unknown"),
                "from_branch": pr.get("head", {}).get("ref"),
                "to_branch": pr.get("base", {}).get("ref"),
                "timestamp": get_current_utc_time()
            }

    return None
