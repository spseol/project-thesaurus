FROM node:10-slim

WORKDIR /usr/src/app

COPY package.json package-lock.json ./
RUN npm ci && rm package.json package-lock.json

COPY . .

ENTRYPOINT ["npm", "run"]