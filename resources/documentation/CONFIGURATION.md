### Configuration

Jetson Camera currently supports a few different features gated behind command line arguments.

#### Debug Mode

`python3 Jetson/jetson-cam/main.py --debug`

Debug mode prints additional log items to console AND draws red bounding boxes around detected objects to assist in debugging.


#### Slack Notifications

`python3 Jetson/jetson-cam/main.py --slack-token <SLACK BOT TOKEN>`

By passing a Slack bot token, Jetson Camera will upload snapshots of detected objects to Slack.

To prevent notification flood, there is currently a 60s delay between motion notifications. This can be overridden by passing an overriding value: `--notification-delay=120`.


#### PTZ Support

**This feature is in active development**

`python3 Jetson/jetson-cam/main.py --ptz-test`

Used to verify functionality of I2C communication and servos.


#### Disabling Motion Detection

`python3 Jetson/jetson-cam/main.py --disable-motion`

Video steam only. Can be used if you do not want motion detection enabled.


#### Override Web Port

`python3 Jetson/jetson-cam/main.py --port 8080`

The web stream runs on port 8000 by default but can be overridden if necessary.