#!/usr/bin/env python3

# File: utils.py

"""
"utils.py" is an utility providing functionality for usage and
maintanance of the Bolinas Rod and Boat Club membership records.
Most commands deal with a csv file named "./Data/memlist.csv" so for
these it is the default input file.
Labels and Envelopes (along with the '-P <params>' option) have
been deprecated but the code left in place incase anyone ever
wishes to revive them.  Current usage replaces them with emails and
letters (which can be prepared using the 'prepare_mailing' command.)
Consult the README file for further info.

Usage:
  ./utils.py [ ? | --help | --version]
  ./utils.py ck_data [-O -d -i <infile> -A <app_spot> -S <sponsors_spot> -X <fees_spot> -C <contacts_spot> -o <outfile>]
  ./utils.py show [-O -i <infile> -A <applicant_spot> -S <sponsors_spot> -o <outfile> ]
  ./utils.py names_only [-O -w <width> -i <infile> -o <outfile> ]
  ./utils.py report [-O -i <infile> -A <applicant_spot> -S <sponsors_spot> -o <outfile> ]
  ./utils.py stati [-O -D -M -B --mode <mode> -i <infile> -A <applicant_spot> -S <sponsors_spot> -o <outfile>]
  ./utils.py zeros [-O -i <infile> -o <outfile]
  ./utils.py usps [-O -i <infile> -o <outfile>]
  ./utils.py extra_charges [-O -w <width> -f <format> -i <infile> -o <outfile> -j <jsonfile>]
  ./utils.py payables [-O -T -w <width> -i <infile> -o <outfile>]
  ./utils.py show_mailing_categories [-O -T -w <width> -o <outfile>]
  ./utils.py prepare_mailing --which <letter> [-O --oo -p <printer> -i <infile> -j <json_file> --dir <mail_dir> --cc <cc> --bcc <bcc> ATTACHMENTS...]
  ./utils.py thank [-t <2thank> -O -p <printer> -i <infile> -j <json_file> --dir <mail_dir> -o <temp_membership_file> -e <error_file>]
  ./utils.py display_emails [-O] -j <json_file> [-o <txt_file>]
  ./utils.py send_emails [-O --mta <mta> --emailer <emailer>] -j <json_file>
  ./utils.py print_letters --dir <mail_dir> [-O --separator <separator> -o outfile]
  ./utils.py emailing [-O -i <infile> -F <muttrc>] --subject <subject> -c <content> [ATTACHMENTS...]
  ./utils.py restore_fees [-O -i <membership_file> -X <fees_spot> -o <temp_membership_file> -e <error_file>]
  ./utils.py fee_intake_totals [-O -i <infile> -o <outfile> -e <error_file>]
  ./utils.py (labels | envelopes) [-O -i <infile> -P <params> -o <outfile> -x <file>]
  ./utils.py wip [-O -o 2check]
  ./utils.py new_db -F function [-O -i <membership_file> -o <new_membership_file> -e <error_file>]

Options:
  -h --help  Print this docstring. Best piped through pager.
  --version  Print version.
  -A <app_spot>  Applicant data file.
  --bcc <bcc>   Comma separated listing of bcc recipients
  --cc <cc>   Comma separated listing of cc recipients
  -c <content>  The name of a file containing the body of an email.
  -C <contacts_spot>  Contacts data file.
  -d   Include details: fee inconsistency for ck_data,
  --dir <mail_dir>  The directory (to be created and/or read)
                    containing letters for batch printing.
  -e <error_file>  Specify name of a file to which an error report
            can be written.  [default: stdout]
  --emailer <emailer>  Use bash (via smtp or mutt) or python to send
                    emails.  [default: python]
  -f <format>  Specify output format of 'extra_charges' command.
        Possible choices are:
            'table' listing of names /w fees tabulated (=> 2 columns.)
            'listing' same format as Data/extra_fees.txt
            'listings' side by side lists (best use landscape mode.)
        [default: table]
  -F <function>  Name of function to apply. (new_db command)
  -i <infile>  Specify file used as input. Usually defaults to
                the MEMBERSHIP_SPoT attribute of the Club class.
  -D   include demographic data  } These pertain
  -M   include meeting dates     } to applicant
  -B   include backers/sponsors  } reports.
  -j <json>  Specify a json formated file (whether for input or output
              depends on context.)
  --mode <mode>   In stati command signals stati to show:
                    If not specified, all stati are reported.
                    | --mode <any string beginning with 'applic'>:
                    only applicants are reported
                    | --mode <member.SEPARATOR separated list of
                    stati>: only report stati listed.
  --mta <mta>  Specify mail transfer agent to use. Choices are:
                clubg     club's gmail account  [default: clubg]
                akg       my gmail account
                easy      my easydns account
  -O  Show Options/commands/arguments.  Used for debugging.
  -o <outfile>  Specify destination. Choices are stdout, printer, or
                the name of a file. [default: stdout]
  --oo   Owing_Only: Only consider members with dues/fees outstanding.
            (Sets owing_only attribute of instance of Club.)
  -P <params>  This option will probably be redacted since old
            methods of mailing are no longer used.
            Defaults are A5160 for labels & E000 for envelopes.
  -p <printer>  Deals with printer variablility; ensures correct
        alignment of text when printing letters. [default: X6505_e1]
  -s <stati>     Report only the stati listed (separated by
            member.SEPARATOR.
  -S <sponsor_SPoL>  Specify file from which to retrieve sponsors.
  --separator <separator>  A string. [default: \f]
  --subject <subject>  The subject line of an email.
  -t <2thank>  A csv file in same format as memlist.csv showing
            recent payments.  Input for thank_cmd.
            [default: Info/2thank.csv]
  -T  Present data in columns (a Table) rather than a long list.
            Used with the 'payables' and 'show_mailing_categories
            command. May not have much effect without setting -w
            to a high number.
  -w <width>  Maximum number of characters per line in output.
                                    [default: 95]
  --which <letter>  Specifies type/subject of mailing.
  -x <file>  Used by commands not in use. (Expect redaction)
  -X <fees_spot>  Extra Fees data file.

Commands:
    When run without a command, suggests ways of getting help.
    ck_data: Checks all the club's data bases for consistency.
        Assumes (user must assert) a fresh export of the gmail
        contacts list. Options:
        | -d  Include fee inconsistencies (which are expected
        when some have paid.)
    show: Returns membership demographics a copy of which can then
        be sent to the web master for display on the web site.
    names_only: Returns a listing of members and applicants- names
        and phone numbers only, without any other demographics.
        If -w is 0, output is a single column, otherwise tabular.
    report: Prepares a 'Membership Report".
    stati: Returns a listing of stati (entries in 'status' field.)
        <mode> if set can be 'applicants' (Applicants only will be
            shown) or a member.SEPARATOR separated set of stati
            (indicating which stati to show.)
        May also include any combination of -D, -M, -S to
        include adress/demographics, meeting dates &/or sponsors
        for applicants.
    usps: Creates a csv file containing names and addresses of
        members without an email address who therefore receive Club
        minutes by post. Also includes any one with a 'be' or an 's'
        status (... a mechanism for sending a copy to the secretary.)
    extra_charges: Reports on members paying extra charges (for
        kayak storage, mooring &/or dock usage.)
        | -f <format>  -specify listing, listings or table format.
        | -w <width>  -specify maxm # of chars per line in output.
        | -j <json_file>  -creat a json file. (This was
        but is no longer required by the restore_fees_cmd.)
    payables: Reports on non zero money fields.
        | -T  Present as a table rather than a listing.
        | -w <width>  Maximum number of characters per line if -T.
    show_mailing_categories: Sends a list of possible entries for the
        '--which' parameter required by the prepare_mailings command.
        (See the 'content_types' dict in content.py.)
    prepare_mailing:  Demands a <--which> argument to specify the
        content and the custom function(s) to be used.  Try the
        'show_mailing_categories' command for a list of choices.
        The command line arguments may end with zero or more names
        of files which are to be added as attachments to the emails.
        Other parameters have defaults set.
        '--oo'  Send request for fee payment only to those with an
        outstanding balance.  This is relevant only to mailings
        relating to dues and fees. Without this option mailings go
        to all members (including those with credit or 0 balance.
        '-p <printer>' specifies printer to be used for letters.
        '-i <infile>' membership data csv file.
        '-j <json_file>' where to dump prepared emails.
        '--dir <mail_dir>' where to file letters.
    thank:  Reads the file specified by -t <thank>, applies payments
        specified there in to the -i <infile> and prepares thank you
        letter/email acknowledging receipt of payment and showing
        current balance(s.) See prepare_mailing command for further
        details.
    display_emails: Provides an opportunity to proof read the emails.
    send_emails: Sends out the emails found in the -j <json_file>.
        Each mta has its own security requirements and each emailer
        has its own way of implementing them. Check the
        Notes/emailREADME for details.  Note that not all
        combinations of mta and emailer are working but the following
        does: "--mta clubg --emailer python".
    within the ./Notes directory (./Notes/msmtprc.)
    print_letters: Sends the files contained in the directory
        specified by the --dir parameter.  Depricated in favour of
        simply using the lpr utility: $ lpr ./Data/MailDir/*
    restore_fees: Use this command to populate each member's record
        with what they will owe for the next club year. Respects any
        existing credits. Best done after all dues and fees have been
        paid. (Will abort if any dues or fees are still outstanding.)
        Results are either placed into a file specified by the '-o'
        option (if provided) or placed into a file named as a
        concatination of "new_" and the input file. One can then
        mannually check the new file and rename it if all is well.
    emailing: Initially developed to allow sending of attachments.
        Since attachments are now possible using the send_mailing
        command (at least with emailer python) this command will
        most likely be redacted.
    fee_intake_totals: Input file should be a 'receipts' file with a
        specific format. It defaults to 'Data/receipts-YYYY.txt'
        where YYYY is the current year.  Output yields subtotals and
        the grand total which can be copy/pasted into the 'receipts'
        file.
    labels: print labels.       | default: -P A5160  | Both
    envelopes: print envelopes. | default: -P E000   | redacted.
    wip: "work in progress" Used for development/testing.
"""

