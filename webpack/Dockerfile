FROM node:10-slim

WORKDIR /usr/src/app

COPY package.json ./
# TODO: somehow force npm to cache (shared volume in compose, but how?!)
RUN npm install
RUN rm package.json

COPY . .

ENTRYPOINT ["npm", "run"]