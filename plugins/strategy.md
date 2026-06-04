# Strategy plugins

Strategy plugins control the flow of play execution by handling task and host scheduling. For more information on using strategy plugins and other ways to control execution order, see playbooks_strategies.

## Enabling strategy plugins

All strategy plugins shipped with Ansible are enabled by default. You can enable a custom strategy plugin by putting it in one of the lookup directory sources configured in ansible.cfg.

## Using strategy plugins

Only one strategy plugin can be used in a play, but you can use different ones for each play in a playbook or ansible run. By default, Ansible uses the linear plugin. You can change this default in Ansible configuration using an environment variable:

``` shell
export ANSIBLE_STRATEGY=free
```

or in the `ansible.cfg` file:

``` ini
[defaults]
strategy=linear
```

You can also specify the strategy plugin in the play with the strategy keyword in a play:

``` yaml
- hosts: all
  strategy: debug
  tasks:
    - copy:
        src: myhosts 
        dest: /etc/hosts
      notify: restart_tomcat

    - package:
        name: tomcat
        state: present

  handlers:
    - name: restart_tomcat
      service:
        name: tomcat
        state: restarted
```

## Plugin list

You can use `ansible-doc -t strategy -l` to see the list of available plugins. Use `ansible-doc -t strategy <plugin name>` to see plugin-specific documentation and examples.
