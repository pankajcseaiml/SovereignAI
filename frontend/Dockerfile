FROM node:20-alpine

WORKDIR /app

# Disable Next.js telemetry
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=development

# Install dependencies
COPY package*.json ./
RUN npm ci || npm install

# Copy source
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
