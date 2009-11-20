from django.core.management.base import BaseCommand
from optparse import make_option
import sys
from eve_db.ccp_importer import util
from eve_db.ccp_importer import importers

def exit_with_error(error_msg):
    """
    Gracefully kills the script when an error was occured.
    """
    parser.error(error_msg)
    
def exit_with_succ():
    """
    Nothing to see here, move along.
    """
    sys.exit(0)
    
def list_tables(option, opt, value, parser):
    """
    Prints a list of tables that are available for import.
    """
    print "CCP Data Dump Table List"
    print "------------------------"
    for table in util.IMPORT_LIST:
        print "%s" % table.__name__.replace('import_', '')
    print "-- %d tables --" % len(util.IMPORT_LIST)
    # The -l argument is just used for listing, proceed no further.
    exit_with_succ()
    
def get_importer_classes_from_arg_list(arg_list):
    """
    Validates the user input for tables to import against the importer list.
    Returns a list of importer classes. In the event that one of the
    arguments does not match up against an importer class, raise an
    exception so the user may be notified.
    """
    importer_classes = []
    for arg in arg_list:
        importer_class = getattr(importers, 'Importer_%s' % arg, False)
        if importer_class not in util.IMPORT_LIST:
            exit_with_error("No such table to import: %s" % arg)
        else:
            importer_classes.append(importer_class)
    return importer_classes

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'),
        make_option("-i", "--include-deps", action="store_true",
                          dest="include_deps", default=False,
                          help="""Import the other tables that the specified table 
                                  [recursively] depends on."""),
        make_option("-l", "--list", action="callback",
                          callback=list_tables,
                          help="List all of the tables in the CCP dump and exit."),
    )
    help = """This importer script will either import one or all tables from
the CCP data dump. If no arguments are specified, all tables will be imported."""
    args = '[table_name1] [table_name2] [...]'

    requires_model_validation = False
            
    def handle(self, *args, **options):
        """
        This is where the user input is handled, and the appropriate
        actions are taken.
        """
        print "OPTIONS", options
        print "ARGS:", args
        
        try:
            if len(args) == 0:
                print "No table names specified, importing all."
                util.run_importers(util.IMPORT_LIST)
            else:
                print "Importing: %s" % args
                importers = get_importer_classes_from_arg_list(args)
                util.run_importers(importers)
        except KeyboardInterrupt:
            print "Terminating early..."
            exit_with_succ()