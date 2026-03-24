import os

MANUAL_PATH = "manuals"


def extract_device_from_filename(filename):

    filename = filename.replace(".txt", "")
    parts = filename.split("_")

    return parts[0].upper()


def search_manuals(question):

    question_words = question.lower().split()

    best_match = None
    highest_score = 0


    for file in os.listdir(MANUAL_PATH):

        filename = file.lower()

        score = sum(word in filename for word in question_words)

        if score > highest_score:

            highest_score = score
            best_match = file


    if best_match:

        filepath = f"{MANUAL_PATH}/{best_match}"

        with open(filepath, encoding="utf-8") as f:

            content = f.read()

        return content


    return None