import os
import shutil
import csv
import codecs
import sys
import time
import random
import json
import subprocess
from docopt import docopt
import sys_globals as glbs
import member
import helpers
import content
import data
import Pymail.send
import Bashmail.send
from rbc import Club


TEXT = ".txt"  # } Used by <extra_charges_cmd>
CSV = ".csv"   # } command.

TEMP_FILE = "2print.temp"  # see <output> function

args = docopt(__doc__, version=glbs.VERSION)
for arg in args:
    if type(args[arg]) == str:
        if args[arg] and (args[arg][0] == '='):
            args[arg] = args[arg][1:]
try:
    max_width = int(args['-w'])
except ValueError:
    print(
        "Value of '-w' command line argument must be an integer.")
    sys.exit()
if args['-O']:
    print("Arguments are...")
    res = sorted(["{}: {}".format(key, args[key]) for key in args])
    ret = helpers.tabulate(res, max_width=max_width, separator='   ')
    print('\n'.join(ret))
    response = input("...end of arguments. Continue? ")
    if response and response[0] in 'yY':
        pass
    else:
        sys.exit()

if args["-p"] not in content.printers.keys():
    print("Invalid '-p' parameter! '{}'".format(args['-p']))
    sys.exit()


def assign_default_files(club, args):
    """
    Assigns the following attributes to <club>:
        infile, and the following 'spot' file names:
            applicant_spot, sponsor_spot,
            extra_fees_spot, contacts_spot
    """
    if args['-i']:
        club.infile = args['-i']
    else:
        club.infile = Club.MEMBERSHIP_SPoT
    if args['-A']:
        club.applicant_spot = args['-A']
    else:
        club.applicant_spot = Club.APPLICANT_SPoT
    if args['-S']:
        club.sponsor_spot = args['-S']
    else:
        club.sponsor_spot = Club.SPONSORS_SPoT
    if args['-X']:
        club.extra_fees_spot = args['-X']
    else:
        club.extra_fees_spot = Club.EXTRA_FEES_SPoT
    if args['-C']:
        club.contacts_spot = args['-C']
    else:
        club.contacts_spot = Club.CONTACTS_SPoT


