class Observer:
    #Base class for all observers.

    def update(self, media, review, session):
        """Handle an update event when a review is added."""
        raise NotImplementedError("Subclasses must implement update()")
