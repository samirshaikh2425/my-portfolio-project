# Flask Portfolio Project

A web-based portfolio project built using Python, Flask, and MySQL. The application provides a foundation for presenting portfolio content and managing contact form submissions through a database.

## Features

- Web application developed using Python and Flask.
- MySQL database integration.
- Contact form data storage using a MySQL database.
- Configuration through environment variables.
- HTML, and CSS for the frontend, as used in the project.
- Local development and deployment support.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| MySQL | Relational database |
| HTML | Web page structure |
| CSS | Styling and layout |
| Git and GitHub | Version control and source code hosting |

## Project Structure

The exact structure may vary depending on your implementation.

```text
portfolio-project/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── ...
├── static/
│   └── ...
└── .env                 # Local configuration; do not upload
```

## Prerequisites

Install the following before running the project locally:

- Python 3
- MySQL Server
- Git
- A code editor such as Visual Studio Code

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Replace the repository URL with your actual GitHub repository URL.

### 2. Create a virtual environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file in the project root and add the variables expected by your application.

Example:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=portfolio_db
FLASK_SECRET_KEY=your_secret_key
```

Replace the example values with your local configuration. Your application may require additional variables.

**Security:** Never commit your `.env` file, database password, secret key, or other sensitive credentials to GitHub.

### 5. Set up the MySQL database

Start your local MySQL server and create or import the database required by the application.

If your project uses the database `portfolio_db`, verify that it exists and that its required tables have been created. Import your database backup if you already have one.

Do not publish database backups containing personal information or credentials.

### 6. Run the application

If the Flask application instance is named `app` inside `app.py`, run:

```bash
python -m flask --app app run
```

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

If your application uses a different entry-point file or Flask instance name, adjust the command accordingly.

## Environment Configuration

The application may use the following environment variables:

| Variable | Description |
|---|---|
| `DB_HOST` | MySQL server hostname |
| `DB_USER` | MySQL username |
| `DB_PASSWORD` | MySQL password |
| `DB_NAME` | Database name |
| `FLASK_SECRET_KEY` | Secret key for Flask sessions and related security features |

Configure these variables according to the names actually used by your application.

## Deployment

The application can be deployed to a compatible Python hosting platform, such as Render, after configuring its production environment.

General deployment steps:

1. Push the project source code to GitHub.
2. Create a web service on your chosen hosting platform.
3. Connect the service to the GitHub repository.
4. Configure the build command:

   ```bash
   pip install -r requirements.txt
   ```

5. Configure a production start command if the project uses Gunicorn:

   ```bash
   gunicorn app:app
   ```

6. Configure the required environment variables in the hosting dashboard.
7. Set up a reachable hosted MySQL database and import the required schema and data.
8. Deploy the application and test its functionality.

The production database must be accessible from the hosting service. `localhost` refers to the running service itself, not your personal computer.

## Security Notes

- Keep `.env` out of version control.
- Use strong, unique passwords.
- Use a separate database account for the application rather than granting unnecessary administrative privileges.
- Do not expose secret keys, database credentials, or private user data.
- Use HTTPS and production-appropriate configuration when deploying.

## Author

**Samir Shaikh**

GitHub: https://github.com/samirshaikh2425

LinkedIn: https://www.linkedin.com/in/samir-shaikh-61071234b/

---

*This README describes the project's general setup. Update the features, file structure, database instructions, and deployment commands to match the final implementation.*