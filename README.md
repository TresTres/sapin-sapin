# Sapin Sapin

## Table of Contents

- [Sapin Sapin](#sapin-sapin)
  - [Table of Contents](#table-of-contents)
  - [Development on the Backend](#development-on-the-backend)
    - [Test User](#test-user)
  - [Development on the Frontend](#development-on-the-frontend)
  - [Production / Containerization](#production--containerization)
  - [Cookies](#cookies)

## Development on the Backend

To set up the backend in isolation, follow these steps:

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
   This will run the backend server in DEV mode on `http://localhost:8000`.

### Test User

When running the backend server in DEV mode, a test user is created with the following credentials:

- Username: `testuser1`
- Email: `foobar@baz.net`
- Password: `testPassword987%`

## Development on the Frontend

To set up the frontend in isolation, follow these steps:

1. Navigate to the frontend folder:

   ```bash
   cd frontend
   ```

2. Ensure that you have Node.js at version 18 or higher installed. I recommend using [nvm](https://github.com/nvm-sh/nvm?tab=readme-ov-file#installing-and-updating). Then, run the following command to install the latest version of Node.js:

   ```bash
   nvm install 18 && nvm use 18
   ```

3. Install yarn by running the following command:

   ```bash
   npm install -g yarn
   ```

4. Install the project dependencies:

   ```bash
   yarn install
   ```

5. Start the frontend development server in DEV mode at `http://localhost:3000` by running the following command:
   ```bash
   yarn start dev
   ```

## Production / Containerization

Services are defined in `docker-compose.yml`. You can build and run the services in PROD mode by running the following command:

```bash
docker-compose up --build --force-recreate -d
```

Accessing the client will be at `http://localhost:4000`, and you'll likely be redirected to a login page.

Shut down the services with:

```bash
docker-compose down
```

## Cookies 
Be aware that running this application in a browser will require you to enable third-party cookies. <br>
This is because the backend server is running on a different port than the frontend server and browser cookies are used as part of JWT session management.