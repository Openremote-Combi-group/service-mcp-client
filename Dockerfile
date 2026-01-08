# ----------------------------------------------------------------------
# This stage uses a Node image to download dependencies and compile the Vue app.
# ----------------------------------------------------------------------
FROM node:24-alpine AS ui-builder

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json first to take advantage of Docker caching.
# This step only re-runs if the dependency definitions change.
COPY ./ui/package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the application source code
COPY ./ui .

# Build the application for production.
# The output (usually 'dist' or 'build') will contain the static HTML, CSS, and JS files.
# The command below assumes your Vue CLI/Vite configuration outputs to a directory named 'dist'.
RUN npm run build

# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:alpine3.22

# Setup a non-root user
RUN adduser -D nonroot

# Use the non-root user to run our application
USER nonroot

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
    uv sync --locked --no-install-project

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app

COPY --from=ui-builder /app/dist ./static

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

EXPOSE 8421

CMD ["uv", "run", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8421"]