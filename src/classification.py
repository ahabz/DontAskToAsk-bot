from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib


model_tuned = joblib.load('res/model/SVM94Tuned20.joblib')
loaded_tfidf_vectorizer = joblib.load('res/model/tfidfvectorizer.pkl')


def Long_Q_segment(post_list, use_tfidf=False):
    permission_tracker = []

    for post in post_list:
        if use_tfidf:
            test_x = [post]

        else:

            test_x = loaded_tfidf_vectorizer.transform([post])

        # Get the probability scores for each class
        print(model_tuned)
        predicted_labels = model_tuned.predict(test_x)

        # Display the predicted labels and probability scores
        for label in zip(predicted_labels):
            permission_tracker.append(predicted_labels[0])

    if permission_tracker[-1] == 'PERMISSION':
        print('permissssssss')
        return 'PERMISSION'
    else:
        print(permission_tracker, '<-- this tracks')
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
    # Rename the variable to avoid conflict
    num_dividers = round(len(big_str) / ave_len)
    # Calculate the remainder
    remainder = len(big_str) % ave_len
    # Calculate the length of each segment
    segment_length = len(big_str) // num_dividers

    # Initialize variables
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
