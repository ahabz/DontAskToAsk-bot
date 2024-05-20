import aiosqlite
from loguru import logger
logger.add('../logs/main.log')

db_file = 'src/DontAskToAsk_bot/db/user_tracker.db'

async def user_check_add(author):

    async with aiosqlite.connect(db_file) as db:
        cursor = await db.cursor()

        # Check if the user already exists in the database
        await cursor.execute('SELECT id FROM users WHERE username = ?', (author,))
        existing_user = await cursor.fetchone()

        if existing_user:
           
            #Fetch the updated interaction count
            await cursor.execute('SELECT interaction_count FROM users WHERE username = ?', (author,))
            updated_interaction_count = await cursor.fetchone()
            if updated_interaction_count[0]>3:
                return updated_interaction_count[0]
            else:

                # If the user already exists, increment the interaction_count
                await cursor.execute('UPDATE users SET interaction_count = interaction_count + 1 WHERE username = ?', (author,))
                logger.info('Interaction count incremented for existing user.')
                await db.commit()


                return updated_interaction_count[0]  # Return the updated int
            
        else:
            # If the user doesn't exist, add them to the database
            await cursor.execute('''
            INSERT INTO users (username, interaction_count)
            VALUES (?, 1)
            ''', (author,))
            await db.commit()

            logger.info('New user added to the database.')
            return 0 # Return 'old' status for existing user




    


 