def confirm_file_present_and_up2date(file_name):
    """
    Asks user to confirm that the file is current.
    Aborts the program if file_name doesn't exist.
    Used for the gmail contacts.csv file.
    """
    if not os.path.exists(file_name):
        print("File '{}' expected but not found.".format(file_name))
        sys.exit()
    response = input("Is file '{}' present and up to date? "
                     .format(file_name))
    if response and response[0] in "Yy":
        return True
    else:
        print("Update the file before rerunning utility.")
        sys.exit()


def output(data, destination=args["-o"], announce_write=True):
    """
    Sends data (text) to destination as specified
    by the -o <outfile> command line parameter (which
    defaults to stdout.)
    Reports file manipulations to stdout.
    """
    if destination == 'stdout':
        print(data)
    elif destination == 'printer':
        with open(TEMP_FILE, "w") as fileobj:
            fileobj.write(data)
            print('Data written to temp file "{}".'.format(fileobj.name))
            subprocess.run(["lpr", TEMP_FILE])
            subprocess.run(["rm", TEMP_FILE])
            print('Temp file "{}" deleted after printing.'
                  .format(fileobj.name))
    else:
        with open(destination, "w") as fileobj:
            fileobj.write(data)
            if announce_write:
                print('Data written to "{}".'.format(fileobj.name))


# Medium specific classes:
# e.g. labels, envelopes, ...
# These classes, one for each medium, need never be instantiated.
# They are used only to maintain a set of constants and
# are named beginning with a letter (A - Avery, E - Envelope, ...)
# followed by a 4 digit number: A5160, E0000, ... .
# Clients typically refer to these as <params>.


class Dummy(object):
    """ REDACTED
    a Dummy class for use when templates are not required"""
    formatter = ""

    @classmethod
    def self_check(cls):  # No need for the sanity check in this case
        pass


class E0000(object):
    """
    REDACTED.
    Custom envelopes used by the Bolinas Rod & Boat Club
    to send out requests for dues.
    """
    n_chars_wide = 60
    n_lines_long = 45
    n_labels_page = 1
    n_lines_per_label = 10

    n_chars_per_field = 25
    separation = (34, )
    top_margin = 32

    left_formatter = (" " * separation[0] +
                      "{{:<{}}}".format(n_chars_per_field))
    right_formatter = (" " * separation[0] + "{{:>{}}}"
                       .format(n_chars_per_field))
    empty_line = ""

    @classmethod
    def self_check(cls):
        """
        No need for the sanity check in this case.
        """
        pass


class A5160(object):
    """
    Avery 5160 labels  3 x 10 grid
    zero based:
        1, 28, 56
        3, 9, 15, 21, 27, 33, 39, 45, 51, 57
        (max content 5 lines of 25 characters each)
    Uses "letter size" blanks.
    BUT: there was a complication- my printer "wraps" at 80 chars.
    So each line could not exceed 80 characters.
    """

    # The first two are restrictions imposed by my printer!
    n_chars_wide = 80  # The Avery labels are wider ?84 I think?
    n_lines_long = 64

    n_labels_per_page = 30
    n_labels_per_row = 3
    n_rows_per_page = n_labels_per_page // n_labels_per_row
    n_lines_per_label = 6   # Limits 'spill over' of long lines.

    # Because of the n_chars_wide restriction, can't use the full
    # width of the labels :
    n_chars_per_field = 23
    #             /------left_margin (spaces before 1st field in row)
    #             |  /----between 1st and 2nd
    #             |  |  /--between 2nd & 3rd
    #             |  |  |   # These numbers refer to the room to be
    #             v  v  v   # left before and between the labels.
    separation = (2, 4, 5)
    line_length_needed = 0
    for n in separation:
        line_length_needed += n
    line_length_needed += n_labels_per_row * n_chars_per_field

    top_margin = 2  # The number of blank lines at top of each page.

    empty_label = [""] * n_lines_per_label

    left_formatter = ("{{:<{}}}".format(n_chars_per_field))
    right_formatter = ("{{:>{}}}".format(n_chars_per_field))
    empty_line = left_formatter.format(" ")

    def __init__(self):
        pass

    @classmethod
    def self_check(cls):
        """
        Provides a 'sanity check'.
        """
        if cls.line_length_needed > cls.n_chars_wide:
            print("Label designations are incompatable!")
            sys.exit()


media = dict(  # keep the classes in a dict
             e000=E0000,
             a5160=A5160,
             )


def ck_data_cmd(args=args):
    print("Checking for data consistency...")
    club = Club()
    assign_default_files(club, args)
    confirm_file_present_and_up2date(club.CONTACTS_SPoT)
    output("\n".join(data.ck_data(club, fee_details=args['-d'])))


