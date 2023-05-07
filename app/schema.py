instructions = [
    'DROP TABLE IF EXISTS users;',
    """
        CREATE TABLE users (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username TEXT NOT NULL,
            uuid TEXT NOT NULL,
            voted TIMESTAMP
        );
    """,
    """
        CREATE TABLE questions (
            id INT PRIMARY KEY AUTO_INCREMENT,
            txt TEXT NOT NULL
        );
    """,
    """
        CREATE TABLE answers (
            id INT PRIMARY KEY AUTO_INCREMENT,
            question_id INT NOT NULL,
            txt TEXT NOT NULL
        );
    """,
    """
        CREATE TABLE votes (
            uuid TEXT ,
            question_id INT NOT NULL,
            answer_id INT NOT NULL,
            timelog TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """,
    """
        CREATE TABLE aux (
            participants INT 
        );
    """

]