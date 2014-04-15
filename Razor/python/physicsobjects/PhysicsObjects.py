import math
import fnmatch

def printOut(objects):
    if len(objects)==0:
        return ''
    return '\n'.join( map( type(objects[0]).__str__, objects) )

from CMGTools.RootTools.physicsobjects.PhysicsObject import PhysicsObject
from CMGTools.RootTools.physicsobjects.TriggerObject import TriggerObject
from CMGTools.RootTools.physicsobjects.Lepton import Lepton
from CMGTools.RootTools.physicsobjects.Photon import Photon
from CMGTools.RootTools.physicsobjects.Muon import Muon
from CMGTools.RootTools.physicsobjects.Electron import Electron
from CMGTools.RootTools.physicsobjects.Jet import Jet
from CMGTools.RootTools.physicsobjects.GenParticle import GenParticle,GenLepton
from CMGTools.Razor.physicsobjects.DiHemisphere import DiHemisphere
from CMGTools.Razor.physicsobjects.Hemisphere import Hemisphere
from CMGTools.Razor.physicsobjects.Float import Float
