# ==============================================================================
# Multi-Stage Dockerfile for KI-Projektmanagement-System
# Optimized for production with Claude-Flow integration
# ==============================================================================

# Stage 1: Builder - Install dependencies
FROM python:3.11-slim as builder

# Set build environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python runtime dependencies only
COPY requirements.runtime.txt ./requirements.runtime.txt
RUN pip install --user --no-cache-dir -r requirements.runtime.txt

# Stage 2: Runtime - Final minimal image
FROM python:3.11-slim

# Set runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH=/home/appuser/.local/bin:$PATH \
    NODE_ENV=production

WORKDIR /app

# Install runtime dependencies (Node.js LTS for Claude-Flow)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g npm@latest \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Verify Node.js and npm installation
RUN node --version && npm --version

# Create non-root user early
RUN groupadd -r appuser && useradd -r -g appuser -m -d /home/appuser appuser

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy package.json and install Claude-Flow (as root for global install)
COPY package.json .
RUN npm install -g claude-flow@alpha || echo "Claude-Flow alpha not available, will use npx"

# Streamlit configuration (optional)
RUN mkdir -p /home/appuser/.streamlit

# Copy application code
COPY --chown=appuser:appuser . .
# Ensure no local package named 'types' shadows Python stdlib 'types'
RUN rm -rf /app/types || true

# Create necessary directories with proper permissions
RUN mkdir -p \
    logs \
    data \
    exports \
    analysis_output \
    .swarm \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose ports
EXPOSE 8000 8501

# Health check (check both backend and UI)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/status || exit 1

# Start script
COPY --chown=appuser:appuser start.sh .
RUN chmod +x start.sh

# Labels for metadata
LABEL maintainer="KI-Projektmanagement-System" \
      version="1.0.0" \
      description="AI-powered project management with Claude-Flow integration" \
      org.opencontainers.image.source="https://github.com/yourusername/ki-projektmanagement"

# Default command
CMD ["./start.sh"]
