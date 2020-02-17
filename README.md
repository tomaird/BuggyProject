# Buggy Project


Code from my 3rd year university project, which involved creating an autonomous buggy to navigate a maze and perform various tasks. The code in this repository does the following:

# Python
- connects to a WiFi access point to retrieve the maze information
- decodes this information into a map of the maze, the obstacles, and points of interest to send the buggy to
- uses the A* algorithm to plot a route around this maze
- translates this route into movement instructions to send to the buggy via bluetooth through a serial port
- retrieve data collected by the buggy at various points
- displays all of the above on an interactive and configurable GUI

# C++
- Runs on the arduino onboard the buggy
- Recieves instructions from the host PC, and decodes them into movements on each individual wheel
- Movement is based on a grid. The arduino must move only inline with the grid, using data from external sensors
- Senses data (voltage) and sends this data to the PC to be displayed
