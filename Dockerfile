# ========================================================
# Stage 1: Build dependencies
# ========================================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies if any are needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies to a local directory
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ========================================================
# Stage 2: Runtime
# ========================================================
FROM python:3.11-slim AS runner

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
COPY requirements.txt .

# Ensure scripts installed by pip are in PATH
ENV PATH=/root/.local/bin:$PATH

# Copy source code
COPY ./src ./src

# Expose port for FastAPI
EXPOSE 8000

# Run FastAPI using uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
