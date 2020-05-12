FROM node:10-slim

WORKDIR /usr/src/app

COPY package.json ./
RUN npm install
RUN rm package.json

COPY . .

ENTRYPOINT ["npm", "run"]