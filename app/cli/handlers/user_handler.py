import logging
from app.cli.commands.user_commands import add_user, list_users

logger = logging.getLogger(__name__)

def handle(args):
    if args.add_user:
        result = add_user(args.add_user)
        logger.info(result["message"])

    elif args.list_users:
        result = list_users()
        if not result.get("success"):
            logger.info(result.get("message", "Something went wrong."))
        else:
            users = result["data"]
            if not users:
                logger.info("No users found.")
            else:
                for u in users:
                    logger.info(f"  - [{u['id']}] {u['name']}")