def show_cmd(args=args):
    club = Club()
    assign_default_files(club, args)
    club.for_web = True
    print("Preparing membership listings...")
    err_code = member.traverse_records(
        club.infile,
        [member.add2lists, ],
        club)
    ret = ["""FOR MEMBER USE ONLY

THE TELEPHONE NUMBERS, ADDRESSES AND EMAIL ADDRESSES OF THE BOLINAS ROD &
BOAT CLUB MEMBERSHIP CONTAINED HEREIN ARE NOT TO BE REPRODUCED OR DISTRIBUTED
FOR ANY PURPOSE WITHOUT THE EXPRESS PERMISSION OF THE BOARD OF THE BRBC.

Data maintained by the Membership Chair and posted here by Secretary {}.
""".format(club.SECRETARY)]

    if club.members:
        helpers.add_header2list("Club Members ({} in number as of {})"
                                .format(club.nmembers, helpers.date),
                                ret, underline_char='=',
                                extra_line=True)
        ret.extend(club.members)
    if club.honorary:
        helpers.add_header2list(
            "Honorary Club Members"
            .format(club.nhonorary, helpers.date),
            ret, underline_char='=', extra_line=True)
        ret.extend(club.honorary)
    if club.by_n_meetings:
        header = ("Applicants ({} in number)"
                  .format(club.napplicants))
        helpers.add_header2list(header, ret, underline_char='=')
        # ####
        club.sponsors = data.get_sponsors(club.sponsor_spot)
        club.meeting_dates = data.get_meeting_dates(
                                    club.applicant_spot)
        ret.extend(member.show_by_status(club.by_n_meetings, club=club))
    output("\n".join(ret))
    print("...results sent to {}.".format(args['-o']))


def names_only_cmd(args=args):
    club = Club()
    assign_default_files(club, args)
    print("Preparing listing of member and applicant names...")
#   print("'-w' is set to {}".format(args['-w']))
    err_code = member.traverse_records(club.infile,
                                       [member.add2names, ],club)
    ret = ["Members and Applicants of the Bolinas Rod & Boat Club",
           "====================================================="]
    if args['-w']:
        club.names = helpers.tabulate(club.names,
                                      max_width=int(args['-w']),
                                      separator=' ')
    ret.extend(club.names)
    output('\n'.join(ret))



def collect_stati_data(club):
    err_code = member.traverse_records(
        club.infile,
        [member.add2stati_by_m,
         member.add2demographics,
         member.add2ms_by_status,
         member.increment_napplicants,
         ],
        club)


def assign_applicant_files(club):
    club.applicant_spot = args['-A']
    if not club.applicant_spot:
        club.applicant_spot = Club.APPLICANT_SPoT
    club.sponsor_file = args['-S']
    if not club.sponsor_file:
        club.sponsor_file = Club.SPONSORS_SPoT


def setup4stati(club):
    club.infile = args["-i"]
    if not club.infile:
        club.infile = Club.MEMBERSHIP_SPoT
    assign_applicant_files(club)
    if not hasattr(club, "include_addresses"):
        club.include_addresses = args['-D']
    if not hasattr(club, "include_dates"):
        club.include_dates = args['-M']
    if not hasattr(club, "include_sponsors"):
        club.include_sponsors = args['-B']
    if not hasattr(club, "which2show"):
        whch2show = args['--mode']  # signals stati to show
    if whch2show:
        if 'applic' in whch2show:
            club.stati2show = set(member.APPLICANT_STATI)
        else:
            club.stati2show = set(whch2show.split(member.SEPARATOR))
    else:
        club.stati2show = set(member.STATI)
    if not club.stati2show.issubset(member.STATI):
        print('Invalid <--mode> parameter provided.')
        sys.exit()
    if club.include_sponsors:
        club.sponsors = data.get_sponsors(club.sponsor_file)
    if club.include_dates:
        club.meeting_dates = data.get_meeting_dates(
                                    club.applicant_spot)


def show_stati(club):
    """
    Returns a list of strings (that can be '\n'.join(ed))
    Assumes existance of following club attributes:
        ms_by_status
            +/- stati2show
        +/- napplicants
        +/- demographics
        +/- meeting_dates
        +/- sponsors
        +/- special_notices_by_m
    See client: stati_cmd() (+/- show_cmd and others?)
    """
    print("Using show_stati function (in utils.py)")
    if not club.ms_by_status:
        return ["Found No Entries with 'Status' Content."]
    ret = []
    applicant_header_written = False
    if hasattr(club, 'stati2show'):
        stati2show = sorted(club.stati2show & club.ms_by_status.keys())
    else:
        stati2show = sorted(club.ms_by_status.keys())
    if hasattr(club, 'special_notices_by_m'):
        special_notice_members = set(club.special_notices_by_m.keys())
    else:
        special_notice_members = None
    for status in stati2show:
        if hasattr(club, 'napplicants'):
            applicant_header = ("Applicants ({} in number)"
                                .format(club.napplicants))
        else:
            applicant_header = "Applicants"
        if status.startswith('a'):
            if not applicant_header_written:
                helpers.add_header2list(
                    applicant_header,
                    ret, underline_char='=')
                applicant_header_written = True
            helpers.add_header2list(member.STATUS_KEY_VALUES[status],
                                    ret, underline_char='-')
            for applicant in sorted(club.ms_by_status[status]):
                if (hasattr(club, 'demographics')
                        and club.include_addresses):
                    ret.append(club.demographics[applicant])
                else:
                    ret.append(applicant)
                if hasattr(club, 'meeting_dates'):
                    if club.meeting_dates[applicant]:
                        ret.append('\tDates(s) attended: {}'.
                                   format(club.meeting_dates[applicant]))
                    # else:
                    #     ret.append('\tNo meetings yet.')
                if hasattr(club, 'sponsors'):
                    ret.append('\tSponsors: {}'.
                               format(club.sponsors[applicant]))
        else:
            helpers.add_header2list(member.STATUS_KEY_VALUES[status],
                                    ret, underline_char='=')
            for status_holder in sorted(club.ms_by_status[status]):
                if hasattr(club, 'demographics'):
                    ret.append(club.demographics[status_holder])
