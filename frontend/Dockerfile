FROM node:17-alpine as builder
# set the working directory
WORKDIR /app
# install dependencies
COPY package.json .
RUN npm install
RUN npm install dotenv --save

# copy files from this repo into the working directory
COPY . .
# start the server
CMD ["npm", "start"]