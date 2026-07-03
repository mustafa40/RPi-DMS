class FatigueScore:
    def __init__(self):
        self.score = 0

    def update(self, driver_state, perclos):
        score = 0

        if perclos > 15:
            score += 20
        if perclos > 30:
            score += 30
        if perclos > 45:
            score += 40

        if driver_state == "EYES_CLOSED":
            score += 35
        elif driver_state == "DASHBOARD":
            score += 5
        elif driver_state == "NO_FACE":
            score += 10

        self.score = min(score, 100)
        return self.score
