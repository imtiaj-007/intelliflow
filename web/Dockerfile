# Stage 1: Dependencies
FROM node:22-alpine AS deps
WORKDIR /app

# Install dependencies only when needed
COPY package.json package-lock.json* ./
RUN npm ci --only=production && \
    cp -R node_modules /prod_node_modules && \
    npm ci

# Stage 2: Builder
FROM node:22-alpine AS builder
WORKDIR /app

# Copy dependencies
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Set build-time environment variables
ENV NEXT_TELEMETRY_DISABLED=1

# Build Next.js application
RUN npm run build

# Stage 3: Runner (Production)
FROM node:22-alpine AS runner
WORKDIR /app

# Set production environment
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PORT=3000

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Install curl for health checks
RUN apk add --no-cache curl

# Copy necessary files from builder
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Set correct permissions
RUN chown -R nextjs:nodejs /app

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:3000 || exit 1

# Start application
CMD ["node", "server.js"]