#                   line = (club.demographics[status_holder])
#                   if (special_notice_members and
#                       status_holder in special_notice_members
#                       ):
#                       line = ('{} {}'.format(
#                           line,
#                           club.special_notices_by_m[status_holder]))
#                   ret.append(line)
                else:
                    ret.append(status_holder)
    return ret


def report_cmd(args=args):
    club = Club()
    assign_default_files(club, args=args)
    club.for_web = False
    print("Preparing Membership Report ...")
    err_code = member.traverse_records(
        club.infile,
        [member.add2lists,
         member.add2ms_by_status,
        ],
        club)
    report = []
    helpers.add_header2list("Membership Report (prepared {})"
                            .format(helpers.date),
                            report, underline_char='=')
    report.append('')
    report.append('Club membership currently stands at {}.'
                  .format(club.nmembers))

    if club.by_n_meetings:
        header = ("Applicants ({} in number, "
                  .format(club.napplicants) +
                  "with meeting dates & sponsors listed)")
        helpers.add_header2list(header, report, underline_char='=')
        # ####
        club.sponsors = data.get_sponsors(club.sponsor_spot)
        club.meeting_dates = data.get_meeting_dates(
                                    club.applicant_spot)
        report.extend(member.show_by_status(club.by_n_meetings, club=club))
    if 'r' in club.ms_by_status:
        header = ('Members ({} in number) retiring from the Club:'
                  .format(len(club.ms_by_status['r'])))
        report.append('')
        helpers.add_header2list(header, report, underline_char='=')
        for name in club.ms_by_status['r']:
            report.append(name)

    misc_stati = member.show_by_status(
        club.ms_by_status, stati2show="m|w|be|ba".split('|'))
    if misc_stati:
        header = "Miscelaneous Info"
        helpers.add_header2list(header, report, underline_char='=')
        report.extend(misc_stati)
    redact = '''
    club_ = club_setup4extra_charges()
    club_.presentation_format = 'listings'
    report.append("""


For Docks and Yard Committee
============================

I continue to include the following listing of extra fees
being charged to serve as a reminder to let me know if any
changes are to be made before charges are applied for the
next (July 1, 2021-June 30, 2022) membership year.

""")
    report.extend(data.extra_charges(club_, raw=True))
    '''

    try:
        with open(glbs.DEFAULT_ADDENDUM2REPORT_FILE, 'r') as fobj:
            print('Opening file: {}'.format(fobj.name))
            addendum = fobj.read()
            report.append(addendum)
    except FileNotFoundError:
        print('report.addendum not found')
    report.extend(
        ['', '',
         "Respectfully submitted by...\n\n",
         "Alex Kleider, Membership Chair,",
         "for presentation {}."
         .format(helpers.next_first_friday(exclude=True)),
         ])
    report.extend(
        ['',
         'PS Zoom ID: 527 109 8273; Password: 999620',
        ])
    output("\n".join(report))
    print("...results sent to {}.".format(args['-o']))


def stati_cmd(args=args):
    club = Club()
    collect_stati_data(club)
    setup4stati(club)
    print("Preparing 'Stati' Report ...")
    output('\n'.join(show_stati(club)))


def zeros_cmd(args=args):
    """
    Reports those with zero vs NIL in fees field.
    """
    infile = args['-i']
    if not infile:
        infile = Club.MEMBERSHIP_SPoT
    club = Club()
    err_code = member.traverse_records(
        infile, [member.get_zeros_and_nulls, ], club)
    res = ["Nulls:",
           "======", ]
    res.extend(club.nulls)
    res.extend(["\nZeros:",
               "======", ])
    res.extend(club.zeros)
    output('\n'.join(res))


def usps_cmd(args=args):
    """
    Generates a cvs file used by the Secretary to send out minutes.
        first,last,address,town,state,postal_code
    (Members who are NOT in the 'email only' category.)
    """
    infile = args['-i']
    if not infile:
        infile = Club.MEMBERSHIP_SPoT
    club = Club()
    club.usps_only = []
    err_code = member.traverse_records(infile, [
                member.get_usps,
                member.get_secretary,
                member.get_bad_emails,
                ], club)
    print("There are {} members without an email address."
          .format(len(club.usps_only)))
    res = []
    header = []
    for key in club.fieldnames:
        header.append(key)
        if key == "postal_code":
            break
    res.append(",".join(header))
    res.extend(club.usps_only)
    # The following 2 lines are commented out because new secretary
    # Michael Rafferty doesn't need/want to be on the list.
#   if hasattr(club, 'secretary'):
#       res.append(club.secretary)
    if club.bad_emails:
        print("... and {} more with a non functioning email."
              .format(len(club.bad_emails)))
        res.extend(club.bad_emails)
    return '\n'.join(res)


def club_setup4extra_charges(args=args):
    """
    Returns an instance of rbc.Club set up with what's needed
    to run the data.extra.charges function.
    """
    club = Club
    club.infile = args["-i"]
    if not club.infile:
        club.infile = club.EXTRA_FEES_SPoT
    club.json_file = args['-j']
    try:
        club.max_width = int(args['-w'])
    except TypeError:
        print("'-w' option must be an integer")
        sys.exit()
    club.presentation_format = args['-f']
    club.bad_format_warning = """Bad argument for '-f' option...
Choose one of the following:        [default: table]
        'table' listing of names /w fees tabulated (=> 2 columns.)
        'listing' same format as Data/extra_fees.txt
        'listings' side by side lists (best use landscape mode.) """
    return club



