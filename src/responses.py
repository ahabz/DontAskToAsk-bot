import re
import discord 
from classification import Long_Q_segment, segment_posts

 
def get_response(user_input: str, roles)->str:
    #pattern to catch questions
    regex_pattern = r'(?i)^(?!.*\b(?:ideas|can i get|idea|suggestions|suggestion|recommendation|recommendations|who|what|where|when|why|how)\b)(?=(?:\b\w+\b\s+){4,}).*\b(?:question|any|where|anyone|is there|questions|ask|problems|does|problem|trying|familiar|can i|help|assist|guide|solve|troubleshoot|error|issue|problem|bug|fix|who|which|here|Any|anyone|one|any body|anybody)\b.*$'

    question:str=user_input
    match:bool=re.search(regex_pattern,question)
    question_mark=re.search(r'[\?]',user_input)
 
     

    if match or question_mark : #if the question matches the initial regex gate (it is ia question)
        decision= Long_Q_segment(segment_posts(question, ave_len=12))

        if decision == 'PERMISSION':
            embed = discord.Embed(
            colour=discord.Colour.dark_teal(), 
            description= """*Some Examples of Good Vs. Bad Questions:*
            ```Anyone here good at JAVA? ❌
Can i ask about X here? ❌ 
Anyone familiar with Y? ❌
How can i do X using Y? ✅
```""", 
            title="😊 DONT ASK TO ASK, JUST ASK 😊"
        )
        
            embed.set_author(name="JustAskBot", url="https://github.com/ahabz/DontAskToAsk-bot")

            embed.set_image(url="https://dontasktoask.com/favicon.png")
                
            embed.add_field(name="How To Ask questions:", value="https://stackoverflow.com/help/how-to-ask",inline=False)
            embed.add_field(name="Inspired by: ",value="https://github.com/maunium/dontasktoask.com",inline=False)


            return embed
        
        else:
            return ""




    else:
      
        return ''
    

    

     




 
