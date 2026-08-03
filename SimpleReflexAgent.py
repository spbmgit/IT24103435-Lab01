
class SimpleReflexAgent:
    """Simple Reflex Agent using only current percepts."""

    def sense_and_act(self, percept):
        # IF food is here THEN collect it
        if percept['food_here']:
            return 'Suck'

        # IF wall is ahead THEN turn left
        elif percept['wall_ahead']:
            return 'Left'

        # ELSE move forward
        else:
            return 'Up'

