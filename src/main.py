from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
import warnings
warnings.filterwarnings("ignore")
from datetime import datetime, timedelta, timezone


# LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)


# MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled)')
        return


    try:
        response: str = get_response(user_message, message.author.roles)
        print(response, "ayoo wot?")
        if response=='':
            pass
        else:
            await message.channel.send(embed=response)
    except Exception as e:
        print(e)


# HANDLING THE STARTUP FOR OUR BOT
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')


# HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    current_time = datetime.now(timezone.utc)  # Make the current time timezone-aware
    days_since_join = (current_time - message.author.joined_at.replace(tzinfo=timezone.utc)).days


     # Check if the message is from a new member
    if message.author.joined_at:
        print(days_since_join)

        current_time = datetime.now(timezone.utc)  # Make the current time timezone-aware
        days_since_join = (current_time - message.author.joined_at.replace(tzinfo=timezone.utc)).days
        threshold_days = 9992  # Adjust this threshold as needed

        username: str = str(message.author)
        user_message: str = message.content
        channel: str = str(message.channel)
        role:list = [role.name for role in message.author.roles] # GET THE ROLE OF USER
        if days_since_join < threshold_days:
            await send_message(message, user_message)


            print(f'[{channel}],[{role}],[{username}]: "{user_message}"','<=== THIS GUY NEW')
        else: 
            print('oh, he is NOT new..')
    else:
        return 




# MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()