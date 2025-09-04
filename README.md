# Placement Notifier

A Python script that monitors IIT Kanpur placement notices and sends notifications via ntfy.sh.

## Setup

1. **Install Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` file and edit it:**
   ```bash
   cp .env.example .env
   ```
3. **Download the ntfy app and subscribe to your topic:**
   - Install the [ntfy app](https://ntfy.sh) on your phone from the Play Store or App Store. You can also use the ntfy website at [https://ntfy.sh/app](https://ntfy.sh/app).
   - Open the app and tap the **plus (+) symbol** in the bottom right corner to "Subscribe to topic".
   - Enter the **topic name** (the server name you set in your `.env` file under `SERVER_NAME`).


4. **Run the script:**
   ```bash
   python3 main.py
   ```

## Features

- Monitors placement notices every minute
- Sends push notifications via ntfy.sh
- Tracks seen notices to avoid duplicates

