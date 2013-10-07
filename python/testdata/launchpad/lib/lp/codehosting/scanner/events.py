# Copyright 2009 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Events generated by the scanner."""

__metaclass__ = type
__all__ = [
    'NewMainlineRevisions',
    'RevisionsRemoved',
    'TipChanged',
    ]


from zope.component.interfaces import (
    implements,
    IObjectEvent,
    ObjectEvent,
    )


class ScannerEvent(ObjectEvent):
    """Base scanner event."""

    def __init__(self, db_branch, bzr_branch):
        """"Construct a scanner event.

        :param db_branch: The database IBranch.
        :param bzr_branch: The Bazaar branch being scanned.
        """
        ObjectEvent.__init__(self, db_branch)
        self.db_branch = db_branch
        self.bzr_branch = bzr_branch


class INewMainlineRevisions(IObjectEvent):
    """A new revision has been found in the branch."""


class NewMainlineRevisions(ScannerEvent):
    """A new revision has been found in the branch."""

    implements(INewMainlineRevisions)

    def __init__(self, db_branch, bzr_branch, bzr_revisions):
        """Construct a `NewRevisions` event.

        :param db_branch: The database branch.
        :param bzr_branch: The Bazaar branch.
        :param db_revision: An `IRevision` for the new revision.
        :param bzr_revision: The new Bazaar revision.
        :param revno: The revision number of the new revision, None if not
            mainline.
        """
        ScannerEvent.__init__(self, db_branch, bzr_branch)
        self.bzr_revisions = bzr_revisions


class ITipChanged(IObjectEvent):
    """The tip of the branch has changed."""


class TipChanged(ScannerEvent):
    """The tip of the branch has changed."""
    implements(ITipChanged)

    def __init__(self, db_branch, bzr_branch, initial_scan):
        """Construct a `TipChanged` event.

        :param db_branch: The database branch.
        :param bzr_branch: The Bazaar branch.
        :param initial_scan: Is this the first scan of the branch?
        """
        ScannerEvent.__init__(self, db_branch, bzr_branch)
        self.initial_scan = initial_scan

    @property
    def old_tip_revision_id(self):
        """The tip revision id from the last scan."""
        return self.db_branch.last_scanned_id

    @property
    def new_tip_revision_id(self):
        """The new tip revision id from this scan."""
        return self.bzr_branch.last_revision()


class IRevisionsRemoved(IObjectEvent):
    """Revisions have been removed from the branch."""


class RevisionsRemoved(ScannerEvent):
    """Revisions have been removed from the branch."""

    implements(IRevisionsRemoved)

    def __init__(self, db_branch, bzr_branch, removed_history):
        """Construct a `RevisionsRemoved` event.

        :param db_branch: The database branch.
        :param bzr_branch: The Bazaar branch.
        :param removed_history: The mainline database `IRevision` objects that
            are no longer present in the mainline of the Bazaar branch.
        """
        ScannerEvent.__init__(self, db_branch, bzr_branch)
        self.removed_history = removed_history


class IScanCompleted(IObjectEvent):
    """The scan has been completed and the database is up-to-date."""


class ScanCompleted(ScannerEvent):
    """The scan has been completed and the database is up-to-date."""

    implements(IScanCompleted)

    def __init__(self, db_branch, bzr_branch, logger, new_ancestry):
        """Construct a `ScanCompleted` event.

        :param db_branch: The database branch.
        :param bzr_branch: The Bazaar branch.
        :param bzr_ancestry: A set of all the revisions -- mainline or
            otherwise -- in the Bazaar branch.
        :param logger: A Python logger object that's used to report incidental
            information, such as merges that we find.
        """
        ScannerEvent.__init__(self, db_branch, bzr_branch)
        self.new_ancestry = new_ancestry
        # This is kind of ick. In a strict Zope sense, the logger should
        # probably be a registered utility.
        self.logger = logger
