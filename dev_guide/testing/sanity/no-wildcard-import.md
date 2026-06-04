orphan  

# no-wildcard-import

Using `import *` is a bad habit which pollutes your namespace, hinders debugging, and interferes with static analysis of code. For those reasons, we do want to limit the use of `import *` in the ansible code. Change our code to import the specific names that you need instead.

Examples of unfixed code:

``` python
from ansible.module_utils.six import *
if isinstance(variable, string_types):
    do_something(variable)

from ansible.module_utils.basic import *
module = AnsibleModule()
```

Examples of fixed code:

``` python
from ansible.module_utils import six
if isinstance(variable, six.string_types):
    do_something(variable)

from ansible.module_utils.basic import AnsibleModule
module = AnsibleModule()
```
