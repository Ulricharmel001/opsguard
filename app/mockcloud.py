import copy

INITIAL_STATE = {
    "staging": {
        "servers": ["web-1", "web-2"],
        "databases": ["staging-db"],
        "services": {"payments": "running", "search": "running"},
    },
    "production": {
        "servers": ["prod-web-1", "prod-web-2", "prod-web-3"],
        "databases": ["prod-db"],
        "services": {"payments": "running", "search": "running"},
    },
}

state = copy.deepcopy(INITIAL_STATE)


def reset() -> None:
    global state
    state = copy.deepcopy(INITIAL_STATE)


def list_servers(environment: str) -> list:
    return state[environment]["servers"]


def delete_database(environment: str, name: str) -> str:
    state[environment]["databases"].remove(name)
    return f"Deleted database {name} in {environment}"
