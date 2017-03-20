#!/bin/bash

# Need to run setup.sh first, and of course make sure /etc/hltd.conf is configured correctly.
# Also, need to make sure genTestFakeBuFromRAW_cfg.py is configured the way you want for 
# this test. For the fast track validation, usually you want to run over an HLTPhysics 
# sample and a sample related to the conditions change you are validating. For example, for 
# a change in ECal conditions, you might run over an EGamma sample.

echo "Running automated fast track validation script. Will compare rates and timing of menus using"
echo "reference and test global tags."
echo " "
sleep 5
 
###############################
testMenu=/cdaq/some/menu/HLT/V1
runNumber=123456
testGT=someTestGT
###############################

outputbasedir=/cmsnfsscratch/globalscratch/hltpro/fastTrack
mkdir -p $outputbasedir

## reference trial:
./newHiltonMenu.py $testMenu
./cleanGenerateAndRun.sh $runNumber skipRepack
cp -r /fff/BU0/output/run$runNumber $outputbasedir/reference_run$runNumber

## test trial:
./newHiltonMenu.py --GT $testGT $testMenu
./cleanGenerateAndRun.sh $runNumber # don't skip repack for test GT
cp -r /fff/BU0/output/run$runNumber $outputbasedir/test_run$runNumber
echo " "
echo "hltd jobs for both test and reference configuration completed. Check the following for correct output:"
echo "$outputbasedir/reference_run$runNumber"
echo "$outputbasedir/test_run$runNumber"
echo " "
echo "dumping rates..."
sleep 3
echo " "
../scripts/monitorRatesMultiLumi.py  $outputbasedir/reference_run$runNumber/streamHLTRates/data/run$runNumber*jsndata > ref_HLT_rates.txt
../scripts/monitorRatesMultiLumi.py  $outputbasedir/test_run$runNumber/streamHLTRates/data/run$runNumber*jsndata > test_HLT_rates.txt
#echo "Doing \"diff ref_HLT_rates.txt test_HLT_rates.txt\" ..."
#diff ref_HLT_rates.txt test_HLT_rates.txt
echo "HLT Rates of menu $testMenu using test GT $testGT dumped to test_HLT_rates.txt."
echo "Reference rates dumped to ref_HLT_rates.txt."
echo " "
echo "getting timing results..."
sleep 3

fastHadd add -o $outputbasedir/reference_run$runNumber/ref_DQM_hists.pb $outputbasedir/reference_run$runNumber/streamDQMHistograms/data/*.pb 
fastHadd add -o $outputbasedir/test_run$runNumber/test_DQM_hists.pb $outputbasedir/test_run$runNumber/streamDQMHistograms/data/*.pb
fastHadd convert -o ref_DQM_hists.root $outputbasedir/test_run$runNumber/ref_DQM_hists.pb
fastHadd convert -o test_DQM_hists.root $outputbasedir/test_run$runNumber/test_DQM_hists.pb

echo " "
echo "DQM histograms (including timing) dumped to:"
echo "ref_DQM_hists.root (reference hists)"
echo "test_DQM_hists.root (test GT $testGT)"
echo "Copy to lxplus and open in TBrowser to examine timing plots."
echo " "
echo "End of script."


