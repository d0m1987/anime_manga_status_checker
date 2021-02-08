# HTML update checker

# Index
[Analysis of my favorite anime pages html structure](./docs/analysis/analysis_anime_pages.md)  
[Development process explained](./docs/development/development_process.md)

## Goal
The goal of this repository is to provide a website that gives you the ability to define XPATH values and be notified when they change.
The original purpose I started this project was to get notified of new anime / manga episodes I periodically check. Then I realized, that the idea can be made more generically and thus the project was changed to be a wider checker.  
If you like other mangas / animes / ..., please feel free to suggest further pages or better: directly create a pull request.

## Run tests

Following VS Code configs can be used to run pytest.

```bash
{
    "name": "Python: Run tests to console",
    "type": "python",
    "request": "launch",
    "module": "pytest",
    "args": ["tests"],
    "console": "integratedTerminal"
},
{
    "name": "Python: Run tests to file",
    "type": "python",
    "request": "launch",
    "module": "pytest",
    "args": ["tests", ">>", "pytest.output"],
    "console": "integratedTerminal"
}
```

## Run at startup with crontab

Open crontab with

```bash
crontab -e
```

Append to the crontab the following (adapted to your environment) task 

```bash
@reboot sleep 120 && /home/pi/scripts/html_update_checker/env/bin/python3 /home/pi/scripts/html_update_checker/start.py
```

We first wait 120 seconds to complete the startup, connect to the internet, etc.