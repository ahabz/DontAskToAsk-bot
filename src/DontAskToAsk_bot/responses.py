import re
from discord import Embed, Colour
from classification import Long_Q_segment, segment_posts
from loguru import logger

logger.add(
    "logs/main.log",
    format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message} | {extra}",
)


def get_response(user_input: str, author) -> str:
    # pattern to catch questions
    regex_pattern = r"(?i)^(?!.*\b(?:ideas|know if|details|opinion|understand|can i get|share|idea|suggestions|suggestion|recommendation|recommendations|who|what|where|when|why|how)\b)(?=(?:\b\w+\b\s+){2,}).*\b(?:question|is it|any|where|anyone|is there|questions|ask|problems|does|problem|trying|familiar|can i|help|assist|guide|solve|troubleshoot|error|issue|problem|bug|fix|who|which|here|any|anyone|one|any body|anybody)\b.*$"

    try:
        question: str = user_input
    except NameError:
        logger.error("No user input, question is empty")
        return ""
    match: bool = re.search(regex_pattern, question)

    if match:  # if the question matches the initial regex gate (it is ia question)
        decision = Long_Q_segment(segment_posts(question, ave_len=5))

        if decision == "PERMISSION":
            embed = Embed(
                colour=Colour.dark_teal(),
                description=f""" * hey {author}, here is Some Examples of Good Vs. Bad Questions:*
            ```Anyone here good at JAVA? ❌
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
            return embed

        else:
            return ""
    else:
        return ""