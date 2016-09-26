# future imports
from __future__ import absolute_import
from __future__ import unicode_literals

# stdlib imports
import logging

from mopidy import core

import requests

# third-party imports
import pykka

logger = logging.getLogger(__name__)


class OhHookFrontend(pykka.ThreadingActor, core.CoreListener):

    def __init__(self, config, core):
        super(OhHookFrontend, self).__init__()
        self.OHHook = OHHook(self, core, config)
        
    def playback_state_changed(self, old_state, new_state):
        if new_state == 'playing':
            self.OHHook.send_ohhook(new_state)
        
class OHHook():
    def __init__(self, frontend, core, config):
        self.config = config['ohhook']

    def send_ohhook(self, state):    
        itemName = self.config['itemstart']

        try:
            logger.info('Sending ' + itemName + ' to ' + self.config['openhaburl'])
            response = requests.get(
                self.config['openhaburl'] + '/CMD?' + itemName + '=ON', timeout=2)
        except Exception as e:
            logger.warning('Unable to send ' + str(e))
        else:
            logger.debug('Webhook response: ({0}) {1}'.format(
                response.status_code,
                response.text,
            ))