def extra_charges_cmd(args=args):
    """
    Returns a report of members with extra charges.
    It also can create a json file: specified by the -j option.
    """
    output('\n'.join(data.extra_charges(club_setup4extra_charges())))


def payables_cmd(args=args):
    """
    Sets up club attributes still_owing and advance_payments (both
    of which are lists) and then calls member.get_payables which
    traverses the db populating them.
    """
    infile = args['-i']
    if not infile:
        infile = Club.MEMBERSHIP_SPoT
    club = Club()
    club.still_owing = []
    club.advance_payments = []
    output = []
    err_code = member.traverse_records(infile,
                                       member.get_payables,
                                       club)
    if club.still_owing:
        helpers.add_header2list(
            "Members owing ({} in number)"
            .format(len(club.still_owing)),
            output, underline_char='=', extra_line=True)
        if args['-T']:
            tabulated = helpers.tabulate(club.still_owing,
                                         max_width=max_width,
                                         separator='  ')
            output.extend(tabulated)
        else:
            output.extend(club.still_owing)
    if club.advance_payments:
        output.append("\n")
        output.extend(["Members with a Credit",
                       "---------------------"])
        output.extend(club.advance_payments)
    return '\n'.join(output)


def show_mailing_categories_cmd(args=args):
    """
    Needs to be rewritten to take advantage of the -T and -w <width>
    options.
    """
    ret = ["Possible choices for the '--which' option are: ", ]
    ret.extend(
        helpers.tabulate(
            [key for key in content.content_types.keys()],
            separator='  '))
#   ret.extend((("\t" + key) for key in content.content_types.keys()))
    output('\n'.join(ret))


def prepare4mailing(club):
    """
    Set up configuration in an instance of rbc.Club.
    """
    club.owing_only = False
    if args['--oo']:
        club.owing_only = True
    if not args['--which']:
        club.which = content.content_types["thank"]
    else:
        club.which = content.content_types[args["--which"]]
    club.lpr = content.printers[args["-p"]]
    club.email = content.prepare_email_template(club.which)
    club.letter = content.prepare_letter_template(club.which,
                                                  club.lpr)
    if not args["-i"]:
        args["-i"] = club.MEMBERSHIP_SPoT
    club.input_file_name = args['-i']
    if not args["-j"]:
        args["-j"] = club.JSON_FILE_NAME4EMAILS
    club.json_file_name = args["-j"]
    if not args["--dir"]:
        args["--dir"] = club.MAILING_DIR
    club.mail_dir = args["--dir"]
    club.attachment = args['ATTACHMENTS']
    club.cc = args['--cc']
    club.bcc = args['--bcc']
    # *** Check that we don't overwright previous mailings:
    if club.which["e_and_or_p"] in ("both", "usps", "one_only"):
        print("Checking for directory '{}'.".format(args["--dir"]))
        club.check_mail_dir(club.mail_dir)
    if club.which["e_and_or_p"] in ("both", "email", "one_only"):
        print("Checking for file '{}'.".format(club.json_file_name))
        club.check_json_file(club.json_file_name)
        club.json_data = []


def prepare_mailing_cmd(args=args):
    """
    See description under 'Commands' heading in the docstring.
    Sets up an instance of rbc.Club with necessary attributes and
    then calls member.prepare_mailing.
    """
    # ***** Set up configuration in an instance of # Club:
    club = Club()
    prepare4mailing(club)
    # ***** Done with configuration & checks ...
    member.prepare_mailing(club)  # Populates club.mail_dir
    #                               and moves json_data to file.
    print("""prepare_mailing completed..
    ..next step might be the following:
    $ zip -r 4Michael {}""".format(args["--dir"]))


def setup4new_db(club):
    club.infile = args['-i']
    club.outfile = args['-o']
    club.extra_fees_spot = args['-X']
#   club.owing_only = args['--oo']  # Why?! Plan 2 delete.
    if not club.infile:
        club.infile = club.MEMBERSHIP_SPoT
#   print('club.outfile set to {}'.format(club.outfile))
    if club.outfile == 'stdout' or not club.outfile:
        club.outfile = helpers.prepend2file_name('new_', club.infile)
#   print('club.outfile set to {}'.format(club.outfile))
    if not club.extra_fees_spot:
        club.extra_fees_spot = club.EXTRA_FEES_SPoT
    club.fieldnames = data.get_fieldnames(club.infile)


def thank_cmd(args=args):
    club = Club()
    club.thank_file = args["-t"]
    if not club.thank_file:
        club.thank_file = Club.THANK_FILE
    member.traverse_records(club.thank_file,
                            [member.add2statement_data, ],
                            club)
    # To implememnt: maintain a record of those thanked...
    club.statement_data_keys = club.statement_data.keys()
    prepare4mailing(club)
    club.input_file_name = club.thank_file
    member.prepare_mailing(club)  # => thank_func,
    # Done with thanking; Must now update DB.
    setup4new_db(club)
    dict_write(club.outfile,
               club.fieldnames,
               member.modify_data(club.infile,
                                  member.credit_payment_func,
                                  club)
               )


def dict_write(f, fieldnames, iterable):
    """
    Writes all records received from <iterable> into a new csv
    file named <f>.  <fieldnames> defines the record keys.
    Code writen in such a way that <iterable> could be
    a generator function. (See member.modify_data.)
    """
    with open(f, 'w') as outfile_obj:
        print("Opening {} for output...".format(outfile_obj.name))
        dict_writer = csv.DictWriter(outfile_obj, fieldnames)
        dict_writer.writeheader()
        for record in iterable:
            dict_writer.writerow(record)


