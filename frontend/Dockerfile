# Stage 1 — Build Vue app
FROM node:20-alpine AS build-stage

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build


# Stage 2 — Serve with NGINX
FROM nginx:alpine

COPY --from=build-stage /app/dist /usr/share/nginx/html

# Custom nginx config for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
