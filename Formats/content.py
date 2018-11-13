#!/usr/bin/env python

# File: content.py

"""
A supporting utility.
Povides, in the form of a dict, the formating strings required by the
'billing' command of the Bolinas Rod & Boat Club utility 'util.py'.

This dict can be imported from this module:
    from Formats.content import content
or ...
the dict can be loaded from a json file created by this module.

If run as 'main' it accepts an optional command line argument
which if not provided defaults to "Formats/content.json".

Don't forget to edit to suit- especially don't forget to modify
the date in "postal_header".

Responsibilities of a
<cust_func>(record, field_names, content, j_record, letters_dir):
Based on the <record> param (which might be modified)
decides what if anything to add to the <j_record> parameter
and to the <letters_dir> (the name of a directory.)
<content> is a dict providing content as needed.
<field_names> is needed in some instances (to deal with fees.)
"""

import os
import sys
import json
from helpers import indent

content_1st_request = {
"subject": "Club fees coming due",

"email_header": """From: rodandboatclub@gmail.com
To: {email}
Subject: {subject}

Dear {first} {last},

""",

"postal_header": """




Bolinas Rod and Boat Club
PO Box 248
Bolinas, CA 94924


{date}



{first} {last}
{address}
{town}, {state} {zip}



Re: {subject}

Dear {first} {last},

""",

"body": """

With July comes the beginning of the new membership year
and ideally we'd like to have all dues and fees in by now.
If you are already paid up, the Club thanks you.

While we've got your attention: please go to the Club web site
(rodandboatclub.com, password is 'fish',) click on 'Membership'
and check that all your data is as you would like it to be.
If you see anything not to your liking, let us know of any
changes you'd like to see made.  You can reply either by email
(if you are receiving this as an email) or by post to the
address provided below.  By the way, if you are getting this
by post but have an email address, we'd very much like to 
know about it and switch you over to 'email_only' status.

A statement of your current standing will appear bellow;
If there are any dues or fees outstanding, please pop your
check into an envelope asap payable and sent to the...
        Bolinas Rod and Boat Club
        PO Box 0248
        Bolinas, CA 94924
{extra}

Sincerely,
Alex Kleider (Membership)"""

}

content_penalty_notice = {
"subject":"BR&BC dues and penalty for late payment",

"email_header":"""From: rodandboatclub@gmail.com
To: {email}
Subject: {subject}

Dear {first} {last},

""",

"postal_header":"""



Bolinas Rod and Boat Club
PO Box 248
Bolinas, CA 94924


{date}



{first} {last}
{address}
{town}, {state} {zip}



Re: {subject}

Dear {first} {last},

""",

"body":"""
The deadline for Club Dues payment has passed.  Records indicate that
you are in arrears with regard to payment of Club dues and a late fee
of $25 is now applied in addition to the regular dues payment of $100.
If you feel this is incorrect, please speak up[1]- we are only human!
Otherwise, don't delay sending in your check.  The end of September
is when anyone who hasn't payed ceases to be a member.

Please pop your check (for $125) into an envelope asap payable and
addressed to the...
        Bolinas Rod and Boat Club
        PO Box 0248
        Bolinas, CA 94924

Sincerely,
Alex Kleider (Membership)

[1] rodandboatclub@gmail.com or a letter to the PO Box

[2] If the club has an email address on file for you, you'll be
receiving this by email as well as 'snail mail.'
"""
}

content_early_aug2018 = {
"subject":"August mailing",

"email_header":"""From: rodandboatclub@gmail.com
To: {email}
Subject: {subject}

Dear {first} {last},

""",

"postal_header":"""



Bolinas Rod and Boat Club
PO Box 248
Bolinas, CA 94924


{date}



{first} {last}
{address}
{town}, {state} {zip}



Re: {subject}

Dear {first} {last},

""",

"body":"""
August is upon us and that is when the Club imposes a penalty
for late payment of dues.

Records indicate that you are in arrears.  If you feel this
is incorrect, please speak up[1]- we are only human!
Otherwise, don't delay sending in your check.  The end of
September is when anyone who hasn't payed ceases to be a member.

Because this is the first year we've been sending notices by email,
Club leadership has determined that before late fees are imposed, at
least one posted notice should be sent out[2] so for this year only,
late fees will not be imposed until after the fishing derby coming
up later this month.

Please pop your check into an envelope asap payable and addressed
to the...
        Bolinas Rod and Boat Club
        PO Box 0248
        Bolinas, CA 94924

Details are as follows:
{}

Sincerely,
Alex Kleider (Membership)

[1] rodandboatclub@gmail.com or a letter to the PO Box

[2] If the club has an email address on file for you, you'll be
receiving this by email as well as 'snail mail.'
"""

}

def custom_early_aug2018(record, log = None):
    """
    Returns a (possibly empty) list of strings.
    Determines what to place in the customizable spot of a letter.
    A specialized version of this function will have to be written
    for each letter and passed to the <billing> method.
    <record> should be a dict created by the <make_dict> method of
    the <Membership> class.
    <log>, if provided, is assumed to be a mutable iterable.
    """
    ret = []

    fees = {}
    fees["Club dues"] = record["dues"]
    fees["Mooring"] = record["mooring"]
    fees["Dock usage"] = record["dock"]
    fees["Kayak storage"] = record["kayak"]
    total_due = 0
    for item in ["Club dues", "Mooring",
                    "Dock usage", "Kayak storage"]:
        if fees[item]:
            fee = int(fees[item])
        else:
            fee = 0
        if fee:
            total_due += fee
            ret.append(
                "{:<13}: ${}".format(item, fee))
    if ret:
        if log:
            log.append("{:<25} {}".format(
                record["first"] + ' ' + record["last"],
                ", ".join(ret)))
        ret.append("Total:           ${}".format(total_due))
        pass

    else:
