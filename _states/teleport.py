# -*- coding: utf-8 -*-
'''
:maintainer:    Erik Kristensen <erik@erikkristensen.com>
:maturity:      new
:depends:       python-requests
:platform:      all

Interact with Gravitational Teleport
'''
import logging

import salt.crypt
import salt.exceptions

log = logging.getLogger(__name__)

def __virtual__():
    '''
    Only load if tctl exists on the system
    '''
    if salt.utils.which('tctl') is None:
        return (False, 'The tctl execution module cannot be loaded: tctl unavailable.')
    else:
        return True

def user_present(name, local_logins=None):
    if __salt__['teleport.users_exists'](name) == True:
        ret = {
            'name': name,
            'changes': None,
            'result': True,
            'comment': 'User is present'
        }
    else:
        teleport_user = __salt__['teleport.users_add'](name, local_logins)
        if teleport_user['result'] == True:
            ret = {
                'name': name,
                'changes': {
                    name: {
                        'old': '',
                        'new': {
                            'login': teleport_user['login'],
                            'local_logins': teleport_user['local_logins']
                        }
                    }
                },
                'result': True,
                'comment': 'User was added successfully'
            }
        else:
            ret = {
                'name': name,
                'changes': None,
                'result': False,
                'comment': 'Error adding or verifying presence of user'
            }

    return ret

def user_absent(name):
    if __salt__['teleport.users_exists'](name) == False:
        ret = {
            'name': name,
            'changes': None,
            'result': True,
            'comment': 'User is NOT present'
        }
    else:
        ret = {
            'name': name,
            'changes': None,
            'result': False,
            'comment': 'Error removing the user'
        }

        teleport_user = __salt__['teleport.users_del'](name)
        if teleport_user['result'] == True:
            ret = {
                'name': name,
                'changes': {
                    name: {
                        'old': {
                            'login': teleport_user['login']
                        },
                        'new': ''
                    }
                },
                'result': True,
                'comment': 'User was removed successfully'
            }

    return ret
