# Canva Monitor V2

Continuously monitors a BingoTingo page for updated Canva Group invitation links, extracting the new token and sending a Telegram notification upon changes.

## Tech Stack
- Python 3.12
- Playwright
- SQLite3
- Systemd

## Installation

1. Clone or copy the repository to your Ubuntu 24.04 server.
2. Run the installation script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

## Configuration

Edit `config/config.py` or set environment variables:
- `BOT_TOKEN`: Your Telegram Bot API token.
- `CHAT_ID`: Your Telegram Chat ID.
- `BINGO_URL`: The target URL to monitor.
- `WAIT_SECONDS`: Countdown time (default 65).
- `CHECK_INTERVAL`: Sleep time between checks (default 300).
- `HEADLESS`: Set to `True` for server environments.

## Run Manually

Activate the virtual environment and run the script:
```bash
source venv/bin/activate
python run.py
```

## Run as Service

To ensure the monitor runs continuously and restarts automatically:

1. Edit `systemd/canva-monitor.service` and verify `WorkingDirectory` and `ExecStart` paths.
2. Copy the service file to systemd:
   ```bash
   sudo cp systemd/canva-monitor.service /etc/systemd/system/
   ```
3. Reload systemd, enable, and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable canva-monitor.service
   sudo systemctl start canva-monitor.service
   ```
4. Check status:
   ```bash
   sudo systemctl status canva-monitor.service
   ```

## Logs

Logs are stored in `logs/monitor.log` and rotate daily.
To monitor real-time logs via systemd:
```bash
journalctl -u canva-monitor.service -f
```

## Troubleshooting
- **Browser Timeout:** Usually caused by network latency. The monitor will automatically retry on the next interval.
- **Telegram Failure:** Verify `BOT_TOKEN` and `CHAT_ID`.
- **Database Locked:** Ensure no other process is actively writing to `data/monitor.db`.
