# Copyright (c) 2023 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from snaphelpers import Snap, SnapCtl

LOG = logging.getLogger(__name__)


class Check:
    """Base class for Pre-flight checks.

    Check performs a verification step to determine
    to proceed further or not.
    """

    def __init__(self, name: str, description: str = ""):
        """Initialise the Check.

        :param name: the name of the check
        """
        self.name = name
        self.description = description
        self.message = None

    def run(self) -> bool:
        """Run the check logic here.

        Return True if check is Ok.
        Otherwise update self.message and return False.
        """

        return True


class JujuSnapCheck(Check):
    """Check if juju snap is installed or not."""

    def __init__(self):
        super().__init__(
            "Check for juju snap",
            "Checking for presence of Juju",
        )

    def run(self) -> bool:
        """Check for juju-bin content."""

        snap = Snap()
        juju_content = snap.paths.snap / "juju"
        if not juju_content.exists():
            self.message = "Juju not detected: please install snap"

            return False

        return True


class SshKeysConnectedCheck(Check):
    """Check if ssh-keys interface is connected or not."""

    def __init__(self):
        super().__init__(
            "Check for ssh-keys interface",
            "Checking for presence of ssh-keys interface",
        )

    def run(self) -> bool:
        """Check for ssh-keys interface."""

        snap = Snap()
        snap_ctl = SnapCtl()
        connect = f"sudo snap connect {snap.name}:ssh-keys"

        if not snap_ctl.is_connected("ssh-keys"):
            self.message = (
                "ssh-keys interface not detected: please connect ssh-keys interface "
                f"by running {connect!r}"
            )
            return False
        return True
