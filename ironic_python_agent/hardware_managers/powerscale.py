# Copyright 2016 Mellanox Technologies, Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import psutil
import socket

from oslo_log import log

from ironic_python_agent import errors
from ironic_python_agent import hardware
from ironic_python_agent import netutils

LOG = log.getLogger()


class DellPowerScaleHardwareManager(hardware.HardwareManager):
    """Mellanox hardware manager to support a single device"""

    HARDWARE_MANAGER_NAME = 'DellPowerScaleHardwareManager'
    HARDWARE_MANAGER_VERSION = '1.0'

    def evaluate_hardware_support(self):
        """Declare level of hardware support provided."""

        return hardware.HardwareSupport.MAINLINE

    def list_network_interfaces(self):
        network_interfaces_list = []
        for ifname, snics in psutil.net_if_addrs().items():
            mac = ipv4 = None
            for snic in snics:
                if snic.family == psutil.AF_LINK:
                    mac = snic.address
                if snic.family == socket.AF_INET:
                    ipv4 = snic.address
            if mac is not None:
                network_interfaces_list.append(
                    hardware.NetworkInterface(ifname, mac,
                        ipv4_address=ipv4,
                        ipv6_address=None,
                        has_carrier=True,
                        vendor="Dell",
                        product="Nic"
                        biosdevname="Nic")

        return network_interfaces_list

    def get_deploy_steps(self, node, ports):
        return [
            {
                'step': 'write_image',
                'priority': 0,
                'interface': 'deploy',
                'reboot_requested': False,
            },
        ]

    def write_image(self, node, ports, image_info, configdrive=None):
        """A deploy step to write an image.

        Downloads and writes an image to disk if necessary. Also writes a
        configdrive to disk if the configdrive parameter is specified.

        :param node: A dictionary of the node object
        :param ports: A list of dictionaries containing information
                      of ports for the node
        :param image_info: Image information dictionary.
        :param configdrive: A string containing the location of the config
                            drive as a URL OR the contents (as gzip/base64)
                            of the configdrive. Optional, defaults to None.
        """
        ext = ext_base.get_extension('standby')
        cmd = ext.prepare_image(image_info=image_info, configdrive=configdrive)
        # The result is asynchronous, wait here.
        return cmd.wait()
