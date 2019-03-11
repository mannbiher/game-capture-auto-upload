# Automated watermark and upload of game-capture videos

Windows 10's XBOX game DVR and Nvidia GeForce Experience™ saves game capture videos in Videos folder. This program 
1. Polls the specified directory and re-encode the video with watermark using ffmpeg-cli.
2. Moves the original and re-encoded videos to specified folder. Useful when your primary drive has limited space
3. It then uploads the re-encoded videos to youtube

## Prerequisite
Download ffmpeg for windows and save in your path
https://www.ffmpeg.org/download.html

## Register your app for YouTube Credentials
1. You should have a Google Account
2. Register your app as Web-App and OAuth-2.0 credentials
https://developers.google.com/youtube/registering_an_application
2. Download and save client secrets as client_secret.json in project root directory
4. Get the credentials.json file using flask application
`
python flask_app.py
`
5. Flask app save the youtube credentials as credentials.json
6. Run the main python file
python main.py C:\Users\Your\Videos\UploadDirectory

## Caveats
1. Youtube upload works on quota system and thus number of uploads per 24 hours are limited.
https://developers.google.com/youtube/v3/getting-started#quota