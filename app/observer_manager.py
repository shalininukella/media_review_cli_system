class ReviewNotifier:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)
    
    def notify(self, media, review, session):
        for ob in self.observers:
            ob.update(media, review, session)