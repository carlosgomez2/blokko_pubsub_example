# GCP PubSub integration on Blokko Flask

## Requirements

- Python >= 3.11
- virtualenv
- pip3

## Setup

1. Clone project with git clone
2. Create a virtualenv with `python3 -m virtualenv .venv`
3. Activate the venv with `. ./.venv/bin/activate`, remember to activate the environment on all terminals as explained below.
4. Install dependencies `pip3 install -r requirements.txt`
5. Add `credentials.json` to root of project
6. Run the subscriber with `python3 subscriber.py` in a new terminal
7. Run the publisher with `python3 publisher.py` in another terminal tab
8. Activate the publisher sending a POST request to /publisher endpoint with `curl -X POST http://localhost:8080/publish` from another terminal tab

You need to run the processes on separate terminals.

Main.py file only acts as example.
