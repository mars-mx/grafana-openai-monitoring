# Grafana OpenAI Monitoring

A Python library that provides decorators to monitor chat completions and Completions endpoints of the OpenAI API. It facilitates sending metrics and logs to **Grafana Cloud**, allowing you to track and analyze OpenAI API usage and responses. This project is an actively maintained fork of the python version in[grafana-openai-monitoring](https://github.com/grafana/grafana-openai-monitoring).

## Features

- Real-time monitoring of OpenAI API usage
- Support for both chat completions and completions endpoints
- Custom metrics and fields support
- Integration with Grafana Cloud
- Detailed cost tracking based on current OpenAI pricing
- Easy setup and configuration

## Prerequisites

- Python 3.7.1 or higher
- OpenAI API key
- Grafana Cloud account

## Installation

You can install the package using pip:

```bash
pip install grafana-openai-monitoring
```

Or using Poetry:

```bash
poetry install
```

## Usage

The following table shows which OpenAI function corresponds to which monitoring function in this library:

| OpenAI Function        | Monitoring Function |
|------------------------|---------------------|
| ChatCompletion.create  | chat_v2.monitor    |
| Completion.create      | chat_v1.monitor    |

### ChatCompletions

To monitor ChatCompletions using the OpenAI API, you can use the `chat_v2.monitor` decorator. This decorator automatically tracks API calls and sends metrics and logs to the specified Grafana Cloud endpoints.

Here's how to set it up:

```python
from openai import OpenAI
from grafana_openai_monitoring import chat_v2

client = OpenAI(
    api_key="YOUR_OPENAI_API_KEY",
)

# Apply the custom decorator to the OpenAI API function. To use with AsyncOpenAI, Pass `use_async` = True in this function.
client.chat.completions.create = chat_v2.monitor(
    client.chat.completions.create,
    metrics_url="YOUR_PROMETHEUS_METRICS_URL",  # Example: "https://prometheus.grafana.net/api/prom"
    logs_url="YOUR_LOKI_LOGS_URL",  # Example: "https://logs.example.com/loki/api/v1/push/"
    metrics_username="YOUR_METRICS_USERNAME",  # Example: "123456"
    logs_username="YOUR_LOGS_USERNAME",  # Example: "987654"
    access_token="YOUR_ACCESS_TOKEN"  # Example: "glc_eyasdansdjnaxxxxxxxxxxx"
)

# Now any call to client.chat.completions.create will be automatically tracked
response = client.chat.completions.create(model="gpt-4", max_tokens=100, messages=[{"role": "user", "content": "What is Grafana?"}])
print(response)
```

### Completions

To monitor completions using the OpenAI API, you can use the `chat_v1.monitor` decorator. This decorator adds monitoring capabilities to the OpenAI API function and sends metrics and logs to the specified Grafana Cloud endpoints.

Here's how to apply it:

```python
from openai import OpenAI
from grafana_openai_monitoring import chat_v1

client = OpenAI(
    api_key="YOUR_OPENAI_API_KEY",
)

# Apply the custom decorator to the OpenAI API function
client.completions.create = chat_v1.monitor(
    client.completions.create,
    metrics_url="YOUR_PROMETHEUS_METRICS_URL",  # Example: "https://prometheus.grafana.net/api/prom"
    logs_url="YOUR_LOKI_LOGS_URL",  # Example: "https://logs.example.com/loki/api/v1/push/"
    metrics_username="YOUR_METRICS_USERNAME",  # Example: "123456"
    logs_username="YOUR_LOGS_USERNAME",  # Example: "987654"
    access_token="YOUR_ACCESS_TOKEN"  # Example: "glc_eyasdansdjnaxxxxxxxxxxx"
)

# Now any call to client.completions.create will be automatically tracked
response = client.completions.create(model="davinci", max_tokens=100, prompt="Isn't Grafana the best?")
print(response)
```

## Configuration

To use the grafana-openai-monitoring library effectively, you need to provide the following information:

- **YOUR_OPENAI_API_KEY**: Replace this with your actual OpenAI API key.
- **YOUR_PROMETHEUS_METRICS_URL**: Replace the URL with your Prometheus URL.
- **YOUR_LOKI_LOGS_URL**: Replace with the URL where you want to send Loki logs.
- **YOUR_METRICS_USERNAME**: Replace with the username for Prometheus.
- **YOUR_LOGS_USERNAME**: Replace with the username for Loki.
- **YOUR_ACCESS_TOKEN**: Replace with the [Cloud Access Policy token](https://grafana.com/docs/grafana-cloud/account-management/authentication-and-permissions/access-policies/) required for authentication.

After configuring the parameters, the monitored API function will automatically log and track the requests and responses to the specified endpoints.

## Pricing

The monitoring system uses the latest OpenAI pricing:

- GPT-4 Turbo: $0.01/1K input tokens, $0.03/1K output tokens
- GPT-3.5 Turbo: $0.0005/1K input tokens, $0.0015/1K output tokens
- Other models: Please refer to the [OpenAI pricing page](https://openai.com/pricing)

## Dependencies
- [OpenAI](https://pypi.org/project/openai/)
- [requests](https://pypi.org/project/requests/)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project is a fork of [grafana-openai-monitoring](https://github.com/grafana/grafana-openai-monitoring). We extend our gratitude to the original authors for their work. 