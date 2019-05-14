This repository was made as a general location to host code and scripts used for the TRI Carla Challenges. It will hold various scenario files and scripts for running scenarios for use during the TRI Carla Challenges and useful tools while testing Carla implementations.

### Running the scenario
Begin by cloning the repository to your local machine. Once cloned, you should run a server instance of Carla (version 0.9.5) with the default parameters. This can be done following the information found on [Carla's wiki](https://carla.readthedocs.io/en/latest/getting_started/).

When the Carla server is running, to run the scenario, simply run
```bash
python Scripts/Event4.py
```

This will run the scenario with random parameters based on the system time when calling the python script. There are several options one can add to the runtime via arguments to the script. These arguments include connection to different host and port configurations for a server instance, a random seed to run the scenario with the same environment, and timeout for connections with the server. For more information of the available arguments, you can add the `--help` argument to the above command to display the help menu for the script. For this release, to have the scenario continuously generate vehicles around the traffic circle, you must also run the `remove_actors.py` script at the same time as `Event4.py`. This can be done before or after you run the Event4 script, but after the Carla server has been created.

```bash
python Scripts/remove_actors.py
```

---

### Release notes
#### 0.1
- Creates a utilities library which provides several useful utility functions that can be used throughout your Carla client script.
- Adds a Scripts directory for holding various scripts that can be used for testing ego vehicle implementations. Specifically,
  - Event4.py: Used for running an initial scenario for the fourth event.
  - remove_actors.py: Used for removing vehicles from the Carla server that are no longer within 100 meters of the traffic circle in Town03.

---

>##### Notes for users and contributors:
>  - ###### The repository will follow the [GitFlow workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
>  - ###### When making a commit, try to make commits small and related to a specific issue. Tense should be present and be written as if the commit is telling you what it is doing. Include the related issue in the summary as well. E.g. Issue #12: Adds a function for handling string comparisons.
>  - ###### When creating a new issue, please be as specific as possible. For bugs, list as many details as possible, including how to reproduce the bug, errors you receive, the expected results, your actual results, etc. For feature requests, provide a precise summary, add a detailed description of the request, be concise, if you can, propose a solution, etc.