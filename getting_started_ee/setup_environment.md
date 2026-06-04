# Setting up your environment

Complete the following steps to set up a local environment for your first Execution Environment:

1.  Ensure the following packages are installed on your system:

    > - `podman` or `docker`
    > - `python3`
    > - `python3-pip`
    >
    > If you use the DNF package manager, install these prerequisites as follows:
    >
    > ``` bash
    > sudo dnf install -y podman python3 python3-pip
    > ```

2.  Install `ansible-navigator`:

    > ``` bash
    > pip3 install ansible-navigator
    > ```
    >
    > Installing `ansible-navigator` lets you run EEs on the command line. It includes the `ansible-builder` package to build EEs.
    >
    > If you want to build EEs without testing, install only `ansible-builder`:
    >
    > ``` bash
    > pip3 install ansible-builder
    > ```

3.  Verify your environment with the following commands:

    > ``` bash
    > ansible-navigator --version
    > ansible-builder --version
    > ```

Ready to build an EE in a few easy steps? Proceed to building_execution_environment.

Want to try an EE without having to build one? Proceed to running_community_execution_environment.
