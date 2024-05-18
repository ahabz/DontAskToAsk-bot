from typing import Final
from discord import Intents, Client, Message, LoginFailure
from responses import get_response
from loguru import logger
from datetime import datetime, timezone
from config import Config

logger.add(
    "logs/main.log",
    format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message} | {extra}",
)


# LOAD OUR TOKEN FROM SOMEWHERE SAFE

TOKEN: Final[str] = Config.from_env().token


# BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)


# MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        logger.debug("Message was empty because intents were not enabled")
        return

    response: str = get_response(user_message, message.author.mention)
    if response != "":
        await message.channel.send(embed=response)
    else:
        return


# HANDLING THE STARTUP FOR OUR BOT
@client.event
async def on_ready() -> None:
    logger.success(f"{client.user} is now running!")


# HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:  # prevent bot from talking to itself
        return
    current_time = datetime.now(timezone.utc)  # Make the current time timezone-aware
    days_since_join = (
        current_time - message.author.joined_at.replace(tzinfo=timezone.utc)
    ).days
    threshold_days = 5  # threshold in days for bot interaction

    # Check if the message is from a new member
    if message.author.joined_at:
        current_time = datetime.now(
            timezone.utc
        )  # Make the current time timezone-aware
        days_since_join = (
            current_time - message.author.joined_at.replace(tzinfo=timezone.utc)
        ).days

        user_message: str = message.content
        if days_since_join < threshold_days:
            await send_message(message, user_message)

        else:
            logger.info("user is not new")
    else:
        return


# MAIN ENTRY POINT
def main() -> None:
    try:
        client.run(token=TOKEN)
    except LoginFailure:
        logger.critical("Failed to log-in using token")


if __name__ == "__main__":
    main()
