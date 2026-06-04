# Glossary

The following is a list (and re-explanation) of term definitions used elsewhere in the Ansible documentation.

Consult the documentation home page for the full documentation and to see the terms in context, but this should be a good resource to check your knowledge of Ansible's components and understand how they fit together. It is something you might wish to read for review or when a term comes up on the Ansible Forum.

Sudo  
Ansible does not require root logins, and since it is daemonless, definitely does not require root level daemons (which can be a security concern in sensitive environments). Ansible can log in and perform many operations wrapped in a sudo command, and can work with both password-less and password-based sudo. Some operations that don't normally work with sudo (like scp file transfer) can be achieved with Ansible's copy, template, and fetch modules while running in sudo mode.

SSH (Native)  
Native OpenSSH as an Ansible transport is specified with `-c ssh` (or a config file, or a keyword in the playbook) and can be useful if wanting to login through Kerberized SSH or using SSH jump hosts, and so on. In 1.2.1, `ssh` will be used by default if the OpenSSH binary on the control machine is sufficiently new. Previously, Ansible selected `paramiko` as a default. Using a client that supports `ControlMaster` and `ControlPersist` is recommended for maximum performance -- if you don't have that and don't need Kerberos, jump hosts, or other features, `paramiko` is a good choice. Ansible will warn you if it doesn't detect ControlMaster/ControlPersist capability.

Tags  
Ansible allows tagging resources in a playbook with arbitrary keywords, and then running only the parts of the playbook that correspond to those keywords. For example, it is possible to have an entire OS configuration, and have certain steps labeled `ntp`, and then run just the `ntp` steps to reconfigure the time server information on a remote host.

Task  
Playbooks exist to run tasks. Tasks combine an action (a module and its arguments) with a name and optionally some other keywords (like looping keywords). Handlers are also tasks, but they are a special kind of task that do not run unless they are notified by name when a task reports an underlying change on a remote system.

Tasks  
A list of Task.

Templates  
Ansible can easily transfer files to remote systems but often it is desirable to substitute variables in other files. Variables may come from the inventory file, Host Vars, Group Vars, or Facts. Templates use the Jinja2 template engine and can also include logical constructs like loops and if statements.

Transport  
Ansible uses `` `Connection Plugins ``\` to define types of available transports. These are simply how Ansible will reach out to managed systems. Transports included are paramiko, ssh (using OpenSSH), and local.

When  
An optional conditional statement attached to a task that is used to determine if the task should run or not. If the expression following the `when:` keyword evaluates to false, the task will be ignored.

Vars (Variables)  
As opposed to Facts, variables are names of values (they can be simple scalar values -- integers, booleans, strings) or complex ones (dictionaries/hashes, lists) that can be used in templates and playbooks. They are declared things, not things that are inferred from the remote system's current state or nature (which is what Facts are).

YAML  
Ansible does not want to force people to write programming language code to automate infrastructure, so Ansible uses YAML to define playbook configuration languages and also variable files. YAML is nice because it has a minimum of syntax and is very clean and easy for people to skim. It is a good data format for configuration files and humans, but also machine readable. Ansible's usage of YAML stemmed from Michael DeHaan's first use of it inside of Cobbler around 2006. YAML is fairly popular in the dynamic language community and the format has libraries available for serialization in many languages (Python, Perl, Ruby, and so on).

