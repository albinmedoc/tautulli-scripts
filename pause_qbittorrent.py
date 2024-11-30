import requests
import sys
import argparse

# Configuration
qbittorrent_url = ''
qbittorrent_username = ''
qbittorrent_password = ''
qbittorrent_categories = ['sonarr', 'radarr', 'prowlarr']

# ----------------------------------------------------------

import requests

# Function to authenticate with qbittorrent
def authenticate_qbittorrent():
    payload = f'username={qbittorrent_username}&password={qbittorrent_password}'
    headers = {
      'Referer': qbittorrent_url,
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", f'{qbittorrent_url}/api/v2/auth/login', headers=headers, data=payload)
    if response.status_code == 200:
        return response.cookies
    else:
        print('Failed to authenticate with qbittorrent.')
        return None

# Function to get torrents by category
def get_torrents_by_category(category, cookies):
    response = requests.get(f'{qbittorrent_url}/api/v2/torrents/info?category={category}', cookies=cookies)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to get torrents for category {category}.')
        return []

# Function to pause torrents by hashes
def pause_torrents(hashes, cookies):
    headers = {
      'Referer': qbittorrent_url,
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(f'{qbittorrent_url}/api/v2/torrents/pause', headers=headers, data={'hashes': '|'.join(hashes)}, cookies=cookies)
    if response.status_code == 200:
        print('Torrents paused successfully.')
    else:
        print('Failed to pause torrents.')

# Function to resume torrents by hashes
def resume_torrents(hashes, cookies):
    headers = {
      'Referer': qbittorrent_url,
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(f'{qbittorrent_url}/api/v2/torrents/resume', headers=headers, data={'hashes': '|'.join(hashes)}, cookies=cookies)
    if response.status_code == 200:
        print('Torrents resumed successfully.')
    else:
        print('Failed to resume torrents.')

# Function to pause qbittorrent
def pause_qbittorrent():
    cookies = authenticate_qbittorrent()
    if cookies:
        for category in qbittorrent_categories:
            torrents = get_torrents_by_category(category, cookies)
            hashes = [torrent['hash'] for torrent in torrents]
            pause_torrents(hashes, cookies)

# Function to resume qbittorrent
def resume_qbittorrent():
    cookies = authenticate_qbittorrent()
    if cookies:
        for category in qbittorrent_categories:
            torrents = get_torrents_by_category(category, cookies)
            hashes = [torrent['hash'] for torrent in torrents]
            resume_torrents(hashes, cookies)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pause or resume qbittorrent downloads.')
    parser.add_argument('action', choices=['pause', 'resume'], help='Action to perform: pause or resume')

    args = parser.parse_args()
    
    if(args.action == "pause"):
        pause_qbittorrent()
    else:
        resume_qbittorrent()

