# OpenRemote MCP Client (Ask-Marc)
An AI client for your OpenRemote instance with support for MCP.



## Quick start guide
This guide assumes you already have an OpenRemote instance running.

1. **Create service user**

   In your OpenRemote instance, create a new service user (`settings > users > SERVICE USERS > ADD USER`) and give it the permissions you want to have.
   The MCP server will auto discover the tools that are available.

   _Note: The service user is required to have the `read:services` & `write:services` role._


2. **Setup docker service**
   Create a docker-compose.yml file and configure the service.
    ```yaml
    services:
      # Other OpenRemote services...
    
      mcp-client:
        image: openremote/mcp-client:latest
        restart: always
        depends_on:
          manager:
            condition: service_healthy
          mcp-server:
            condition: service_started
        ports:
          - "8421:8421"
        volumes:
          - ./mcp_config.json:/app/mcp_config.json
        environment:      
          OPENREMOTE_CLIENT_ID=<OPENREMOTE_CLIENT_ID>
          OPENREMOTE_CLIENT_SECRET=<OPENREMOTE_CLIENT_SECRET>
          OPENREMOTE_URL=<OPENREMOTE_URL>
          OPENREMOTE_VERIFY_SSL=1
    
          # Fill one of the following keys or both!
          OPENAI_API_KEY=<OPENAI_API_KEY>
          ANTHROPIC_API_KEY=<ANTHROPIC_API_KEY>
    ```

3. **Create MCP configuration**

   Create a new file `mcp_config.json` in the same directory as the `docker-compose.yml` file.
   Add any MCP configuration you want to use. Below is a quick example to connect it to the OpenRemote MCP server.
    ```json
    {
      "openremote": {
        "transport": "streamable_http",
        "url": "https://mcp-server:8420/mcp"
      }
    }
    ```

4. **Run the service**

   Finally, you can run the new services by using docker compose.
    ```shell
    docker compose up
    ```
   This will run the additional service, it will auto-register to your OpenRemote instance. and you can view them in the services tab inside your OpenRemote dashboard.


## Development guide
This guide assumes you already have an OpenRemote instance running.

1. **Create service user**

   In your OpenRemote instance, create a new service user (`settings > users > SERVICE USERS > ADD USER`) and give it the permissions you want to have.
   The MCP server will auto discover the tools that are available.

   _Note: The service user is required to have the `read:services` & `write:services` role._


2. **Sync dependencies**
    ```shell
    uv sync
    ```

3. **Setup environment variables**

   Create a new file `.env` in the root of the project directory. and fill in the following variables replacing the brackets with your own values.
    ```dotenv
    OPENREMOTE_CLIENT_ID=<OPENREMOTE_CLIENT_ID>
    OPENREMOTE_CLIENT_SECRET=<OPENREMOTE_CLIENT_SECRET>
    OPENREMOTE_URL=<OPENREMOTE_URL>
    OPENREMOTE_VERIFY_SSL=1
   
    # Fill one of the following keys or both!
    OPENAI_API_KEY=
    ANTHROPIC_API_KEY=
    ```

4. **Create MCP configuration**

   Create a new file `mcp_config.json` in the root directory of the project.
   Add any MCP configuration you want to use. Below is a quick example to connect it to the OpenRemote MCP server.
    ```json
    {
      "openremote": {
        "transport": "streamable_http",
        "url": "http://localhost:8420/mcp"
      }
    }
    ```

5. **Setup UI**

   Go into the `ui` directory and install the npm packages.
    ```shell
    cd ui && npm install
    ```

6. **Run service**
    ```shell
    uv run uvicorn app:app --reload --port=8421
    ```

   Ask-Marc UI:
    ```shell
    cd ui && npm run dev
    ```
