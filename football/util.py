
def winner(home, away):
    if home is not None and away is not None:
        if home > away:
            return True
        elif home < away:
            return False
        else:
            return "Draw"
    else:
        return None
