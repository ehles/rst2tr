

class Step:
    index = -1  # some invalid value for checking
    description = ''
    expected = ''


class Case:
    id = ''
    description = ''
    complexity = ''
    steps = []

    def __init__(self, description, complexity, steps=[]):
        self.description = description
        self.complexity = complexity
        if steps:
            self.steps = steps

    def add_step(self, description, expected):
        step = Step(description, expected)
        step.index = len(self.steps)
        self.steps.append(step)