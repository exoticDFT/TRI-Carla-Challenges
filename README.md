This repository was made as a general location to host code and scripts used for the TRI Carla Challenges. It will hold various scenario files and scripts for running scenarios for use during the TRI Carla Challenges and useful tools while testing Carla implementations.

### Setting up your environment
Begin by cloning the repository to your local machine. Once cloned, you must first add the repository directory to your `PYTHONPATH` environment variable. This can be done in the terminal you wish to run the scenario or added to `.bashrc` or similar. For example, if you cloned to `/home/username/TRI-Carla-Challenges`, export the path as follows 
```
bash
export PYTHONPATH=/home/username/TRI-Carla-Challenges:$PYTHONPATH
```

We must also make sure the necessary Python packages are installed for using the Carla API. This can be done by simply installing the requirements with `pip` using the `requirement.txt` file.
```
bash
pip3 install --user -r requirements.txt
```

### Running the scenario
Start by running a server instance of Carla (**version [0.9.5](https://github.com/carla-simulator/carla/releases/tag/0.9.5)**) with the default parameters. This can be done following the information found on [Carla's wiki](https://carla.readthedocs.io/en/latest/getting_started/). As an example, you can run a Carla server instance in a windowed mode using the following command when in the Carla install directory:
```
bash
./CarlaUE4.sh -windowed -ResX=1280 -ResY=720 -benchmark -fps=30
```
To better understand these arguments, see [Carla's documentation](https://carla.readthedocs.io/en/latest/configuring_the_simulation/) and [Unreal Engine's documentation](https://docs.unrealengine.com/en-US/Programming/Basics/CommandLineArguments/index.html) on the topic.

Once the Carla server is running, you can run the scenario. Make sure you've followed the [environment instructions](#Setting-up-your-environment). Once your path is configured, to start the scenario, simply run
```bash
python3 Scripts/Event4.py
```

This will run the scenario with random parameters based on the system time when calling the python script. There are several options one can add to the runtime via arguments to the script. These arguments include connection to different host and port configurations for a server instance, a random seed to run a pseudorandom scenario, and timeout for connections with the server. For more information of the available arguments, you can add the `--help` argument to the above command to display the help menu for the script. For this release, you will have to start your ego vehicle script manually. This should be done shortly after the `Event4` script is run. Just call your script (let's say it's called `ego_vehicle.py`) in a terminal where the script is contained.

```bash
python3 ego_vehicle.py
```

**A quick note for running during the competition:** *Python's random module has different seeding behavior based on the version of Python. For the competition, it is expected everyone will be using Python 3, to guarantee the scenario will be equivalent between users when a seed is provided.*

---

### Release notes
#### 0.2
- Updates `Event4.py` script to handle the overall agent handling for the scenario. No need to call `remove_actors.py` unless you want to clear out the entire world of all vehicles.
- Modifies `remove_actors.py` to remove all vehicles from the Carla server, including any ego vehicles.
- Adds `--num-agents` argument to `Event4.py` to specify the total number of ambient vehicles used in the scenario (default is 10 when not used.)
- Replaces the large `carla_common` module with several smaller and more specific modules.
#### 0.1
- Creates a utilities library which provides several useful utility functions that can be used throughout your Carla client script.
- Adds a Scripts directory for holding various scripts that can be used for testing ego vehicle implementations. Specifically,
  - `Event4.py`: Used for running an initial scenario for the fourth event.
  - `remove_actors.py`: Used for removing vehicles from the Carla server that are no longer within 100 meters of the traffic circle in Town03.

#### General
- The releases have only been fully tested with Python 3.5, but is expected to work with 3.5+.

---

>##### Notes for users and contributors:
>  - ###### The repository will follow the [GitFlow workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
>  - ###### When making a commit, try to make commits small and related to a specific issue. Tense should be present and be written as if the commit is telling you what it is doing. Include the related issue in the summary as well. E.g. Issue #12: Adds a function for handling string comparisons.
>  - ###### When creating a new issue, please be as specific as possible. For bugs, list as many details as possible, including how to reproduce the bug, errors you receive, the expected results, your actual results, etc. For feature requests, provide a precise summary, add a detailed description of the request, be concise, if you can, propose a solution, etc.