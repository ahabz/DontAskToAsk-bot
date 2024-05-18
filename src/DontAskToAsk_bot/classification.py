from collections import Counter
from config import Config
import warnings

warnings.filterwarnings("ignore")
import joblib
from loguru import logger

logger.add(
    "logs/main.log",
    format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message} | {extra}",
)


model_path = Config.from_env_SVM()
tfidf_path = Config.from_env_TFIDF()

if model_path is not None and tfidf_path is not None:
    model_tuned = joblib.load(model_path.token)
    loaded_tfidf_vectorizer = joblib.load(tfidf_path.token)

else:
    logger.critical("Model/vectorizer path is empty, cannot run classifier")


logger.info("Model loaded successfully")


def Long_Q_segment(post_list, use_tfidf=False):
    permission_tracker = []  # used in majority vote

    for post in post_list:
        if use_tfidf:
            test_x = [post]

        else:
            test_x = loaded_tfidf_vectorizer.transform([post])

        # Get the probability scores for each class
        predicted_labels = model_tuned.predict(test_x)

        # Display the predicted labels and probability scores
        for label in zip(predicted_labels):
            permission_tracker.append(predicted_labels[0])

    if permission_tracker[-1] == "PERMISSION":
        return "PERMISSION"
    else:
        label_counts = Counter(permission_tracker)

        # Find the label with the highest count
        majority_label = str(label_counts.most_common(1)[0][0])

        return majority_label


def segment_posts(test_str, ave_len=12):
    # Tokenize the input string
    big_str = test_str.split()
    if len(big_str) <= ave_len:
        return [test_str]

    # Calculate the number of dividers
    num_dividers = round(len(big_str) / ave_len)
    # Calculate the remainder
    remainder = len(big_str) % ave_len
    # Calculate the length of each segment
    segment_length = len(big_str) // num_dividers

    segments = []
    start_index = 0
    # Create segments
    for i in range(num_dividers):
        end_index = min(start_index + segment_length, len(big_str))
        segments.append(big_str[start_index:end_index])
        start_index = end_index

    # Add the remaining words to the last segment
    segments[-1] += big_str[start_index:]

    segments_sent = [" ".join(segment) for segment in segments]

    return segments_sent
