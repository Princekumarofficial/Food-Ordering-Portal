FROM node:18-alpine AS builder

WORKDIR /frontend

COPY package.json package-lock.json ./

RUN npm install

ENV NEXT_TELEMETRY_DISABLED 1

COPY . .

RUN npm run build

FROM node:18-alpine AS production

WORKDIR /frontend

COPY package.json package-lock.json ./
RUN npm install --production

COPY --from=builder /frontend/.next ./.next
COPY --from=builder /frontend/public ./public
COPY --from=builder /frontend/next.config.mjs ./next.config.mjs

EXPOSE 3000

CMD ["npm", "start"]