redacted = '''
def new_db_cmd():
    """
    One time use only:
    Eliminated 'email_only' field from data base.
    Already done so can redact this.
    """
    if args['-F'] and args['-F'] in member.func_dict:
        func, fieldnames = member.func_dict[args['-F']]
    else:
        print("Not a valid function parameter.")
        print("Must be one of the following:")
        for f in member.func_dict.keys():
            print("\t{}".format(f))
        print("Terminating")
        sys.exit()
    club = Club()
    setup4new_db(club)
    club.new_fieldnames = fieldnames
    dict_write(club.outfile, fieldnames,
               member.modify_data(club.infile, func, club)
               )
'''


def display_emails_cmd(args=args):
    records = helpers.get_json(args['-j'], report=True)
    all_emails = []
    n_emails = 0
    for record in records:
        email = []
        for field in record:
            email.append("{}: {}".format(field, record[field]))
        email.append('')
        all_emails.extend(email)
        n_emails += 1
    print("Processed {} emails...".format(n_emails))
    return "\n".join(all_emails)


def ck_lesssecureapps_setting():
    """
    Does nothing if not using a gmail account. (--mta ending in 'g')
    If using gmail the account security setting must be lowered:
    https://myaccount.google.com/lesssecureapps
    """
    if args['--mta'].endswith('g'):
        print(             # Check lesssecureapps setting:
            'Has "https://myaccount.google.com/lesssecureapps" been set')
        response = input(
            '.. and have you respoinded affirmatively to the warning? ')
        if ((not response) or not (response[0] in 'Yy')):
            print("Emailing won't work until that's done.")
            sys.exit()


def send_emails_cmd(args=args):
    """
    Sends emails prepared by prepare_mailing_cmd.
    See also content.authors_DOCSTRING.
    """
    ck_lesssecureapps_setting()
    mta = args["--mta"]
    emailer = args["--emailer"]
    if emailer == "python":
        emailer = Pymail.send.send
        print("Using Python modules to dispatch emails.")
    elif emailer == "bash":
        emailer = Bashmail.send.send
        print("Using Bash to dispatch emails.")
    else:
        print('"{}" is an unrecognized "--emailer" option.'
              .format(emailer))
        sys.exit(1)
    wait = mta.endswith('g')
    message = None
    data = helpers.get_json(args['-j'], report=True)
    emailer(data, mta, include_wait=wait)


def print_letters_cmd(args=args):
    """
    Depricated in favour of simply using 'lpr' cmd.
    """
    successes = []
    failures = []
    for letter_name in os.listdir(args["--dir"]):
        path_name = os.path.join(mail_dir, letter_name)
        completed = subprocess.run(["lpr", path_name])
        if completed.returncode:
            failures.append("Problem ({}) printing '{}'."
                            .format(completed.returncode, path_name))
        else:
            successes.append("{}".format(path_name))
    if successes:
        successes = ("Following letters printed successfully:\n"
                     + successes)
    else:
        successes = ["No file was printed successfully."]
    if failures:
        failures = ("Following letters failed to print:\n"
                    + failures)
    else:
        failures = ["All files printed successfully."]
    successes = '\n'.join(successes)
    failures = '\n'.join(failures)
    report = successes + args['--separator'] + failures
    output(report)


def emailing_cmd(args=args):
    """
    Uses mutt (in member.send_attachment.)
    Sends emails with an attachment.
    Sets up an instance of Club and traverses
    the input file calling member.send_attachment
    on each record.
    """
    club = Club()
    club.mutt_send = mutt_send
    if not args["-i"]:
        args["-i"] = club.MEMBERSHIP_SPoT
    with open(args["-c"], "r") as content_file:
        club.content = content_file.read()
    err_code = member.traverse_records(args["-i"],
                                       member.send_attachment,
                                       club=club)


def restore_fees_cmd(args=args):
    """
    If records are found with balance still outstanding, these are
    reported to errors.  Also reported will be anyone listed as paying
    fees but not found amongst members.
    Repopulates the club's master list with the ANNUAL_DUES constant
    and any fees being charged as specified in the file specified by
    'args['<extra_fees.json>']'.
    The -i <membership_file> is not changed.
    If '-o <temp_membership_file>' is specified, output goes there,
    if not, output goes to a file named by concatenating 'new_' with
    the name of the input file.
    """
    # ## During implementation, be sure to ...                     ###
    # ## Take into consideration the possibility of credit values. ###
    club = Club()
    setup4new_db(club)
    data.restore_fees(club)  # Populates club.new_db & club.errors
    data.save_db(club.new_db, club.outfile, club.fieldnames)
    if club.errors:
        output('\n'.join(
               ['Note the following irregularities:',
                '==================================', ]
               + club.errors), destination=args['-e'])

#   if club.still_owing:
#       pass
    if club.errors and args["-e"]:
        with open(args["-e"], 'w') as file_obj:
            file_obj.write('\n'.join(club.errors))
            print('Wrote errors to "{}".'.format(file_obj.name))
#   if ret:
#       sys.exit(ret)


def fee_intake_totals_cmd(args=args):
    """
    This command deals with the manual method of entering receipts.
    Eventually this will be deprecated in favour of the thank_cmd
    """
    outfile = args['-o']
    errorfile = args['-e']
    club = Club()
    if args['-i']:
        fees_taken_in = club.fee_totals(infile=args['-i'])
    else:
        fees_taken_in = club.fee_totals()
    fees_taken_in.append(" ")
    res = '\n'.join(fees_taken_in)
    output(res)
    if club.invalid_lines and errorfile:
        print('Writing possible errors to "{}".'
              .format(errorfile))
        output('\n'.join(club.invalid_lines),
               errorfile, announce_write=False)


