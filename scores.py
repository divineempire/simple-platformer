import csv
import os

SCORES_FILE = "scores.csv"


def get_scores():
    """Returns a list of scores from the scores file"""
    if not os.path.exists(SCORES_FILE):
        return []

    with open(SCORES_FILE) as file:
        reader = csv.reader(file)
        scores = [int(row[0]) for row in reader]
        return scores


def save_scores(scores):
    """Saves a list of scores to the scores file"""
    with open(SCORES_FILE, "w") as file:
        writer = csv.writer(file)
        rows = [[score] for score in scores]
        writer.writerows(rows)
