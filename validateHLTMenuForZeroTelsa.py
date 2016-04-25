#Sam Harper
#
# a little script to print out all the E/p cut values below a given threshold (99999)
#
# use as python validateHLTMenuForZeroTelsa.py inputFiles=hlt.py
#


def printEPValues(process,pathName,printThres=9999999):
    outputStr=pathName
    hasEPFilter=False
    path = getattr(process,pathName)
    for filterName in path.moduleNames():
        filt = getattr(process,filterName)
        if type(filt).__name__=="EDFilter":
            if filt.type_()=="HLTElectronOneOEMinusOneOPFilterRegional":
               # print "old school tracking detected in %s" % pathName
                barrelCut = filt.getParameter("barrelcut").value()
                endcapCut = filt.getParameter("endcapcut").value()
                if barrelCut<printThres or endcapCut <printThres:
                    print "%s in %s : 1/E - 1/p cuts < %s (barrel) < %s (endcap) " % (filterName,pathName,barrelCut,endcapCut)
            
            if filt.type_()=="HLTEgammaGenericFilter":
                if filt.getParameter("nonIsoTag").getModuleLabel()!="": print "mis configured E/gamma filter %s in %s" % (filterName,pathName)
                if filt.getParameter("isoTag").getProductInstanceLabel()=="OneOESuperMinusOneOP":
                   # print "e/p filter detected"
                    barrelCut = filt.getParameter("thrRegularEB").value()
                    endcapCut = filt.getParameter("thrRegularEE").value()
                    if barrelCut<printThres or endcapCut < printThres:
                        print "%s in %s : 1/E - 1/p cuts < %s (barrel) < %s (endcap) " % (filterName,pathName,barrelCut,endcapCut)
                    
             
  


import argparse

parser = argparse.ArgumentParser(description='dumps the save tag filters of a menu')

parser.add_argument('hltMenuName',help="the python file containing the hlt menu, needs inputFiles=<name> (its due to cmssw var parsing, dont ask...)")
args = parser.parse_args()

hltMenuName=args.hltMenuName.rstrip(".py")
hltMenuName=hltMenuName.split("=")[1]
#print hltMenuName
import importlib

mod = importlib.import_module(hltMenuName)
process = getattr(mod,"process")
#from setSaveTags import *

printThres=99999.

for pathName in process.pathNames().split():
    printEPValues(process,pathName,printThres)


