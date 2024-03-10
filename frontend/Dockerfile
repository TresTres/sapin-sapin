FROM node:21.6.1-bullseye-slim as base

ARG API_VERSION
ARG BASE_URL
WORKDIR /client
ENV API_VERSION=${API_VERSION}
ENV BASE_URL=${BASE_URL}


# Install dependencies
# RUN apk update && apk upgrade
# RUN apk add git

COPY ./package*.json /client/
RUN yarn install && yarn cache clean --force

# Copy code into working directory.  Expected context: <project root>/frontend
COPY . /client

FROM base as development

# Run app in dev mode
CMD ["yarn", "dev"]


FROM base as production
# Create a user for running the app
WORKDIR /client
RUN useradd -m client_admin

# Build the app
RUN yarn build

# Set permissions
RUN chown -R client_admin:client_admin /client
USER client_admin

CMD [ "node", ".output/server/index.mjs" ]


