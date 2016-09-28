#! /usr/bin/env python

#Usage: This script takes an HLT menu in ORCOFF as argument and changes the menu on the Hilton. 
#       It assumes that the HLT browser is currently not broken (if you get a menu without the 
#       name in the heading, check the browser).
#       It also assumes that the test_hlt_config1 in /etc/hltd.conf is set to 
#       python/HiltonMenu.py. If this is not the case, you will need to change it by hand.
#       
#       Update 21/09/16: ported newHiltonMenu.sh to python


import argparse
import subprocess
import os
import sys

def l1xml_override(l1xml_filename):
    """ Returns a string of the python necessary to override the L1 menu using an xml."""
    #because the L1TUtmTriggerMenuESProducer has the path hardcoded to a specific directory,
    #specifically L1Trigger/L1TGlobal/data/Luminosity/startup/ 
    #we need to escape that back up to the root of the filesystem
    #hence if the CMSSW directory structure changes or hilton install location changes (unlikely)
    #this will break    
    l1xml_str= 'process.TriggerMenu = cms.ESProducer( "L1TUtmTriggerMenuESProducer",\n'
    l1xml_str+='    L1TriggerMenuFile = cms.string("../../../../../../../../../../../../%s")\n' % os.path.abspath(l1xml_filename)
    l1xml_str+=')\n'
    return l1xml_str

   
def l1gt_override(tagname):
    """ Returns a string of the python necessary to override the L1 menu using an GT record."""
    l1gt_str= "process.GlobalTag.toGet = cms.VPSet(\n"
    l1gt_str+="   cms.PSet(\n"
    l1gt_str+="       connect = cms.string('frontier://(proxyurl=http://localhost:3128)(serverurl=http://localhost:8000/FrontierOnProd)(serverurl=http://localhost:8000/FrontierOnProd)(retrieve-ziplevel=0)/CMS_CONDITIONS'),\n"
    l1gt_str+="       record = cms.string('L1TUtmTriggerMenuRcd'),\n"
    l1gt_str+="       snapshotTime = cms.string('9999-03-21 17:00:00.000'),\n"
    l1gt_str+="       tag = cms.string('%s')\n" % tagname
    l1gt_str+="   )\n"
    l1gt_str+=")\n"
    return l1gt_str

def main(args):

    if os.getenv("CMSSW_VERSION") == None:
        print "You need to do cmsenv first"
        sys.exit()


    print  "dumping",args.menu," from ConfDB v2..."
    out,err = subprocess.Popen(['/nfshome0/hltpro/scripts/hltConfigFromDB',
                                '--v2','--gdr','--configName',args.menu],
                               stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
    with open("hlt.py","w") as f:
        f.write(out)

    # check for errors in the menu
    print "checking dump consistency"
    try:
        from hlt import process
        print "   found HLT version: \t%s" % process.HLTConfigVersion.tableName.value()
    except:
        print "   hlt menu (dump is in hlt.py) is corrupted, most of the time this is a typo in menu name"
        sys.exit()

    # convert the hlt menu for online use in the hilton
    # run the menu checker script
    print "\nrunning MenuChecker.py"
    subprocess.Popen(["python","/nfshome0/hltpro/RateMon/MenuChecker.py",args.menu]).communicate()

    globaltag = process.GlobalTag.globaltag.value()
    print " "
    print "checking L1 seeds in HLT menu against L1 xml in global tag",globaltag
    subprocess.Popen(["/nfshome0/hltpro/scripts/L1MenuCheck_FromGT.sh",
                      "hlt.py",globaltag]).communicate()

    if process.GlobalTag.toGet.value()==[]:
        print "checking for GlobalTag overrides: \033[32mSUCCEEDED\033[0m"
    else:
        print "checking for GlobalTag overrides: \033[31mFAIL\033[0m"
        print "\033[31mERROR:\033[0m overriding records in GlobalTag, \033[31m this must be removed from the menu!\033[0m"
        for pset in process.GlobalTag.toGet.value():
            print "   ",pset.dumpPython().replace("\n","\n    ")
 
    print "\nconverting menu for use on hilton"

    with open("/nfshome0/hltpro/scripts/hilton_menu_overrides.txt") as f:
        menu_overrides = f.read()
    if args.l1XML!=None:
        print "   overriding L1 menu for hilton config with xml:",args.l1XML
        menu_overrides += l1xml_override(args.l1XML)
        print "   rechecking HLT menu for missing seeds in xml"
        #the hlt.py is just used to get the list of seeds so doesnt matter that we have not
        #rewriten the xml override to it yet
        subprocess.Popen(["/nfshome0/hltpro/scripts/L1MenuCheck.sh","hlt.py",args.l1XML]).communicate()

    if args.l1GT!=None:
        print "   overriding L1 menu for hilton config with gt record:",args.l1GT
        menu_overrides += l1gt_override(args.l1GT)

    with open("hlt.py","a") as f:
        f.write(menu_overrides)


    subprocess.Popen(["sudo","cp","hlt.py","/opt/hltd/python/HiltonMenu.py"]).communicate()
    os.remove("hlt.py")

    import ConfigParser
    hltd_config = ConfigParser.RawConfigParser()
    hltd_config.read("/etc/hltd.conf")
    print "\nHLTD config:"
    print "   ",hltd_config.get("CMSSW","test_hlt_config1")
    print "   ",hltd_config.get("CMSSW","cmssw_default_version")
    print "\nheading of /opt/hltd/python/HiltonMenu.py:"
    subprocess.Popen(["head","-1","/opt/hltd/python/HiltonMenu.py"]).communicate()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='takes a HLT menu in ORCOFF and changes the menu on the Hilton')
    parser.add_argument('menu',help='HLT menu location in ORCOFF')
    parser.add_argument('--l1XML',help='overrides the L1 menu in the resulting hilton menu via an XML file ')
    parser.add_argument('--l1GT',help='override the L1 menu in the resulting hilton menu via a GlobalTag record, example would be "--l1GT L1Menu_Collisions2016_v6r8m_m2" ask your friendly L1 menu expert for the correct record name')
    args = parser.parse_args()
    main(args)
