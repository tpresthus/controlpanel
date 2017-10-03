# Controlpanel

Controlpanel is a simple controlpanel for easy home-automation.

Controlpanel was originally developed to run on a Raspberry Pi and control the heating, lamps, water pumps and other facilities of an RV.

It's written in python and uses Gtk for the frontend.

## Features

Controlpanel makes it easy to compose a touchscreen friendly GUI that connects to different actions.

Actions are primarily invoked as shell scripts / calling executables.

Currently two kind of actions are supported:
  - Short lived calls. These simply call their script, and triggers a callback upon success.
  - Long lived calls. These are designed to execute long-running scripts.

Controlpanel also makes it easy to gather information to be displayed in gauges or labels. Currently only fetching data by reading files is supported, but this can easily be extended. Files are polled for new data at configured intervals. 
