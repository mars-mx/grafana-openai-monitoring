# Grafana OpenAI Monitoring

A Python-based monitoring solution for OpenAI API usage, designed to track and visualize metrics in Grafana Cloud. This project is an actively maintained fork of [grafana-openai-monitoring](https://github.com/grafana/grafana-openai-monitoring).

## Features

- Real-time monitoring of OpenAI API usage
- Support for both chat completions and completions endpoints
- Custom metrics and fields support
- Integration with Grafana Cloud
- Detailed cost tracking based on current OpenAI pricing
- Easy setup and configuration

## Prerequisites

- Python 3.12 or higher
- OpenAI API key
- Grafana Cloud account
- Poetry for dependency management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mars-mx/grafana-openai-monitoring.git
cd grafana-openai-monitoring
```

2. Install dependencies using Poetry:
```bash
poetry install
```

## Configuration

Create a configuration file with your OpenAI and Grafana Cloud credentials:

```yaml
openai:
  api_key: your-openai-api-key

grafana:
  cloud_url: your-grafana-cloud-url
  api_key: your-grafana-api-key
```

## Pricing

The monitoring system uses the latest OpenAI pricing:

- GPT-4 Turbo: $0.01/1K input tokens, $0.03/1K output tokens
- GPT-3.5 Turbo: $0.0005/1K input tokens, $0.0015/1K output tokens
- Other models: Please refer to the [OpenAI pricing page](https://openai.com/pricing)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project is a fork of [grafana-openai-monitoring](https://github.com/grafana/grafana-openai-monitoring). We extend our gratitude to the original authors for their work. 