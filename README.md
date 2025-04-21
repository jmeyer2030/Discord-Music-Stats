# Discord Music Stats

## Overview

This is a python script that can be used to view the song requests that you have sent in discord using flavibot. It offers basic analysis which can be interesting.

## Features

Depending on arguments displays:
 - user: Each user's most played songs, sorted by the number of songs that user has played, then each song they've played by count
 - total: The most played songs, and the number of times each user has played that songs

This script automatically detects .json files in the same directory as the script making it easy to analyze large numbers of messages without
manual file upload or typing out file paths.

## Requirements:

 - Flavibot usage in discord (No other music bot's messages will be processed, this script will not work for other music bots)
 - Python
 - Discrub, availible as a chrome extension here
   - https://chromewebstore.google.com/detail/discrub/plhdclenpaecffbcefjmpkkbdpkmhhbj?hl=en-US&pli=1

## Usage

### 1. Clone the repository

```
git clone https://github.com/jmeyer2030/Discord-Music-Stats.git
```

### 2. Use Discrub to get messages as a .json

The chrome extension is easy to use. There might be other ways of using Discrub.
If using the chrome extension:
 - Open discord in chrome
 - Click on the discrub icon at the top right and choose the server and channel. Press search.
 - Click Export messages, then export again and choose JSON
 - Repeat export for all channels you wish to use
 - Finally, move all exported .json files directly into the directory this file is in.

### 3. Run songRequests.py

Open this directory in your preferred terminal.

Run to view song requests per user.
```
python songRequests.py user
```

Run to view most played songs
```
python songRequests.py total
```
