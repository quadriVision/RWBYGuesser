# RWBYGuesser

A simple episode guesser game for RWBY<br>
In this game, you have to guess the episode based on the screenshot you receive

## How to run
1. Install [Python](https://www.python.org/)
2. Download the files and the screenshots from [my website](https://quadvision.eu/episodes.7z)
3. Put all of those files and folders in one folder
4. Open CMD in the folder and run "pip install -r requirements.txt". This will install all the necessary dependencies.
5. After the installation has finished, run "flask --app backend run". You might have to close and reopen the cmd.

## How to host using gunicorn and nginx (Linux only)
1. Do all the steps above except for step 5
2. Run "gunicorn backend:app"
3. Put this snippet into nginx:
```
location / {
      proxy_pass http://127.0.0.1:8000/;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_set_header X-Forwarded-Host $host;
      proxy_set_header X-Forwarded-Prefix /;
}
```
4. On the second line, change the port to whatever gunicorn shows.
5. Restart nginx with "sudo systemctl restart nginx"
6. RWBYGuesser is now can be accessed publicly.
