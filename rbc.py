#/usr/bin/env python

# File: rbc.py

"""
This module is specific to the Bolinas Rod and Boat Club
data as maintained in the (4 or 5, depending how you count)
SPoT (Single Point of Truth) files.
It provides the <Club> class.
Most of class Club (all of its methods) is/are being redacted,
its/their functionality having been moved elsewhere.
"""

import os
import sys
import shutil
import helpers

# Specify input file and its data:
class Club(object):
    """
    Create such an object for each data base used.
    In the current use case this is the only one and
    it pertains to the 'Bolinas Rod and Boat Club'.

    It may well be that most if not all the methods are redacted,
    their functionality taken over by code found elsewhere.
    """

    ## Constants and Defaults...
    YEARLY_DUES = 100

    # Data bases used with default file names.
    MEMBERSHIP_SPoT = 'Data/memlist.csv'
    APPLICANT_SPoT = "Data/applicants.txt"
    SPONSORS_SPoT = "Data/sponsors.txt"
    EXTRA_FEES_SPoT = 'Data/extra_fees.txt'
    CONTACTS_SPoT = os.path.expanduser(     #} File to which google
                '~/Downloads/contacts.csv') #} exports the data.
    RECEIPTS_FILE = 'Data/receipts-{}.txt'.format(helpers.this_year)
    THANK_FILE = 'Info/2thank.csv'
        # Zeroed out yearly
        # and then stored in archives with date extension.
        # The method for dealing with receipts is expected to change
        # to use of the utils.thank_cmd.

    SEPARATOR = "|"   #} File APPLICANT_SPoT must be in a
    N_SEPARATORS = 3  #} specific format for it to be read
                      #} correctly. Number of meetings is
                      #} derived from N_SEPARATORS.
    ### NOTE: this SEPARATOR although having the same value is NOT
    ### the same as the one defined in member.py module.
    NAME_KEY = "by_name"         #} Used in context of
    CATEGORY_KEY = "by_category" #} the extra fees.

    ## Google Contact Groups in use:
    GOOGLE_GROUPS = { "applicant," "DockUsers", "Kayak",
            "LIST", "moorings", "Officers", 'Secretary',
            "member",   # 'member' is there but not used.
            }
    ### Should use the above to check data integrity!! ####
    ### Yet to be implemented. ###
    APPLICANT_GROUP = "applicant"  # } These are specific to
    MEMBER_GROUP = "LIST"          # } the gmail contacts csv:
    OFFICER_GROUP = 'Officers'     # } CONTACTS_SPoT
    DOCK_FEE = 75
    KAYAK_FEE = 70
    DOCK = 'DockUsers'     #} These are the 'groups'
    KAYAK = 'Kayak'        #} as defined in the club's
    MOORING = 'moorings'   #} gmail contacts.

    SECRETARY = "Michael Rafferty"

    # Intermediate &/or temporary files used:
    EXTRA_FEES_JSON = 'Data/extra_fees.json'
    EXTRA_FEES_TBL = 'Data/extra_fees.tbl'  # not used!
    TEMP_MEMBERSHIP_SPoT = 'Data/new_memlist.csv'
    OUTPUT2READ = 'Data/2read.txt'       #} generally goes to stdout.
    MAILING_DIR = 'Data/MailingDir'
    JSON_FILE_NAME4EMAILS = 'Data/emails.json'
    ## ...end of Constants and Defaults.

    def __init__(self, params=None):
        """
        <params> was necessary in the past when using labels or
        envelopes but is expected to be redacted since these are
        no longer used. Each instance needed to know the format
        of the media.
        """
        self.infile = Club.MEMBERSHIP_SPoT
        self.pattern = '{last}, {first}'
#       self.json_data = []
        self.previous_name = ''              # } Used to
        self.previous_name_tuple = ('', '')  # } check 
        self.first_letter = ''               # } ordering.


    def fee_totals(self, infile=RECEIPTS_FILE):
        """
        Returns a list of strings: subtotals and grand total.
        Sets up and populates self.invalid_lines ....
        (... the only reason it's a class method
        rather than a function or a static method.)
        NOTE: Money taken in (or refunded) must appear
        within line[23:28]! i.e. maximum 5 digits (munus sign
        and only 4 digits if negatime).
        """
        res = ["Fees taken in to date:"]
        self.invalid_lines = []

        total = 0
        subtotal = 0
        date = ''

        with open(infile, "r") as file_obj:
            print('Reading from file "{}".'
                .format(file_obj.name))
            for line in file_obj:
                line= line.rstrip()
                if line[:5] == "Date:":
                    date = line
                if (line[24:27] == "---") and subtotal:
                    res.append("    SubTotal            --- ${}"
                        .format(subtotal))
                    subtotal = 0
                try:
                    amount = int(line[23:28])
                except (ValueError, IndexError):
                    self.invalid_lines.append(line)
                    continue
#               res.append("Adding ${}.".format(amount))
                total += amount
                subtotal += amount
#               print(" adding {}, running total is {}"
#                   .format(amount, total))
        if subtotal:
            res.append("    SubTotal            --- ${}"
                .format(subtotal))
        res.append("\nGrand Total to Date:    --- ---- ${}"
            .format(total))
#       print("returning {}".format(res))
        return res


    def check_dir4letters(self, dir4letters):
        """
        Set up the directory for postal letters.
        """
        if os.path.exists(dir4letters):
            print("The directory '{}' already exists."
                .format(dir4letters))
            response = input("... OK to overwrite it? ")
            if response and response[0] in "Yy":
                shutil.rmtree(dir4letters)
            else:
                print(
            "Without permission, must abort.")
                sys.exit(1)
        os.mkdir(dir4letters)
        pass


    def check_json_file(self, json_email_file):
        """
        Checks the name of the json output file where
        emails are to be stored.
        """
#       print("method check_json_file param is: {}"
#           .format(json_email_file))
        if os.path.exists(json_email_file):
            print("The file '{}' already exists."
                .format(json_email_file))
            response = input("... OK to overwrite it? ")
            if response and response[0] in "Yy":
                os.remove(json_email_file)
            else:
                print(
            "Without permission, must abort.")
                sys.exit(1)

### I believe methods can all be redacted. ###
### They are implemented elsewhere: mostly in data.py
### 
####  End of Club class declaration.
