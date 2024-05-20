import re
from discord import Embed, Colour
from classification import Long_Q_segment, segment_posts
from loguru import logger
from db.users_db import user_check_add

logger.add(
    "logs/main.log",
    format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message} | {extra}",
)




async def get_response(user_input: str, author) -> str:
    # pattern to catch questions
    regex_pattern = r"(?i)^(?!.*\b(?:ideas|know if|details|opinion|understand|can i get|share|idea|suggestions|suggestion|recommendation|recommendations|who|what|where|when|why|how)\b)(?=(?:\b\w+\b\s+){2,}).*\b(?:question|is it|any|where|anyone|is there|questions|ask|problems|does|problem|trying|familiar|can i|help|assist|guide|solve|troubleshoot|error|issue|problem|bug|fix|who|which|here|any|anyone|one|any body|anybody)\b.*$"

    try:
        question: str = user_input
    except NameError:
        logger.error("No user input, question is empty")
        await  ""
    match: bool = re.search(regex_pattern, question)

    if match:  # if the question matches the initial regex gate (it is ia question)
        decision = Long_Q_segment(segment_posts(question, ave_len=5))

        if decision == "PERMISSION":
            user_status =await user_check_add(author)
            if user_status in range(1,2):
                embed = Embed(
                    colour=Colour.red(),
                    description=f"""Hey {author}, it looks like you asked a permission question again. Please read my previous instructions before posting again.""",
                    title="😤 Please Follow The instructions 😤",
                )

                embed.set_author(
                    name="JustAskBot", url="https://github.com/ahabz/DontAskToAsk-bot"
                )
                embed.add_field(
                    name="How To Ask questions:",
                    value="https://stackoverflow.com/help/how-to-ask",
                    inline=False,
                )
                
                logger.info('embed created')
                return   embed
            
            elif user_status in range(0,2) :

                embed = Embed(
                    colour=Colour.dark_teal(),
                    description=f"""*Hey {author}, here is Some Examples of Good Vs. Bad Questions:*
                    ```
Anyone here good at JAVA? ❌
Can i ask about X here? ❌ 
Anyone familiar with Y? ❌
How can i do X using Y? ✅
```""",
                    title="😊 DONT ASK TO ASK, JUST ASK 😊",
                )

                embed.set_author(
                    name="JustAskBot", url="https://github.com/ahabz/DontAskToAsk-bot"
                )
                embed.set_image(url="https://dontasktoask.com/favicon.png")
                embed.add_field(
                    name="How To Ask questions:",
                    value="https://stackoverflow.com/help/how-to-ask",
                    inline=False,
                )
                embed.add_field(
                    name="Inspired by: ",
                    value="https://github.com/maunium/dontasktoask.com",
                    inline=False,
                )
                logger.info('embed created')
                return   embed
            

            else: 
                 return   ""

 

        else:
            return  ''
    else:
        return   ""
