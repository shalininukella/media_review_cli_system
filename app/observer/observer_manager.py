class ReviewNotifier:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)
    
    def detach(self, observer):
        """Detach an observer from the notifier."""
        self.observers.remove(observer)
    
    def notify(self, media, review, session):
        for ob in self.observers:
            ob.update(media, review, session)