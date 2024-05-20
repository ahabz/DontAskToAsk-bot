import aiosqlite
from datetime import datetime, timedelta
from loguru import logger
logger.add('../logs/main.log')


async def init_database():
    db_file = 'src/DontAskToAsk_bot/db/user_tracker.db'

    async with aiosqlite.connect(db_file) as db:
        cursor = await db.cursor()

        await cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,        
            interaction_count INT DEFAULT 0
        )
        ''')

        await db.commit()
    logger.info('DataBase Initialization success!')


# Function to delete inactive users
async def old_users(days):
    async with aiosqlite.connect('src/DontAskToAsk_bot/db/user_tracker.db') as db:

        cursor = await db.cursor()

        # Calculate the timestamp X days ago
        cutoff_date = datetime.now() - timedelta(days=days)

        # Delete users who aren't considered "new" anymore
        await cursor.execute('''
        DELETE FROM users WHERE last_interaction < ?
        ''', (cutoff_date,))

        # Commit changes and close connection
        await db.commit()

 
