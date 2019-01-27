FROM node:alpine

WORKDIR /usr/src/app

COPY . .

RUN npm install

ENV GOOGLE_APPLICATION_CREDENTIALS /usr/src/app/credentials.json

EXPOSE 3000

CMD ["npm", "start"]
