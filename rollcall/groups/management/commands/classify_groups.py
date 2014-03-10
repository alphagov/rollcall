from optparse import make_option

from django.core.management.base import NoArgsCommand

from rollcall.groups.models import Group, GroupState


class Command(NoArgsCommand):
    args = 'args'
    help = 'help'

    option_list = NoArgsCommand.option_list + (
        make_option('-n',
                    '--dry-run',
                    action='store_true',
                    dest='dry_run',
                    default=False,
                    help="Don't save changes to the database"),
    )

    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', '1'))

        unknown_groups = Group.objects.filter(state=GroupState.unknown)
        matching_groups = [g for g in unknown_groups if g.is_quad_format]
        for group in matching_groups:
            if verbosity >= 2:
                print "Group %s matches new format" % group.email
            group.state = GroupState.format_one
            if not options['dry_run']:
                group.save()

        if verbosity >= 1:
            if options['dry_run']:
                print "Reclassified %d groups (dry run)" % len(matching_groups)
            else:
                print "Reclassified %d groups" % len(matching_groups)
