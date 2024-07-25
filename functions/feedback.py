from database import db

def insert_feedback(question: str, feedback: str):
    connection = db
    if connection:
        cursor = connection.cursor()
        sql = "INSERT INTO feedback (question, feedback) VALUES (%s, %s)"
        val = (question, feedback)
        cursor.execute(sql, val)
        connection.commit()
        cursor.close()
        connection.close()