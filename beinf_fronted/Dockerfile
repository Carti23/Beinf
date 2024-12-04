FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
# Option 1: Use npm install instead of npm ci
RUN npm install

# Option 2: If you want to stick with npm ci, ensure package-lock.json is in sync first
# COPY package*.json ./
# RUN npm install --package-lock-only
# RUN npm ci

COPY . .

FROM node:18-alpine

WORKDIR /app

COPY --from=builder /app .

CMD ["npm", "start"]