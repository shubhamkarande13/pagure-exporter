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


import sys

from protop2g.conf import standard
from protop2g.view.dcrt import failure, general, section, success, warning
from protop2g.work.tkts import MoveTkts


def showtkts():
    moveobjc = MoveTkts()
    section("Attempting source namespace issue ticket count...")
    warning(
        f"Extracting {'only ' if standard.tktstate == 'open' or standard.tktstate == 'closed' else ''}{standard.tktstate} issue tickets {'with' if standard.movetags else 'without'} labels from the source namespace to the destination namespace"
    )
    warning(
        f"Transferring {'all' if standard.movecmts else 'no'} comments from the source namespace to the destination namespace"
    )
    qantrslt = moveobjc.getcount()
    if qantrslt[0] == 200:
        general(
            f"Found {standard.tktcount} issue ticket(s) across {standard.pageqant} page(s) in {qantrslt[2]} second(s)"
        )
        for indx in range(standard.pageqant):
            section(
                f"Reading issue tickets information (Page {indx + 1} of {standard.pageqant})..."
            )
            pagerslt = moveobjc.iterpage(indx + 1)
            if pagerslt[0] == 200:
                general(
                    f"Found {len(standard.pagerslt)} issue ticket(s) on this page in {pagerslt[2]} second(s)"
                )
                for jndx in standard.pagerslt:
                    issurslt = moveobjc.itertkts(jndx)
                    section(
                        f"Migrating issue ticket {'with' if standard.movetags else 'without'} labels #{standard.issuiden} '{standard.issuname}' by '{standard.authname} (ID {standard.authorid})'..."
                    )
                    if issurslt[0] == 201:
                        general(f"Migrated to {issurslt[1]} in {issurslt[2]} second(s)")
                        if standard.movecmts:
                            section("Reading comment information...")
                            standard.issucmts = jndx["comments"]
                            general(f"Found {len(standard.issucmts)} entities in 0.00 second(s)")
                            for kndx in standard.issucmts:
                                cmtsrslt = moveobjc.itercmts(kndx)
                                section(
                                    f"Transferring comment (Entity {standard.cmtsqant} of {len(standard.issucmts)})..."
                                )
                                if cmtsrslt[0] == 201:
                                    general(
                                        f"Transferred to {cmtsrslt[1]} in {cmtsrslt[2]} second(s)"
                                    )
                                else:
                                    failure("Comment transfer failed!")
                                    general(
                                        f"Failed due to code '{cmtsrslt[0]}' and reason '{cmtsrslt[1]}' in {cmtsrslt[2]} second(s)"
                                    )
                                    sys.exit(1)
                            standard.cmtsqant = 0
                    else:
                        failure("Issue ticket migration failed!")
                        general(
                            f"Failed due to code '{issurslt[0]}' and reason '{issurslt[1]}' in {issurslt[2]} second(s)"
                        )
                        sys.exit(1)
            else:
                failure("Issue ticket information reading failed!")
                general(
                    f"Failed due to code '{pagerslt[0]}' and reason '{pagerslt[1]}' in {pagerslt[2]} second(s)"
                )
                sys.exit(1)
        success("Namespace assets transferring queue processed!")
        general(f"{standard.issutnfs} issue ticket(s) transferred")
        sys.exit(0)
    else:
        failure("Source namespace issue ticket count failed!")
        general(
            f"Failed due to code '{qantrslt[0]}' and reason '{qantrslt[1]}' in {qantrslt[2]} second(s)"
        )
        sys.exit(1)
