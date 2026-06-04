# Running integration tests

In the following examples, we will use `Docker` to run integration tests locally. Ensure you collection_prepare_environment first.

We assume that you are in the `~/ansible_collections/NAMESPACE/COLLECTION` directory.

After you change the tests, you can run them with the following command:

``` text
ansible-test integration <target_name> --docker <distro>
```

The `target_name` is a test role directory containing the tests. For example, if the test files you changed are stored in the `tests/integration/targets/postgresql_info/` directory and you want to use the `fedora34` container image, then the command will be:

``` bash
ansible-test integration postgresql_info --docker fedora
```

You can use the `-vv` or `-vvv` argument if you need more detailed output.

In the examples above, the `fedora34` test image will be automatically downloaded and used to create and run a test container.

See the list of supported container images.

In some cases, for example, for platform-independent tests, the `default` test image is required. Use the `--docker default` or just `--docker` option without specifying a distribution in this case.

If you have any difficulties with writing or running integration tests or you are not sure if the case can be covered, submit your pull request without the tests. Other contributors can help you with them later if needed.

