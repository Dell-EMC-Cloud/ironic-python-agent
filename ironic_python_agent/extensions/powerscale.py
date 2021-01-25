from ironic_python_agent import errors
from ironic_python_agent.extensions import base
from ironic_python_agent import utils
from ironic_python_agent.extensions import standby
from oslo_concurrency import processutils
from oslo_config import cfg
from oslo_log import log

#CONF = cfg.CONF
LOG = log.getLogger(__name__)


class PowerscaleExtension(standby.StandbyExtension):
    def __init__(self, agent=None):
        """Constructs an instance of StandbyExtension.

        :param agent: An optional IronicPythonAgent object. Defaults to None.
        """
        super(PowerscaleExtension, self).__init__(agent=agent)

    @base.async_command('prepare_image')
    def prepare_image(self,
                      image_info=None,
                      configdrive=None):
        try:
            utils.execute('/root/bin/reimage.sh', image_info['urls'][0], configdrive)
        except processutils.ProcessExecutionError as e:
            raise errors.ImageWriteError('/tmp/', e.exit_code, e.stdout, e.stderr)

        msg = 'image ({}) written to directory /tmp/ '.format(image_info['urls'][0]) 
        LOG.info(msg)
        return msg
