from ROOT import TFile, TTree, TChain
from CMGTools.RootTools.Chain import Chain
from CMGTools.H2TauTau.proto.plotter.embed import embedScaleFactor


def prepareComponents(dir, config):
    '''Selects all components in configuration file. computes the integrated lumi
    from data components, and set it on the MC components.
    '''
    # all components in your configuration object (cfg)
    selComps = dict( [ (comp.name, comp) for comp in config.components ])
    totIntLumi = 0
    newSelComps = {}
    
    # loop on all components
    for comp in selComps.values():
        comp.dir = comp.name
        comp.realName = comp.name
        newSelComps[comp.name] = comp
        print comp.getWeight()

    # prepare weight dictionary, with all the components
    weights = dict( [ (comp.name,comp.getWeight()) \
                      for comp in newSelComps.values() ] )
    
    


    return newSelComps, weights
    
