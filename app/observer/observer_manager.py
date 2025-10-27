import logging
logger = logging.getLogger(__name__)

class ReviewNotifier:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self, media, review, session):
        if not self.observers:
            logger.info(f"No observers for '{media.title}'.")
            return

        for ob in self.observers:
            try:
                ob.update(media, review, session)
            except Exception as e:
                logger.exception(f"Error in {ob.__class__.__name__}: {e}")