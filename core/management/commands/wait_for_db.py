import time

from MySQLdb import OperationalError as MySQLdbOpError

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    """
    Django command to wait for database.
    """

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write("\nWaiting for database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (MySQLdbOpError, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
