#!/bin/env python

# Last modified by Dylan G. Hsu on 2014-12-08

import sys, os
import collections
import datetime
import json

# length of a lumisections, corresponding to 2**18 LHC orbits, or 23.31 seconds
SECS_PER_LUMI = 23.31040958083832;

# Supply this method with a FULL PATH to a .jsndata file to read it and put the HLT or L1 rates inside into the database.
# The jsndata needs the .ini descriptor files to be there or this will fail
#
# For the HLT rates, each lumisection has several path IDs which get their own row for that LS.
# We get these path IDs by looking up the path names provided in the .ini file in a mapping
# from the production database.
# For the L1 rates, we insert a single row per LS.
# However in this row are two Varrays containing 128 and 64 bits respectively, for the trigger rates, accomplishing in
# 1 row what the HLT rates table does with many rows.

def monitorRates(jsndata_file):
    # This takes the full path of a .jsndata file as parameter
    # Any other call of this function is inappropriate and will just not work!
    # e.g. jsndata_file='/store/lustre/mergeMiniDAQMacro/run230852/run230852_ls0110_streamHLTRates_mrg-c2f13-37-01.jsndata'

    json_dir=os.path.dirname(jsndata_file)
    jsndata_filename=os.path.basename(jsndata_file)
    file_raw, file_ext = os.path.splitext(jsndata_filename)
    raw_pieces=file_raw.split( '_' , 3 ) # this is not an emoji!
    run_number=raw_pieces[0][3:] # 123456
    ls=raw_pieces[1] # ls1234
    stream=raw_pieces[2][6:] # HLTRates | L1Rates
    extra=raw_pieces[3]

    if stream != "HLTRates" and stream != "L1Rates":
        print 'Unrecognized rate stream: '+raw_pieces[2]
        return False
    
    # Open the jsndata file
    # If it doesn't exist, this function will crash

    try:
        rates_json=open(jsndata_file).read()
    except (OSError, IOError) as e:
        print 'Error finding or opening jsndata file: "'+jsndata_file+'"'
        return False
    rates=json.loads(rates_json)

    # Get the ini in the directory with rates corresponding to specified run number, lumi section, and HLT|L1
    # The correspondence might look like:
    # run230852_ls0110_streamL1Rates_mrg-c2f13-37-01.jsndata =>
    # run230852_ls0000_streamL1Rates_mrg-c2f13-37-01.ini
    # If the INI file is not there, this function will crash

    ini_filename=raw_pieces[0]+'_ls0000_'+raw_pieces[2]+'_'+raw_pieces[3]+'.ini'
    if stream=='HLTRates':
        try:
            HLT_json=open(json_dir+'/'+ini_filename).read()
        except (OSError, IOError) as e:
            print 'Error finding or opening ini file: "'+json_dir+'/'+ini_filename+'"'
        HLT_names = json.loads(HLT_json)
        HLT_rates = collections.OrderedDict()
        # Get the rates for each trigger path
        for i, pathname in enumerate(HLT_names['Path-Names']):
            HLT_rates[pathname] = {}
            HLT_rates[pathname]['L1PASS']   = rates['data'][2][i]
            HLT_rates[pathname]['PSPASS']   = rates['data'][3][i]
            HLT_rates[pathname]['PACCEPT']  = rates['data'][4][i]
            HLT_rates[pathname]['PREJECT']  = rates['data'][5][i]
            HLT_rates[pathname]['PEXCEPT']  = rates['data'][6][i]

        sys.stdout.write("\x1b[0;0;32m")
        print "%-60s       %12s    %12s    %12s" % ("HLT Path Name", "L1 seed rate", "Prescale rate", "HLT path rate")
        sys.stdout.write("\x1b[0;0m")
        for (pathname, rate) in HLT_rates.iteritems():
            print "%-60s    %10.1f Hz    %10.1f Hz    %10.1f Hz" % (pathname, rate['L1PASS'] / SECS_PER_LUMI, rate['PSPASS'] / SECS_PER_LUMI, rate['PACCEPT'] / SECS_PER_LUMI)
        print

    
    elif stream=='L1Rates':
        try:
            L1_json=open(json_dir+'/'+ini_filename).read()
        except (OSError, IOError) as e:
            print 'Error finding or opening ini file: "'+json_dir+'/'+ini_filename+'"'
        L1_names = json.loads(L1_json)
        L1_rates = collections.OrderedDict()
        L1_rates['EVENTCOUNT']      = rates['data'][0][0]
        L1_rates['L1_DECISION']     = rates['data'][1]
        L1_rates['L1_TECHNICAL']    = rates['data'][2]
        L1_rates['MOD_DATETIME']    = str(datetime.datetime.fromtimestamp(os.path.getmtime(jsndata_file)))
        # Here we record the file modification time of the jsndata file for book keeping purposes
        
        sys.stdout.write("\x1b[0;0;32m")
        print "%-60s       %12s" % ("L1 Algo Trigger", "post-DT rate")
        sys.stdout.write("\x1b[0;0m")
        for i, rate in enumerate(L1_rates['L1_DECISION']):
            print "%-60s    %10.1f Hz" % (L1_names['L1-Algo-Names'][i], rate / SECS_PER_LUMI)
        print
        sys.stdout.write("\x1b[0;0;32m")
        print "%-60s       %12s" % ("L1 Tech Trigger", "post-DT rate")
        sys.stdout.write("\x1b[0;0m")
        for i, rate in enumerate(L1_rates['L1_TECHNICAL']):
            print "%-60s    %10.1f Hz" % (L1_names['L1-Tech-Names'][i], rate / SECS_PER_LUMI)
        print


for arg in sys.argv[1:]:
    sys.stdout.write("\x1b[0;0;31m")
    print arg
    sys.stdout.write("\x1b[0;0m")
    monitorRates(arg)
