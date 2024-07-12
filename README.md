# SQL Chatbot Project

## Overview
SQL Chatbot is a web-based application that generates SQL queries based on user inputs, executes them, and displays the results. The application also provides data visualization capabilities for the executed queries. It also provides the option for user to customize the visualization as required.

## Features
- User-friendly interface for generating SQL queries.
- Execution of generated SQL queries against a database.
- Display of query results in a tabular format.
- Data visualization of query results.
- Option to edit visualization parameters and update the graph accordingly.

## Prerequisites
- Python 3.x
- FastAPI
- Pandas
- Matplotlib
- SQLAlchemy
- LangChain
- LIDA

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Ripperox/SQL_Chatbot.git
    cd SQL_Chatbot
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the project root directory and add the following:
    ```
    DB_USER=your_database_url
    DB_PASSWORD=your_database_password
    DB_HOST=your_database_host
    DB_NAME=your_database_name
    OPENAI_API_KEY=your_openai_key
    
    ```

## Usage

1. Start the Flask application:
    ```sh
    python main.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

3. Enter your SQL query in the provided input field and submit to generate and execute the query.

4. View the query results and data visualizations on the results page.

## Project Structure

- `main.py` - The entry point for the Flask application.
- `database.py` - Contains database connection and query execution logic.
- `logger.py` - Logging configuration and utilities.
- `py_modules.py` - Additional Python modules used in the project.
- `sql_query.py` - SQL query generation and manipulation functions.
- `visualization.py` - Functions for generating data visualizations.
- `.env` - Environment variables for database connection.

## Example

![image](https://github.com/user-attachments/assets/66969bf3-87b3-4ce2-a55a-076fe1236612)
![image](https://github.com/user-attachments/assets/81847c4b-8f89-4775-8c2f-ba06b4b32ccb)



## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License.

## Contact

Your Name - [rishitrdhote@gmail.com](mailto:rishitrdhote@gmail.com)

Project Link: [https://github.com/Ripperox/SQL_Chatbot](https://github.com/Ripperox/SQL_Chatbot)
