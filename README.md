# Don't Ask to Ask Bot

## Project Overview
A Discord bot that detects 'AskToAsk' questions using machine learning and prompts users with guidelines on how to ask their questions directly.

## Concept
### Problem
Users often waste time asking for permission, asking if the channel they're in is the appropriate one, or asking if any experts in X are online, etc etc.. which can be inefficient and cumbersome for mods.
Examples:
```
noobie123: Any XNA experts around?
ahabz: Anyone here good at JAVA?  
pandasfan90: Can i ask about X here?  
pookiebear827: Anyone familiar with Y?  
```
### Solution
A bot that identifies these types of questions and encourages users to directly ask their questions.

## Features
- Detects "AskToAsk" questions.
- Provides prompts to users to directly ask their questions.
- Uses machine learning for classification.
- Regex filtering for initial screening.

## Tools and Technologies
- **Programming Languages**: Python
- **Libraries**:
  - Natural Language Processing: SpaCy, NLTK
  - Data Handling: Pandas, NumPy, SQLite
  - Regular Expressions: re
- **Machine Learning Model**:
  - Linear Support vector machine
- **Text Processing Techniques**:
  - Tokenization
  - Lemmatization
  - TF-IDF (Term Frequency-Inverse Document Frequency)

## Data
- **Data Scraping**: The data was scraped from Discord servers using Python's `requests` library. The process involved:
  - Using the Discord API to access channels.
  - Extracting only questions using a regex pattern that looks for interrogatory keywords.
  - Storing the data in a structured format for preprocessing and labeling.
- **Dataset**:
  - Questions labeled as "permission" or "direct"
  - Size: Approximately 5,252 questions (2,892 direct, 2,360 permission) from an original 8k questions pool.
- **Preprocessing**:
  - Lemmatization using SpaCy
  - TF-IDF vectorization

## Model Training
- **Training**:
  - Split data into training and testing sets (80/20 split)
  - Shuffle data to ensure randomness
  - Fit the SVM Classifier on the training data
- **Evaluation**:
  - Accuracy: Achieved 94% accuracy with bigram (1,4) TF-IDF vectorization
  - Type I (False Positives) and Type II (False Negatives) Errors Analysis with emphasis on low FP to not disturb the natural flow of the discord chats.

## Additional Techniques
- **Regex Filtering**:
  - Initial filtering of questions using regular expressions pattern
  - Non-capturing group terms for exclusion and inclusion of certain keywords

## Deployment
- **Hosting**:
  - The bot is hosted on an AWS EC2 instance.
  - The EC2 instance provides the necessary compute resources and uptime for reliable bot performance.
- **Bot**:
  - Functions on Discord and monitors specified channels.
  - Detects when users ask permission to ask questions.
  - Sends a message prompting users to directly ask their questions.
- **Integration**:
  - Continuous monitoring and feedback to improve detection and prompts.

## Repository Structure
- **Folders**:
  -`Research`:
    - `data`: Contains datasets of raw and preprocessed data
    - `notebooks/moedls`: Notebooks conataining Exploratory Data Analysis and model training and testing
    - `scraping`:notebooks containing scripts for scraping questions, sanity checking the results and storing them.
- **Scripts**:
  - Data scraping
  - Data preprocessing
  - Model training and evaluation
  - Bot interaction and deployment scripts

## License
This project is licensed under a custom license allowing free use but not for financial gain.


## Future Improvements
- **Enhancements**:
  - Expand the dataset through scraping more "AskToAsk" questions in order to enhance the accuracy
  - Integrate more NLP rule-based matching techniques for better understanding of context
  


## About the Bot
For more information and to invite the bot into your server, visit our [Bot Invitation Link](https://discord.com/oauth2/authorize?client_id=1235240271994814464&permissions=274878032960&scope=bot).

If you're interested in testing the bot, join our [Discord testing server](https://discord.gg/Ka6THHvc8j).

---

### Motivation
I'm interested in learning more about natural language processing and looking to land an apprenticeship in France for a master's degree program. This project was a learning experience to improve my skills in NLP and machine learning, and I hope it can be useful to the community.

*Note: inspired by [Dontasktoask.com](https://dontasktoask.com/).*
