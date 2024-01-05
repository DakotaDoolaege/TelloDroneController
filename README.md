Program for controlling my DJI Tello drone from the command line.

Also supports displaying live video and status information from the drone.

# Install
Create a virtual environment:
`python3 -m venv myvenv`

Activate your new virtual environment:
`source myvenv/bin/activate`

Install the required packages:
`pip install -r requirements.txt`

# Running
`./tello.py`

The program will send typed commands to the drone. See the 
[Official Tello SDK](https://www.ryzerobotics.com/tello/downloads) for a list
of commands.

## Custom commands
#### stateon
Activates the asynchronous state handler.

#### stateoff
Deactivates the asynchronous state handler.

