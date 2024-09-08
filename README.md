# Recyclo

Recyclo is a web application designed to enhance waste management and recycling efficiency. It provides a robust platform for users to manage waste donations and receive rewards. By integrating a rewards-based approach, Recyclo aims to make recycling more appealing and effective, capturing value from waste and encouraging sustainable practices.

## Key Features

- **User Management:** Easy registration, login, and profile updates.
- **Donation Workflow:** Specify waste types, input donation weights, and find local recycling hubs.
- **Coupon System:** Generates coupons based on the amount of recyclable materials donated, incentivizing recycling and promoting greater community engagement.
- **Donation Logs:** Track and view detailed records of all donations.

## Tech Stack

- **Flask:** Web framework for backend development.
- **SQLAlchemy:** ORM for database management.
- **HTML/CSS:** For structuring and styling the web pages.
- **Python:** Programming language used for backend logic.
- **Jinja2:** Templating engine for rendering HTML templates.
- **Figma:** Design tool used for creating user interface mockups.
- **JavaScript:** Adds interactivity to the web pages.

## Getting Started

To set up and run the application locally, follow these steps:

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/Recyclo.git
    ```

2. **Navigate to the Project Directory:**
    ```bash
    cd Recyclo
    ```

3. **Set Up a Virtual Environment:**
    ```bash
    python -m venv venv
    ```

4. **Activate the Virtual Environment:**
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

5. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

6. **Initialize the Database:**
    ```bash
    flask shell
    >>> from app import db
    >>> db.create_all()
    >>> exit()
    ```

7. **Run the Application:**
    ```bash
    flask run
    ```

8. **Access the Application:**
    Open your browser and go to `http://127.0.0.1:5000`.

## Usage

1. **Registration:** Sign up with a username, name, email, and password.
2. **Login:** Access the platform using your credentials.
3. **Donate Waste:** Enter waste details, weight, and find recycling hubs.
4. **View Coupons:** Receive and use coupons based on your donations.
5. **Track Donations:** View and manage your donation history.

## Contributing

We welcome contributions to Recyclo! To get involved:

- **Report Issues:** Open an issue for bugs or feature requests.
- **Submit Pull Requests:** Make improvements or fixes and submit a pull request.


## Contact

For any questions or feedback, please contact karanamsruthi17@gmail.com .

---
