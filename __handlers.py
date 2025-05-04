"""
Utility functions for handling cost calculation and metrics and logs sending.

This module provides utility functions that are used to calculate the cost
of OpenAI API usage based on the model and token usage, as well as sending metrics and logs
to Grafana Cloud.

Functions:
    __check(metrics_url, logs_url, metrics_username, logs_username, access_token):
        Check if all required arguments are provided and modify metrics and logs URLs
    
    __calculate_cost(model, prompt_tokens, sampled_tokens):
        Calculate the cost based on the model, prompt tokens, and sampled tokens.

    __send_metrics(metrics_url, metrics_username, access_token, metrics):
        Send metrics to the specified Prometheus URL.
    
    __send_logs(logs_url, metrics_username, access_token, metrics):
        Send logs to the specified Loki URL.
"""
import logging
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

# Function to check if all required arguments are provided and modify metrics and logs URLs
def __check(metrics_url, logs_url, metrics_username, logs_username, access_token):
    # Check if all required parameters are provided
    if not all([metrics_url, logs_url, metrics_username, logs_username, access_token]):
        raise ValueError("All parameters (metrics_url, logs_url, metrics_username, "
                         "logs_username, access_token) must be provided")


    # Check if 'api/prom' is present in the metrics URL
    if "api/prom" not in metrics_url:
        raise ValueError("Invalid metrics URL format. It should contain 'api/prom' in the URL.")

    # Convert metrics_url to use the influx line protocol url
    if "prometheus" in metrics_url:
        metrics_url = metrics_url.replace("prometheus", "influx")
        metrics_url = metrics_url.replace("api/prom", "api/v1/push/influx/write")

        # Special case exception for prometheus-us-central1
        if "-us-central1" in metrics_url:
            metrics_url = metrics_url.replace("-us-central1", "-prod-06-prod-us-central-0")

    # Return metrics_url and logs_url without the trailing slash
    return (
        metrics_url[:-1] if metrics_url.endswith('/') else metrics_url,
        logs_url[:-1] if logs_url.endswith('/') else logs_url
    )


# Function to calculate the cost based on the model, prompt tokens, and sampled tokens
def __calculate_cost(model, prompt_tokens, sampled_tokens):
    # Define the pricing information for different models
    prices = {
        # GPT-4.1 Models
        "gpt-4.1": (0.002, 0.008),  # $2/1M input, $8/1M output
        "gpt-4.1-mini": (0.0004, 0.0016),  # $0.40/1M input, $1.60/1M output
        "gpt-4.1-nano": (0.0001, 0.0004),  # $0.10/1M input, $0.40/1M output
        "gpt-4.5-preview": (0.075, 0.15),  # $75/1M input, $150/1M output
        
        # GPT-4o Models
        "gpt-4o": (0.0025, 0.01),  # $2.50/1M input, $10/1M output
        "gpt-4o-mini": (0.00015, 0.0006),  # $0.15/1M input, $0.60/1M output
        
        # O-Series Models
        "o1": (0.015, 0.06),  # $15/1M input, $60/1M output
        "o1-pro": (0.15, 0.6),  # $150/1M input, $600/1M output
        "o3": (0.01, 0.04),  # $10/1M input, $40/1M output
        "o3-mini": (0.0011, 0.0044),  # $1.10/1M input, $4.40/1M output
        "o1-mini": (0.0011, 0.0044),  # $1.10/1M input, $4.40/1M output
        "o4-mini": (0.0011, 0.0044),  # $1.10/1M input, $4.40/1M output
        
        # GPT-4 Models
        "gpt-4": (0.03, 0.06),  # $30/1M input, $60/1M output
        "gpt-4-32k": (0.06, 0.12),  # $60/1M input, $120/1M output
        "gpt-4-turbo": (0.01, 0.03),  # $10/1M input, $30/1M output
        "gpt-4-turbo-2024-04-09": (0.01, 0.03),  # $10/1M input, $30/1M output
        "gpt-4-0613": (0.03, 0.06),  # $30/1M input, $60/1M output
        
        # GPT-3.5 Models
        "gpt-3.5-turbo": (0.0005, 0.0015),  # $0.50/1M input, $1.50/1M output
        "gpt-3.5-turbo-0125": (0.0005, 0.0015),  # $0.50/1M input, $1.50/1M output
        "gpt-3.5-turbo-16k": (0.003, 0.004),  # $3/1M input, $4/1M output
        "gpt-3.5-turbo-16k-0613": (0.003, 0.004),  # $3/1M input, $4/1M output
        "gpt-3.5-turbo-instruct": (0.0015, 0.002),  # $1.50/1M input, $2/1M output
        
        # Legacy Models (keeping for backward compatibility)
        "davinci-002": (0.002, 0.002),  # $2/1M input, $2/1M output
        "babbage-002": (0.0004, 0.0004),  # $0.40/1M input, $0.40/1M output
        "ada": (0.0004, 0.0004),
        "text-ada-001": (0.0004, 0.0004),
        "babbage": (0.0004, 0.0004),
        "text-babbage-001": (0.0004, 0.0004),
        "curie": (0.0020, 0.0020),
        "text-curie-001": (0.0020, 0.0020),
        "davinci": (0.0020, 0.0020),
        "text-davinci-001": (0.0020, 0.0020),
        "text-davinci-002": (0.0020, 0.0020),
        "text-davinci-003": (0.0020, 0.0020),
    }

    # First try exact match
    if model in prices:
        prompt_price, sampled_price = prices[model]
    else:
        # Find the longest matching model name
        matching_models = [m for m in prices.keys() if m in model]
        if matching_models:
            # Sort by length in descending order to get the longest match
            longest_match = sorted(matching_models, key=len, reverse=True)[0]
            prompt_price, sampled_price = prices[longest_match]
        else:
            # If no match found, return 0 cost
            return 0

    # Calculate the total cost based on prompt and sampled tokens
    cost = (prompt_tokens / 1000) * prompt_price + (sampled_tokens / 1000) * sampled_price

    return cost

# Function to send logs to the specified logs URL
def __send_logs(logs_url, logs_username, access_token, logs):
    try:
        response = requests.post(logs_url,
                                 auth=(logs_username, access_token),
                                 json=logs,
                                 headers={"Content-Type": "application/json"},
                                 timeout=60
                                )
        response.raise_for_status()  # Raise an exception for non-2xx status codes
    except requests.exceptions.RequestException as err:
        logger.error("Error sending Logs: %s", err)

# Function to send metrics to the specified metrics URL
def __send_metrics(metrics_url, metrics_username, access_token, metrics):
    try:
        body = '\n'.join(metrics)
        response = requests.post(metrics_url,
                                 headers={'Content-Type': 'text/plain'},
                                 data=str(body),
                                 auth=(metrics_username, access_token),
                                 timeout=60
                            )
        response.raise_for_status()  # Raise an exception for non-2xx status codes
    except requests.exceptions.RequestException as err:
        logger.error("Error sending Metrics: %s", err)