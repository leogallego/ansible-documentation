# validate-modules

Analyze modules for common issues in code and documentation.

## Usage

``` shell
cd /path/to/ansible/source
source hacking/env-setup
ansible-test sanity --test validate-modules
```

## Help

Type `ansible-test sanity --test validate-modules -h` to display help for using this sanity test.

## Extending validate-modules

The `validate-modules` tool has a [schema.py](https://github.com/ansible/ansible/blob/devel/test/lib/ansible_test/_util/controller/sanity/validate-modules/validate_modules/schema.py) that is used to validate the YAML blocks, such as `DOCUMENTATION` and `RETURNS`.

## Codes

<table>
<thead>
<tr class="header">
<th><strong>Error Code</strong></th>
<th><strong>Type</strong></th>
<th><strong>Level</strong></th>
<th><strong>Sample Message</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><blockquote>
<p>ansible-deprecated-module</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>A module is deprecated and supposed to be removed in the current or an earlier Ansible version</td>
</tr>
<tr class="even">
<td><blockquote>
<p>collection-deprecated-module</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>A module is deprecated and supposed to be removed in the current or an earlier collection version</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>ansible-deprecated-version</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>A feature is deprecated and supposed to be removed in the current or an earlier Ansible version</td>
</tr>
<tr class="even">
<td><blockquote>
<p>ansible-module-not-initialized</p>
</blockquote></td>
<td>Syntax</td>
<td>Error</td>
<td>Execution of the module did not result in initialization of AnsibleModule</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>collection-deprecated-version</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>A feature is deprecated and supposed to be removed in the current or an earlier collection version</td>
</tr>
<tr class="even">
<td><blockquote>
<p>deprecated-date</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>A date before today appears as <code>removed_at_date</code> or in <code>deprecated_aliases</code></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>deprecation-mismatch</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Module marked as deprecated or removed in at least one of the file name, its metadata, or in DOCUMENTATION (setting DOCUMENTATION.deprecated for deprecation or removing all Documentation for removed) but not in all three places.</td>
</tr>
<tr class="even">
<td><blockquote>
<p>doc-choices-do-not-match-spec</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Value for "choices" from the argument_spec does not match the documentation</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>doc-choices-incompatible-type</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Choices value from the documentation is not compatible with type defined in the argument_spec</td>
</tr>
<tr class="even">
<td><blockquote>
<p>doc-default-does-not-match-spec</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Value for "default" from the argument_spec does not match the documentation</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>doc-default-incompatible-type</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Default value from the documentation is not compatible with type defined in the argument_spec</td>
</tr>
<tr class="even">
<td><blockquote>
<p>doc-elements-invalid</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Documentation specifies elements for argument, when "type" is not <code>list</code>.</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>doc-elements-mismatch</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Argument_spec defines elements different than documentation does</td>
</tr>
<tr class="even">
<td><blockquote>
<p>doc-missing-type</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Documentation doesn't specify a type but argument in <code>argument_spec</code> use default type (<code>str</code>)</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>doc-required-mismatch</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>argument in argument_spec is required but documentation says it is not, or vice versa</td>
</tr>
<tr class="even">
<td><blockquote>
<p>doc-type-does-not-match-spec</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Argument_spec defines type different than documentation does</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>documentation-error</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Unknown <code>DOCUMENTATION</code> error</td>
</tr>
<tr class="even">
<td><blockquote>
<p>documentation-syntax-error</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Invalid <code>DOCUMENTATION</code> schema</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>import-before-documentation</p>
</blockquote></td>
<td>Imports</td>
<td>Error</td>
<td>Import found before documentation variables. All imports must appear below <code>DOCUMENTATION</code>/<code>EXAMPLES</code>/<code>RETURN</code></td>
</tr>
<tr class="even">
<td><blockquote>
<p>import-error</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td><code>Exception</code> attempting to import module for <code>argument_spec</code> introspection</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>attributes-check-mode</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>If a module documents the <code>check_mode</code> attribute, its <code>support</code> value must be compatible with the <code>supports_check_mode</code> parameter of <code>AnsibleModule</code></td>
</tr>
<tr class="even">
<td><blockquote>
<p>attributes-check-mode-details</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>If a module documents the <code>check_mode</code> attribute with support values <code>partial</code> or <code>N/A</code>, it must provide <code>details</code></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>import-placement</p>
</blockquote></td>
<td>Locations</td>
<td>Warning</td>
<td>Imports should be directly below <code>DOCUMENTATION</code>/<code>EXAMPLES</code>/<code>RETURN</code></td>
</tr>
<tr class="even">
<td><blockquote>
<p>imports-improper-location</p>
</blockquote></td>
<td>Imports</td>
<td>Error</td>
<td>Imports should be directly below <code>DOCUMENTATION</code>/<code>EXAMPLES</code>/<code>RETURN</code></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>incompatible-choices</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Choices value from the argument_spec is not compatible with type defined in the argument_spec</td>
</tr>
<tr class="even">
<td><blockquote>
<p>incompatible-default-type</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Default value from the argument_spec is not compatible with type defined in the argument_spec</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>invalid-argument-name</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Argument in argument_spec must not be one of 'message', 'syslog_facility' as it is used internally by Ansible Core Engine</td>
</tr>
<tr class="even">
<td><blockquote>
<p>invalid-argument-spec</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Argument in argument_spec must be a dictionary/hash when used</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>invalid-argument-spec-options</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Suboptions in argument_spec are invalid</td>
</tr>
<tr class="even">
<td><blockquote>
<p>invalid-documentation</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td><code>DOCUMENTATION</code> is not valid YAML</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>invalid-documentation-markup</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td><code>DOCUMENTATION</code> or <code>RETURN</code> contains invalid markup</td>
</tr>
<tr class="even">
<td><blockquote>
<p>invalid-documentation-options</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td><code>DOCUMENTATION.options</code> must be a dictionary/hash when used</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>invalid-examples</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td><code>EXAMPLES</code> is not valid YAML</td>
</tr>
<tr class="even">
<td><blockquote>
<p>invalid-extension</p>
</blockquote></td>
<td>Naming</td>
<td>Error</td>
<td>Official Ansible modules must have a <code>.py</code> extension for python modules or a <code>.ps1</code> for powershell modules</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>invalid-module-schema</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td><code>AnsibleModule</code> schema validation error</td>
</tr>
<tr class="even">
<td><blockquote>
<p>invalid-removal-version</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>The version at which a feature is supposed to be removed cannot be parsed (for collections, it must be a <a href="https://semver.org/">semantic version</a>)</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>invalid-requires-extension</p>
</blockquote></td>
<td>Naming</td>
<td>Error</td>
<td>Module <code>#AnsibleRequires -CSharpUtil</code> should not end in .cs, Module <code>#Requires</code> should not end in .psm1</td>
</tr>
<tr class="even">
<td><blockquote>
<p>missing-doc-fragment</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td><code>DOCUMENTATION</code> fragment missing</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>missing-existing-doc-fragment</p>
</blockquote></td>
<td>Documentation</td>
<td>Warning</td>
<td>Pre-existing <code>DOCUMENTATION</code> fragment missing</td>
</tr>
<tr class="even">
<td><blockquote>
<p>missing-documentation</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>No <code>DOCUMENTATION</code> provided</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>missing-examples</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>No <code>EXAMPLES</code> provided</td>
</tr>
<tr class="even">
<td><blockquote>
<p>missing-gplv3-license</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>GPLv3 license header not found</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>missing-module-utils-basic-import</p>
</blockquote></td>
<td>Imports</td>
<td>Warning</td>
<td>Did not find <code>ansible.module_utils.basic</code> import</td>
</tr>
<tr class="even">
<td><blockquote>
<p>missing-module-utils-import-csharp-requirements</p>
</blockquote></td>
<td>Imports</td>
<td>Error</td>
<td>No <code>Ansible.ModuleUtils</code> or C# Ansible util requirements/imports found</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>missing-powershell-interpreter</p>
</blockquote></td>
<td>Syntax</td>
<td>Error</td>
<td>Interpreter line is not <code>#!powershell</code></td>
</tr>
<tr class="even">
<td><blockquote>
<p>missing-python-interpreter</p>
</blockquote></td>
<td>Syntax</td>
<td>Error</td>
<td>Interpreter line is not <code>#!/usr/bin/python</code></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>missing-return</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>No <code>RETURN</code> documentation provided</td>
</tr>
<tr class="even">
<td><blockquote>
<p>missing-return-legacy</p>
</blockquote></td>
<td>Documentation</td>
<td>Warning</td>
<td>No <code>RETURN</code> documentation provided for legacy module</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>missing-suboption-docs</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Argument in argument_spec has sub-options but documentation does not define sub-options</td>
</tr>
<tr class="even">
<td><blockquote>
<p>module-incorrect-version-added</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Module level <code>version_added</code> is incorrect</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>module-invalid-version-added</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Module level <code>version_added</code> is not a valid version number</td>
</tr>
<tr class="even">
<td><blockquote>
<p>module-utils-specific-import</p>
</blockquote></td>
<td>Imports</td>
<td>Error</td>
<td><code>module_utils</code> imports should import specific components, not <code>*</code></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>multiple-utils-per-requires</p>
</blockquote></td>
<td>Imports</td>
<td>Error</td>
<td><code>Ansible.ModuleUtils</code> requirements do not support multiple modules per statement</td>
</tr>
<tr class="even">
<td><blockquote>
<p>multiple-csharp-utils-per-requires</p>
</blockquote></td>
<td>Imports</td>
<td>Error</td>
<td>Ansible C# util requirements do not support multiple utils per statement</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>no-default-for-required-parameter</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Option is marked as required but specifies a default. Arguments with a default should not be marked as required</td>
</tr>
<tr class="even">
<td><blockquote>
<p>no-log-needed</p>
</blockquote></td>
<td>Parameters</td>
<td>Error</td>
<td>Option name suggests that the option contains a secret value, while <code>no_log</code> is not specified for this option in the argument spec. If this is a false positive, explicitly set <code>no_log=False</code></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>nonexistent-parameter-documented</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Argument is listed in DOCUMENTATION.options, but not accepted by the module</td>
</tr>
<tr class="even">
<td><blockquote>
<p>option-incorrect-version-added</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td><code>version_added</code> for new option is incorrect</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>option-invalid-version-added</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td><code>version_added</code> for option is not a valid version number</td>
</tr>
<tr class="even">
<td><blockquote>
<p>parameter-invalid</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Argument in argument_spec is not a valid python identifier</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>parameter-invalid-elements</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Value for "elements" is valid only when value of "type" is <code>list</code></td>
</tr>
<tr class="even">
<td><blockquote>
<p>implied-parameter-type-mismatch</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Argument_spec implies <code>type="str"</code> but documentation defines it as different data type</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>parameter-type-not-in-doc</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Type value is defined in <code>argument_spec</code> but documentation doesn't specify a type</td>
</tr>
<tr class="even">
<td><blockquote>
<p>parameter-alias-repeated</p>
</blockquote></td>
<td>Parameters</td>
<td>Error</td>
<td>argument in argument_spec has at least one alias specified multiple times in aliases</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>parameter-alias-self</p>
</blockquote></td>
<td>Parameters</td>
<td>Error</td>
<td>argument in argument_spec is specified as its own alias</td>
</tr>
<tr class="even">
<td><blockquote>
<p>parameter-documented-multiple-times</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>argument in argument_spec with aliases is documented multiple times</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>parameter-list-no-elements</p>
</blockquote></td>
<td>Parameters</td>
<td>Error</td>
<td>argument in argument_spec "type" is specified as <code>list</code> without defining "elements"</td>
</tr>
<tr class="even">
<td><blockquote>
<p>parameter-state-invalid-choice</p>
</blockquote></td>
<td>Parameters</td>
<td>Error</td>
<td>Argument <code>state</code> includes <code>get</code>, <code>list</code> or <code>info</code> as a choice. Functionality should be in an <code>_info</code> or (if further conditions apply) <code>_facts</code> module.</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>python-syntax-error</p>
</blockquote></td>
<td>Syntax</td>
<td>Error</td>
<td>Python <code>SyntaxError</code> while parsing module</td>
</tr>
<tr class="even">
<td><blockquote>
<p>removal-version-must-be-major</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>According to the semantic versioning specification (<a href="https://semver.org/">https://semver.org/</a>), the only versions in which features are allowed to be removed are major versions (x.0.0)</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>return-syntax-error</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td><code>RETURN</code> is not valid YAML, <code>RETURN</code> fragments missing or invalid</td>
</tr>
<tr class="even">
<td><blockquote>
<p>return-invalid-version-added</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td><code>version_added</code> for return value is not a valid version number</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>subdirectory-missing-init</p>
</blockquote></td>
<td>Naming</td>
<td>Error</td>
<td>Ansible module subdirectories must contain an <code>__init__.py</code></td>
</tr>
<tr class="even">
<td><blockquote>
<p>try-except-missing-has</p>
</blockquote></td>
<td>Imports</td>
<td>Warning</td>
<td>Try/Except <code>HAS_</code> expression missing</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>undocumented-parameter</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>Argument is listed in the argument_spec, but not documented in the module</td>
</tr>
<tr class="even">
<td><blockquote>
<p>unidiomatic-typecheck</p>
</blockquote></td>
<td>Syntax</td>
<td>Error</td>
<td>Type comparison using <code>type()</code> found. Use <code>isinstance()</code> instead</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>unknown-doc-fragment</p>
</blockquote></td>
<td>Documentation</td>
<td>Warning</td>
<td>Unknown pre-existing <code>DOCUMENTATION</code> error</td>
</tr>
<tr class="even">
<td><blockquote>
<p>use-boto3</p>
</blockquote></td>
<td>Imports</td>
<td>Error</td>
<td><code>boto</code> import found, new modules should use <code>boto3</code></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>use-fail-json-not-sys-exit</p>
</blockquote></td>
<td>Imports</td>
<td>Error</td>
<td><code>sys.exit()</code> call found. Should be <code>exit_json</code>/<code>fail_json</code></td>
</tr>
<tr class="even">
<td><blockquote>
<p>use-module-utils-urls</p>
</blockquote></td>
<td>Imports</td>
<td>Error</td>
<td><code>requests</code> import found, should use <code>ansible.module_utils.urls</code> instead</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>use-run-command-not-os-call</p>
</blockquote></td>
<td>Imports</td>
<td>Error</td>
<td><code>os.call</code> used instead of <code>module.run_command</code></td>
</tr>
<tr class="even">
<td><blockquote>
<p>use-run-command-not-popen</p>
</blockquote></td>
<td>Imports</td>
<td>Error</td>
<td><code>subprocess.Popen</code> used instead of <code>module.run_command</code></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>use-short-gplv3-license</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>GPLv3 license header should be the short form for new modules</td>
</tr>
<tr class="even">
<td><blockquote>
<p>mutually_exclusive-type</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>mutually_exclusive entry contains non-string value</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>mutually_exclusive-collision</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>mutually_exclusive entry has repeated terms</td>
</tr>
<tr class="even">
<td><blockquote>
<p>mutually_exclusive-unknown</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>mutually_exclusive entry contains option which does not appear in argument_spec (potentially an alias of an option?)</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>required_one_of-type</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>required_one_of entry contains non-string value</td>
</tr>
<tr class="even">
<td><blockquote>
<p>required_one_of-collision</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>required_one_of entry has repeated terms</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>required_one_of-unknown</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>required_one_of entry contains option which does not appear in argument_spec (potentially an alias of an option?)</td>
</tr>
<tr class="even">
<td><blockquote>
<p>required_together-type</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>required_together entry contains non-string value</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>required_together-collision</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>required_together entry has repeated terms</td>
</tr>
<tr class="even">
<td><blockquote>
<p>required_together-unknown</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>required_together entry contains option which does not appear in argument_spec (potentially an alias of an option?)</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>required_if-is_one_of-type</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>required_if entry has a fourth value which is not a bool</td>
</tr>
<tr class="even">
<td><blockquote>
<p>required_if-requirements-type</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>required_if entry has a third value (requirements) which is not a list or tuple</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>required_if-requirements-collision</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>required_if entry has repeated terms in requirements</td>
</tr>
<tr class="even">
<td><blockquote>
<p>required_if-requirements-unknown</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>required_if entry's requirements contains option which does not appear in argument_spec (potentially an alias of an option?)</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>required_if-unknown-key</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>required_if entry's key does not appear in argument_spec (potentially an alias of an option?)</td>
</tr>
<tr class="even">
<td><blockquote>
<p>required_if-key-in-requirements</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>required_if entry contains its key in requirements list/tuple</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>required_if-value-type</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>required_if entry's value is not of the type specified for its key</td>
</tr>
<tr class="even">
<td><blockquote>
<p>required_by-collision</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>required_by entry has repeated terms</td>
</tr>
<tr class="odd">
<td><blockquote>
<p>required_by-unknown</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>required_by entry contains option which does not appear in argument_spec (potentially an alias of an option?)</td>
</tr>
<tr class="even">
<td><blockquote>
<p>version-added-must-be-major-or-minor</p>
</blockquote></td>
<td>Documentation</td>
<td>Error</td>
<td>According to the semantic versioning specification (<a href="https://semver.org/">https://semver.org/</a>), the only versions in which features are allowed to be added are major and minor versions (x.y.0)</td>
</tr>
</tbody>
</table>
