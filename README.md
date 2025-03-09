# spotify-playlist

A simple tool to extract track information from Spotify playlist

## Requirements

- Python 3.6+
- Spotify API credentials

## Setup & Running Locally

```bash
# Set up virtual environment
python -m venv spotify_env
source spotify_env/bin/activate  # On Windows: spotify_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Get your credentials from https://developer.spotify.com/dashboard/
# Run the script
python spotify_tracks.py "https://open.spotify.com/playlist/1QEYHy5k9dtfLgQgC4HrqN" your_client_id your_client_secret

# Output to file
python spotify_tracks.py "https://open.spotify.com/playlist/1QEYHy5k9dtfLgQgC4HrqN" your_client_id your_client_secret > tracks.jsonl
```

## Docker Usage

```bash
docker run --rm -e SPOTIFY_CLIENT_ID=your_client_id -e SPOTIFY_CLIENT_SECRET=your_client_secret $(docker build -q .) "https://open.spotify.com/playlist/1QEYHy5k9dtfLgQgC4HrqN"
```

## Output Format

```json
{"artist": "FRAX, Senk", "name": "DROP THE BEAT", "url": "https://open.spotify.com/track/43xbHioriHFANtIRSuelrg"}
{"artist": "Rene Wise", "name": "Complicated", "url": "https://open.spotify.com/track/6s803Mds01E3KGc3sIx0kO"}
```

Status messages go to stderr, JSON data to stdout.