Hello

1. To build a python virtual invironment and activate it:
    On Nightmare:
        - run command "make" in the same directory as the Makefile and the default target will run to build environment
    
    On Another device (alternate):
        - run command "make venv2" in the same directory as the Makefile and the target venv2 will be run

2. To install the packages numpy and matplotlib which are listed in requirements.txt file:
    - run "make install" and using pip it will install those packages

3. To deactivate the virtual environment, run command "deactivate"
4. To delete the virtual venv directory run "make clean"

5. To the 3 Scenarios file simple run on command line:
    - python <ScenarioFile>

    You can add the flag "-stochastic" to use stochastic transitions to train the agent
    e.g. python Scenario1.py -stochastic