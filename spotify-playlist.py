import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import atexit
import glob

# Clean up cache file
def cleanup_cache():
    # Delete all .cache files in the current directory
    cache_files = glob.glob('.cache*')
    for file in cache_files:
        try:
            os.remove(file)
        except Exception:
            pass  # Silently ignore any errors

# Register the cleanup function to run when the script exits
atexit.register(cleanup_cache)

def extract_playlist_id(playlist_url):
    """Extract the playlist ID from a Spotify playlist URL."""
    # Common formats:
    # https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
    # spotify:playlist:37i9dQZF1DXcBWIGoYBM5M
    
    pattern = r'playlist[/|:]([a-zA-Z0-9]+)'
    match = re.search(pattern, playlist_url)
    
    if match:
        return match.group(1)
    else:
        raise ValueError(f"Could not extract playlist ID from URL: {playlist_url}")

def get_track_info(playlist_url, client_id=None, client_secret=None):
    """
    Get track information from a Spotify playlist URL.
    
    Args:
        playlist_url (str): URL of the Spotify playlist
        client_id (str, optional): Spotify API client ID. If None, will try to get from environment variable.
        client_secret (str, optional): Spotify API client secret. If None, will try to get from environment variable.
        
    Returns:
        list: List of dictionaries containing track info (artist, name, url)
    """
    # Get credentials from arguments or environment variables
    client_id = client_id or os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = client_secret or os.environ.get('SPOTIFY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        raise ValueError(
            "Spotify API credentials not provided. Either pass them as arguments or "
            "set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables."
        )
    
    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    playlist_id = extract_playlist_id(playlist_url)
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    track_info = []
    for item in tracks:
        track = item['track']
        if track:  # Sometimes tracks can be None (e.g., if removed from Spotify)
            # Get all artists
            artists = [artist['name'] for artist in track['artists']]
            artists_str = ", ".join(artists)
            
            track_data = {
                "artist": artists_str,
                "name": track['name'],
                "url": f"https://open.spotify.com/track/{track['id']}"
            }
            track_info.append(track_data)
    
    return track_info

def main():
    if len(sys.argv) < 2:
        print("Usage: python spotify_tracks.py <playlist_url> [client_id] [client_secret]")
        sys.exit(1)
    
    playlist_url = sys.argv[1]
    client_id = sys.argv[2] if len(sys.argv) > 2 else None
    client_secret = sys.argv[3] if len(sys.argv) > 3 else None
    
    try:
        import json
        tracks = get_track_info(playlist_url, client_id, client_secret)
        print(f"Found {len(tracks)} tracks in playlist.", file=sys.stderr)
        
        # Output each track as a JSON line to stdout
        for track in tracks:
            print(json.dumps(track))
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()