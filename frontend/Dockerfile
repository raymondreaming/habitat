FROM oven/bun:1-slim

WORKDIR /app
ENV PORT=4173

COPY package.json bun.lock ./
RUN bun install --frozen-lockfile

COPY . .

ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN bun run build

CMD ["bun", "run", "start"]
