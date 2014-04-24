import FWCore.ParameterSet.Config as cms

from CMGTools.Common.eventContent.everything_cff import *
from CMGTools.Susy.RazorMultiJet.razorMultiJetEventContent_cff import *
from CMGTools.Susy.common.eventContent_cff import eventContent as commonEventContent

susyEventContent = everything
#susyEventContent += multijetEventContent
#susyEventContent += RA1EventContent
#susyEventContent += RA2EventContent
#susyEventContent += razorEventContent
susyEventContent += razorMJjetEventContent
#susyEventContent += leptonicStopEventContent
#susyEventContent += LPEventContent
susyEventContent += commonEventContent
 
