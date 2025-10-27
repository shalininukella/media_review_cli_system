import logging
from app.cli.commands.concurrency import concurrent_reviews_command
logger = logging.getLogger(__name__)

def handle(args):
    if args.concurrent:
        concurrent_reviews_command(args.concurrent)