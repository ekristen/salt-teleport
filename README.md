[![License: MIT](https://img.shields.io/github/license/mashape/apistatus.svg)](https://opensource.org/licenses/MIT)

# salt-teleport

This is a custom module and state for SaltStack to support Teleport.

It comes with basic user management, absent and present, and the ability to generate a token to join a node using publish.publish!

## Features

### Dynamic Teleport Node Authentication 

This feature allows a minion to use the `publish.publish` feature to request an authentication token from another minion (the teleport auth server) and then populate the teleport.yaml config. From there the service can be started and will register with the teleport auth service.

There are a few checks the `node_authentication_token` function does. First it checks to see if `/var/lib/teleport/auth_token` exists and if the token in there has expired yet. It also checks to see if `/var/lib/teleport/node.key` is present. If the node.key is missing it is assumed that the node has not registered itself with the auth service.

If it determines that it is not authenticated, the module function will run publish.publish to get the token and you can use it to populate a config and trigger any other actions necessary.

## Installation

Copy the `_modules` and the `_states` to your `base` file roots or gitfs repo, then make sure you run `salt '*' saltutil.sync_all`

## Examples

### Dynamic Teleport Node Authentication Token

Template File

```yaml
teleport:
  token: {{ token }}

ssh_service:
  enabled: yes

auth_service:
  enabled: no

proxy_service:
  enabled: no
```

SLS File

```yaml
teleport-config:
  file.managed:
    - name: /etc/teleport.yaml
    - source: salt://config.tmpl
    - template: jinja
    - defaults:
        token: {{ salt['teleport.node_authentication_token']('role:teleport-auth', expr_form='grain') }}
```
