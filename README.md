# Uptime Kuma Network Agent

Uptime Kuma Network Agent is a monitoring agent designed to work with Uptime Kuma, a self-hosted monitoring tool. This agent periodically pings specified hosts and pushes the results to an external Uptime Kuma instance, allowing you to monitor the latency and availability of your internal network devices.

## Features

- Periodically fetches and updates the list of hosts from Uptime Kuma.
- Pings internal hosts and external Uptime Kuma instance.
- Pushes ping results to Uptime Kuma using the PUSH monitor type.
- Automatically restarts and starts on boot.

## Prerequisites

- Docker
- Docker Compose

## Installation

To set up and run the Uptime Kuma Network Agent using Docker Compose, follow these steps:

1. **Create a Docker Compose File:**

    Create a `docker-compose.yml` file with the following content:

    ```yaml
    version: '3'
    services:
      uptime-kuma-agent:
        image: zethraa/py-uptime-kuma-agent:latest
        environment:
          - UPTIME_KUMA_INSTANCE_HOSTNAME=uptime.example.com
          - UPTIME_KUMA_INSTANCE_URL=https://monitor.example.com
          - UPTIME_KUMA_INSTANCE_USERNAME=username
          - UPTIME_KUMA_INSTANCE_PASSWORD=password
        restart: always  # Ensure the container restarts automatically
        init: true  # Start the container on boot
    ```

2. **Configure Environment Variables:**

    Replace the environment variables in the `docker-compose.yml` file with your actual Uptime Kuma instance details:

    - `UPTIME_KUMA_INSTANCE_HOSTNAME`: The hostname of your Uptime Kuma instance. This will be used to measure latency between Uptike Kuma and internal devices.
    - `UPTIME_KUMA_INSTANCE_URL`: The URL of your Uptime Kuma dashboard.
    - `UPTIME_KUMA_INSTANCE_USERNAME`: Your Uptime Kuma dashboard username.
    - `UPTIME_KUMA_INSTANCE_PASSWORD`: Your Uptime Kuma dashboard password.

3. **Start the Docker Compose Services:**

    ```bash
    docker-compose up -d
    ```

    The `-d` flag runs the containers in detached mode.

## Usage

Once the agent is running, it will periodically fetch the list of hosts from your Uptime Kuma instance, ping them, and push the results back to Uptime Kuma. The agent will also automatically restart if it crashes and will start on boot.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Uptime Kuma](https://github.com/louislam/uptime-kuma) - A fancy self-hosted monitoring tool.