#       ret = ["\nYou're all paid up!"]
        pass
    return ret


def cust_aug31_2018(record, field_names, content,
                    j_record, letters_dir):
    """
    Responsibilities of a
        <cus_func>(record, content, j_record, letters_dir):
    Based on the <record> param (which might be modified)
    decides what if anything to add to the <j_record> parameter
    and to the <letters_dir> (the name of a directory.)
    <content> is a dict providing content as needed.
    <field_names> provides access to any needed keys in <record>.
    """
    fees_outstanding = []
    for key in field_names[-4:]:
#       print("key/value are: '{}'/ '{}'"
#           .format(key, record[key]))
        if record[key] and int(record[key])>0:
            fees_outstanding.append(
                "{} {}"
                .format(
                key,
                record[key]
                ))
    if fees_outstanding:
#       extras = ''
        if record["email"]:  # create email and add to json
            entry = (content["email_header"] .format(**record)
                + content["body"]  # .format(record["extras"])
                )
            j_record.append([[record["email"]], entry])
            print("Appended to json_ret")
#       record["extras"] = indent(record["extras"])
        entry = (
            content["postal_header"].format(**record)
            + content["body"]   # .format(record["extras"])
            )
        entry = indent(entry)
        path2write = os.path.join(letters_dir,
            "_".join((record['last'], record['first'])))
        with open(path2write, "w") as file_object:
            file_object.write(entry)

proto_content = {
"subject": "Proto mailing",

"email_header": """From: rodandboatclub@gmail.com
To: {email}
Subject: {subject}

Dear {first} {last},

""",

"postal_header": """




Bolinas Rod and Boat Club
PO Box 248
Bolinas, CA 94924


{date}



{first} {last}
{address}
{town}, {state} {zip}



Re: {subject}

Dear {first} {last},

""",

"body": """
Blah, Blah-
more Blah blah

etc

First extra content is
{extra0}

May have as many 'extras' as required as long as each one
is defined by the custom function
the content dict.  i.e. {extra1}

Sincerely,
Alex Kleider (Membership)"""

}

content_new_applicant_welcome = {
"subject": "Welcome to the Club",

"email_header": """From: rodandboatclub@gmail.com
To: {email}
Subject: {subject}

Dear {first} {last},

""",

"postal_header": """




Bolinas Rod and Boat Club
PO Box 248
Bolinas, CA 94924


{date}



{first} {last}
{address}
{town}, {state} {zip}



Re: {subject}

Dear {first} {last},

""",

"body": """
As Membership Chair it is my pleasure to welcome you as a new
applicant for membership in the Bolinas Rod and Boat Club.

Please come and enjoy the meetings (first Fiday of each month.)
To become eligible for membership (and not waste your application
fee) you must attend a minimum of three meetings with in the six
month period beginning the date your application was received. 

Sincerely,
Alex Kleider (Membership)"""

}

content_request_inductee_payment = {
"subject": "Welcome to the Bolinas Rod & Boat Club",

"email_header": """From: rodandboatclub@gmail.com
To: {email}
Subject: {subject}

Dear {first} {last},

""",

"postal_header": """




Bolinas Rod and Boat Club
PO Box 248
Bolinas, CA 94924


{date}



{first} {last}
{address}
{town}, {state} {zip}



Re: {subject}

Dear {first} {last},

""",

"body": """
As you may already know, the Club Executive approved your application
for Club membership at their October 5th meeting.  All that remains
for your membership to take effect is payment of dues. 

Please send a check for $100 to the Club at
    PO Box 248
    Bolinas, CA 94924

Upon receipt of your membership dues, I'll send you more information
about the Club and your privileges as a member there of.


Sincerely,
Alex Kleider (Membership)"""

}

welcome_member = {
"subject": "Welcome to the Bolinas Rod & Boat Club",

"email_header": """From: rodandboatclub@gmail.com
To: {email}
Subject: {subject}

Dear {first} {last},

""",

"postal_header": """




Bolinas Rod and Boat Club
PO Box 248
Bolinas, CA 94924


{date}



{first} {last}
{address}
{town}, {state} {zip}



Re: {subject}

Dear {first} {last},

""",

"body": """
It is my pleasure to welcome you as a new member to the Bolinas Rod
and Boat Club!

You will now be receiving meeting minutes (via email) as prepared by
current Secretary Peter Pyle.

As you may know, the Club has its own web site: 'rodandboatclub.com'.
It is password protected; the password is 'fish' (a not very closely
guarded secret.)  By clicking on the "Membership" heading, you can
find all your fellow members along with contact information.  If you
see any inaccuracies there, please let me know [1] so corrections can
be made.

Members can (upon payment of a $10 deposit) get a key to the Club
from "keeper of the keys" Ralph Cammicia.  Many take advantage of
having this access to spend time on the balconey enjoying views of the
lagoon and Bolinas Ridge.  Please be sure to lock up upon leaving.

The Club is available for members to rent for private functions (if
certain conditions are met.)  More information can be found on the web
site: "Rules and Forms" and under that "Club Rentals".

Most important of all, come to meetings and other functions to enjoy
the comraderie!


Sincerely,
Alex Kleider (Membership)


[1] email to rodandboatclub@gmail.com or PO Box 428, 94924
"""
}

#content = content_late_aug2018
cust_func = cust_aug31_2018

if __name__ == "__main__":
    if len(sys.argv) > 1:
        jsonfile = sys.argv[1]
    else:
        jsonfile = "Formats/content.json"
    with open(jsonfile, "w") as file_object:
        json.dump(content, file_object)

