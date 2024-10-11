class RandomAgent:
    def __init__(self):
        pass

    def move(self, action_space):
        action = action_space.sample()
        return action


class SimpleAgent:
    def __init__(self) -> None:
        pass

    def move(self, observation, action_space):
        ...
