FROM node:18-alpine AS builder

WORKDIR /frontend

COPY package.json package-lock.json ./

RUN npm install

ENV NEXT_TELEMETRY_DISABLED 1

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
