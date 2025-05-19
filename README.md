# Infinite Derp

A Python tool to crawl Tailscale's DERP nodes from Shodan and convert them to Tailscale's node format.

## Features

- Searches Shodan for Tailscale DERP nodes (currently filtered for China).
- Converts results to Tailscale's DERP node JSON format.
- Outputs to `derp.json`.

## Requirements

- Python 3.7+
- Shodan API key

## Installation

1. Clone the repository.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. Copy `sample.env` to `.env`:

   ```bash
   cp sample.env .env
   ```

2. Edit `.env` and set your Shodan API key:

   ```conf
   SHODAN_API_KEY=your_actual_api_key_here
   ```

## Usage

Run the main script:

```bash
python main.py
```

- This will search Shodan for DERP nodes and write the results to `derp.json`.

## Output

- `derp.json` will contain the DERP nodes in Tailscale's node format, under region ID 900.

## Configuration

- You can adjust the Shodan search query in `main.py` to target different regions or keywords.

## License

[Specify your license here]
