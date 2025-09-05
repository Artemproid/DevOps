FROM node:16

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . ./

# Установить переменную окружения для обхода проблем с OpenSSL
ENV NODE_ENV=development

EXPOSE 3000

CMD ["npm", "start"] 