orphan  

# Sanity Tests

Sanity tests are made up of scripts and tools used to perform static code analysis. The primary purpose of these tests is to enforce Ansible coding standards and requirements.

Tests are run with `ansible-test sanity`. All available tests are run unless the `--test` option is used.

## Set up your environment

1.  Install ansible-core that provides the `ansible-test` tool.

> - If you want to run checks available in the development version of `ansible-core`, install it from source code.
>   - Run `source hacking/env-setup` from its source code directory in the same terminal session you run your tests.

2.  Install `podman` or `docker` to avoid installing all the dependencies on your system.
3.  If you test files in a collection:

> - Ensure you have your collection installed in the following path in your home directory: `~/ansible_collections/<NAMESPACE>/<COLLECTION_NAME>`. For instance, in case of the `community.general` collection, it will be `~/ansible_collections/community/general`
> - If your collection is hosted on a remote server such as GitHub, clone it to that path as follows: `git clone <COLLECTION_REPO_URL> ~/ansible_collections/<NAMESPACE>/<COLLECTION_NAME>`

## How to run

To run sanity tests using podman or docker, always use the default docker image by passing the `--docker` argument without specifying the image name.

1.  When testing files in a collection, change your location to your collection directory you created while setting up your environment:

``` shell
cd ~/ansible_collections/<NAMESPACE>/<COLLECTION_NAME>
```

2.  To run all sanity tests in a container:

``` shell
ansible-test sanity --docker
```

- To run a specific test, add the `--test <NAME>` argument, for example, `--test validate-modules`.
  - To list available tests, run: `ansible-test sanity --list-tests`
- To include disabled tests, add the `--allow-disabled` argument.

## Available Tests

See the full list of sanity tests, which also details how to fix identified issues.