def labels_cmd(args=args):
    if args["-P"]:
        medium = media[args["-P"]]
    else:
        medium = A5160
    club = Club(medium)
    club = args["-i"]
    return club.get_labels2print(source_file)


def envelopes_cmd(args=args):
    if args["-P"]:
        medium = media[args["-P"]]
    else:
        medium = E0000
    club = Club(medium)
    source_file = args["-i"]
    club.print_custom_envelopes(source_file)


def wip_cmd(args=args):
    """
    Code under development (work in progress) temporarily housed here.
    """
    applicants = data.get_applicant_data(Club.APPLICANT_SPoT,
                                         Club.SPONSORS_SPoT)
    for key in applicants.keys():
        if applicants[key]['dates']:
            print("{}: Meeting dates {}"
                  .format(key, applicants[key]['dates']))
        else:
            print("{}: No meetings attended to date."
                  .format(key))
        print("\tsponsors are {}".format(applicants[key]['sponsors']))
    return


# # Plan to redact the next two functions in favour of using
# # the Python mailing modules instead of msmtp and mutt.
# # For the time being the Python modules are being used
# # when sending via Easydns.com but msmtp is still being
# # used when gmail is the MTA.


'''
def smtp_send(recipients, message):
    """
    Send email, as defined in <message>,
    to the <recipients> who will receive this email
    from the Bolinas Rod and Boat Club.
    <recipients> must be an iterable of one or more email addresses.
    Note: Must first lower br&bc's account security at:
    https://myaccount.google.com/lesssecureapps
    Also Note: <message> must be in proper format with
    "From:", "To:" & "Subject:" lines (no leading spaces!) followed
    by a blank line and then the text of the email. The "From:" line
    should read as follows: "From: rodandboatclub@gmail.com"
    """
    cmd_args = ["msmtp", "-a", glbs.MSMTP_ACCOUNT, ]
    for recipient in recipients:
        cmd_args.append(recipient)
    p = subprocess.run(cmd_args, stdout=subprocess.PIPE,
                       input=message, encoding='utf-8')
    if p.returncode:
        print("Error: {} ({})".format(
            p.stdout, recipient))
'''


def mutt_send(recipient, subject, body, attachments=None):
    """
    Does the mass e-mailings with attachment(s) which, if
    provided, must be in the form of a list of files.
    """
    cmd_args = ["mutt", "-F", args["-F"], ]
    cmd_args.extend(["-s", "{}".format(subject)])
    if attachments:
        list2attach = ['-a']
        for path2attach in attachments:
            list2attach.append(path2attach)
        cmd_args.extend(list2attach)
    cmd_args.extend(["--", recipient])
    p = subprocess.run(cmd_args, stdout=subprocess.PIPE,
                       input=body, encoding='utf-8')
    if p.returncode:
        print("Error: {} ({})".format(
            p.stdout, recipient))


if __name__ == "__main__":
    #   print(args)

    if args["?"]:
        doc_lines = __doc__.split('\n')
        for n in range(len(doc_lines)):
            if doc_lines[n] == "Usage:":
                uline = n
            if doc_lines[n] == "Options:":
                oline = n
                break
        print('\n'.join(doc_lines[uline:oline - 1]))
    elif args["ck_data"]:
        ck_data_cmd()
    elif args["show"]:
        show_cmd()
    elif args["names_only"]:
        names_only_cmd()
    elif args["report"]:
        report_cmd()
    elif args["stati"]:
        stati_cmd()
    elif args["zeros"]:
        zeros_cmd()
    elif args["usps"]:
        print("Preparing a csv file listing showing members who")
        print("receive meeting minutes by mail. i.e. don't have (or")
        print("haven't provided) an email address (to the Club.)")
        output(usps_cmd())
    elif args["extra_charges"]:
        print("Selecting members with extra charges:")
        extra_charges_cmd()
    elif args["payables"]:
        print("Preparing listing of payables...")
        output(payables_cmd())
    elif args['show_mailing_categories']:
        show_mailing_categories_cmd()
    elif args["prepare_mailing"]:
        print("Preparing emails and letters...")
        prepare_mailing_cmd()
        print("...finished preparing emails and letters.")
    elif args["thank"]:
        print("Preparing thank you emails and/or letters...")
        thank_cmd()
#       print("...finished preparing thank you emails and/or letters.")
    elif args['display_emails']:
        output(display_emails_cmd())
    elif args["send_emails"]:
        print("Sending emails...")
        send_emails_cmd()
        print("Done sending emails.")
    elif args["print_letters"]:
        print("Printing letters ...")
        print_letters_cmd()
        print("Done printing letters.")
    elif args['emailing']:
        emailing_cmd()
    elif args['restore_fees']:
        restore_fees_cmd()
    elif args['fee_intake_totals']:
        fee_intake_totals_cmd()
    elif args["labels"]:
        print("Printing labels from '{}' to '{}'"
              .format(args['-i'], args['-o']))
        output(labels_cmd())
    elif args["envelopes"]:
        # destination is specified within Club
        # method print_custom_envelopes() which is called
        # by print_statement_envelopes()
        print("""Printing envelopes...
    addresses sourced from '{}'
    with output sent to '{}'"""
              .format(args['-i'], args['-o']))
        envelopes_cmd()
    elif args["wip"]:
        print("Work in progress command...")
        wip_cmd()
    elif args["new_db"]:
        print("Creating a modified data base...")
        new_db_cmd()
    else:
        print("You've failed to select a command.")
        print("Try ./utils.py ?           # brief!  or ...")
        print("    ./utils.py -h          # for more detail  or ...")
        print("    ./utils.py -h | pager  # to catch it all.")

NOTE = """
emailing_cmd()
    uses Club.traverse_records(infile,
        club.send_attachment(args["-i"]))
"""
