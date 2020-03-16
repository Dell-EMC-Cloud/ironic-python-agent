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

import copy

from ironic_lib import utils as il_utils

from ironic_python_agent import errors


def get_block_devices_for_raid(block_devices, logical_disks):
    """Get block devices that are involved in the RAID configuration.

    This call does two things:
    * Collect all block devices that are involved in RAID.
    * Update each logical disks with suitable block devices.
    """
    serialized_devs = [dev.serialize() for dev in block_devices]
    # NOTE(dtantsur): we're going to modify the structure, so make a copy
    logical_disks = copy.deepcopy(logical_disks)
    # NOTE(dtantsur): using a list here is less efficient than a set, but
    # allows keeping the original ordering.
    result = []
    for logical_disk in logical_disks:
        if logical_disk.get('physical_disks'):
            matching = []
            for phys_disk in logical_disk['physical_disks']:
                candidates = [
                    dev['name'] for dev in il_utils.find_devices_by_hints(
                        serialized_devs, phys_disk)
                ]
                if not candidates:
                    raise errors.SoftwareRAIDError(
                        "No candidates for physical disk %(hints)s "
                        "from the list %(devices)s"
                        % {'hints': phys_disk, 'devices': serialized_devs})

                try:
                    matching.append(next(x for x in candidates
                                         if x not in matching))
                except StopIteration:
                    raise errors.SoftwareRAIDError(
                        "No candidates left for physical disk %(hints)s "
                        "from the list %(candidates)s after picking "
                        "%(matching)s for previous volumes"
                        % {'hints': phys_disk, 'matching': matching,
                           'candidates': candidates})
        else:
            # This RAID device spans all disks.
            matching = [dev.name for dev in block_devices]

        # Update the result keeping the ordering and avoiding duplicates.
        result.extend(disk for disk in matching if disk not in result)
        logical_disk['block_devices'] = matching

    return result, logical_disks
