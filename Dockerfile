FROM ghcr.io/astral-sh/uv:alpine AS app-builder

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project \


# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"


# ----------------------------------------------------------------------
# This stage uses a Node image to download dependencies and compile the Vue app.
# ----------------------------------------------------------------------
FROM node:24-alpine AS ui-builder

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json first to take advantage of Docker caching.
# This step only re-runs if the dependency definitions change.
COPY ./src/services/mcp-client-api/ui/package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the application source code
COPY ./src/services/mcp-client-api/ui .

# Build the application for production.
# The output (usually 'dist' or 'build') will contain the static HTML, CSS, and JS files.
# The command below assumes your Vue CLI/Vite configuration outputs to a directory named 'dist'.
RUN npm run build

FROM ghcr.io/astral-sh/uv:alpine AS production
LABEL authors="Fontys-OpenRemote"

WORKDIR /app

# Copy the builder outputs to current stage
COPY --from=app-builder /app .
COPY --from=ui-builder /app/dist ./static

COPY ./src/shared ./shared
COPY ./src/services/mcp-client-api/app ./mcp-client-api/app

EXPOSE 8421

ENTRYPOINT ["uv", "run", "uvicorn", "mcp-client-api.app:app", "--host", "0.0.0.0", "--workers", "4", "--port", "8421"]