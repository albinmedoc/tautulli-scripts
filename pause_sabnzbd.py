import requests
import sys
import argparse

# Configuration
sabnzbd_url = ''
sabnzbd_api_key = ''

# ----------------------------------------------------------

import requests

# Function to pause SABnzbd
def pause_sabnzbd():
    response = requests.get(f'{sabnzbd_url}/sabnzbd/api?mode=pause&apikey={sabnzbd_api_key}')
    if response.status_code == 200:
        print('sabNZBd paused successfully.')
    else:
        print('Failed to pause SABnzbd.')

# Function to resume SABnzbd
def resume_sabnzbd():
    response = requests.get(f'{sabnzbd_url}/sabnzbd/api?mode=resume&apikey={sabnzbd_api_key}')
    if response.status_code == 200:
        print('SABnzbd resumed successfully.')
    else:
        print('Failed to resume SABnzbd.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pause or resume SABnzbd downloads.')
    parser.add_argument('action', choices=['pause', 'resume'], help='Action to perform: pause or resume')

    args = parser.parse_args()
    
    if(args.action == "pause"):
        pause_sabnzbd()
    else:
        resume_sabnzbd()

