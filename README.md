# Sapin Sapin

## Development on the Backend

To set up the backend, follow these steps:

1. Install Poetry by running the following command:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

2. Navigate to the backend folder:
    ```bash
    cd backend
    ```

3. Install the project dependencies:
    ```bash
    poetry install
    ```

4. To start the poetry shell, run the following command:
    ```bash
    poetry shell
    ```

5. To run the backend server in debug mode, run the following command:
    ```bash
    sh ./dev-server.sh
    ```
    This will run the backend server in debug mode on `http://localhost:8000`.

## Development on the Frontend

To set up the frontend, follow these steps:

1. Navigate to the frontend folder:
    ```bash
    cd frontend
    ```

2. Ensure that you have Node.js at version 18 or higher installed. I recommend using [nvm](https://github.com/nvm-sh/nvm?tab=readme-ov-file#installing-and-updating).  Then, run the following command to install the latest version of Node.js:
    ```bash
    nvm install 18 && nvm use 18
    ```

3. Install yarn by running the following command:
    ```bash
    npm install -g yarn
    ```

3. Install the project dependencies:
    ```bash
    yarn install
    ```

4. Start the frontend development server in debug mode at `http://localhost:3000` by running the following command: 
    ```bash
    yarn start dev
    ```

## Production / Containerization

## Test User
- Username: `testuser`
- Email: `foobar@baz.net`
- Password: `testPassword987%`