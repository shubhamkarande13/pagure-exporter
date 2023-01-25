"""
protop2g
Copyright (C) 2022-2023 Akashdeep Dhar

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Any Red Hat trademarks that are incorporated in the source
code or documentation are not subject to the GNU General Public
License and may only be used or replicated with the express permission
of Red Hat, Inc.
"""


from protop2g.work.rqst import SrceData, DestData
from protop2g.view.dcrt import success, failure, section, general
from protop2g.conf import standard
from time import strftime, localtime
import sys


def showstat():
    section("REQUESTING FOR SOURCE NAMESPACE METADATA...")
    srcerslt = SrceData().obtninfo()
    if srcerslt == (200, "OK"):
        success("SOURCE NAMESPACE METADATA ACQUISITION SUCCEEDED!")
        general("Name: %s" % str(standard.srcedict["reponame"]))
        general("Identifier: %s" % str(standard.srcedict["identity"]))
        general("Maintainer: %s (ID %s)" % (str(standard.srcedict["maintain"]["fullname"]), str(standard.srcedict["maintain"]["username"])))
        general("Location: %s" % str(standard.srcedict["repolink"]))
        general("Address: %s" % str(standard.srcehuto))
        general("Created on: %s" %  strftime("%c", localtime(int(standard.srcedict["makedate"]))))
        general("Last modified on: %s" % strftime("%c", localtime(int(standard.srcedict["lastmode"]))))
        general("Tags: %s" % str(standard.srcedict["tagslist"]))
        destrslt = DestData().obtninfo()
        section("REQUESTING FOR DESTINATION NAMESPACE METADATA...")
        if destrslt == (200, "OK"):
            success("DESTINATION NAMESPACE METADATA ACQUISITION SUCCEEDED!")
            general("Name: %s" % str(standard.destdict["reponame"]))
            general("Identifier: %s" % str(standard.destdict["identity"]))
            general("Maintainer: %s (ID %s)" % (str(standard.destdict["maintain"]["fullname"]), str(standard.destdict["maintain"]["username"])))
            general("Location: %s" % str(standard.destdict["repolink"]))
            general("Address: %s" % str(standard.desthuto))
            general("Created on: %s" % str(standard.destdict["makedate"]))
            general("Last modified on: %s" % str(standard.destdict["lastmode"]))
            general("Tags: %s" % str(standard.destdict["tagslist"]))
        else:
            failure("DESTINATION NAMESPACE METADATA ACQUISITION FAILED!")
            general("The namespace metadata could not be acquired.")
            general("Code: %s" % str(destrslt[0]))
            general("Reason: %s" % str(destrslt[1]))
            sys.exit(1)
    else:
        failure("SOURCE NAMESPACE METADATA ACQUISITION FAILED!")
        general("The namespace metadata could not be acquired.")
        general("Code: %s" % str(srcerslt[0]))
        general("Reason: %s" % str(srcerslt[1]))
        sys.exit(1)
