FROM node:22-slim

WORKDIR /app
ENV PORT=4173

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 4173
CMD ["npm", "run", "start"]
