FROM node:21.6.1-bullseye-slim

ARG API_VERSION
ARG BASE_URL

# Create a user for running the app
RUN useradd -m client_admin

WORKDIR /client

# Install dependencies
# RUN apk update && apk upgrade
# RUN apk add git

COPY ./package*.json /client/
RUN yarn install && yarn cache clean --force

# Copy code into working directory.  Expected context: <project root>/frontend
COPY . /client

# Build the app
ENV API_VERSION=${API_VERSION}
ENV BASE_URL=${BASE_URL}
RUN yarn build

# Set permissions
RUN chown -R client_admin:client_admin /client
USER client_admin

CMD [ "node", ".output/server/index.mjs" ]


