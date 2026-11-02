# syntax=docker/dockerfile:1
# Front-end: build com Node 24 LTS e arquivos estáticos servidos pelo nginx.
# Versões verificadas em 29/10/2026 — confira as atuais antes de fixar.
FROM node:24-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY . .
# VITE_API_URL é embutida no JavaScript na hora do build: nunca coloque segredos aqui.
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
