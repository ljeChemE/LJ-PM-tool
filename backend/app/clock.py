from datetime import date


def today() -> date:
    """FastAPI dependency for "what day is it". Real system date in
    production; overridden in tests (`app.dependency_overrides[today] = ...`)
    so rollover behavior can be tested without waiting for real days to pass.
    """
    return date.today()
