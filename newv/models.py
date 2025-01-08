import json

# Class to manage topics from the database
class TopicsManager:
    def __init__(self, connection):
        self.connection = connection
        self.topics = self.load_topics()

    def load_topics(self):
        topics = {}
        if self.connection:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM topics")
            rows = cursor.fetchall()
            for row in rows:
                topics[row['name']] = {
                    "description": row['description'],
                    "example": row['example']
                }
            cursor.close()
        return topics

    def get_topic(self, topic_name):
        return self.topics.get(topic_name, {"description": "Topic not found", "example": ""})

# Class to manage quiz content from the database
class QuizManager:
    def __init__(self, connection):
        self.connection = connection
        self.quiz_content = self.load_quiz_content()

    def load_quiz_content(self):
        quiz_content = []
        if self.connection:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM quiz_content")
            rows = cursor.fetchall()
            for row in rows:
                quiz_content.append({
                    "question": row['question'],
                    "options": json.loads(row['options']),
                    "answer": row['answer']
                })
            cursor.close()
        return quiz_content
