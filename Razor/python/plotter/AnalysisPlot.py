import os, re
from fnmatch import fnmatch
import copy

from ROOT import TFile, TH1F, TPaveText, TPad, gStyle, TLine, kBlue, kOrange

from CMGTools.RootTools.DataMC.AnalysisDataMCPlot import AnalysisDataMC
from CMGTools.RootTools.fwlite.Weight import Weight
from CMGTools.RootTools.fwlite.Weight import printWeights
from CMGTools.RootTools.Style import *


class AnalysisPlot( AnalysisDataMC ):

    keeper = {}
    HINDEX = 0

    def __init__(self, varName, directory, selComps, weights,
                 bins = None, xmin = None, xmax=None, cut = '',weight=1,
                 treeName=None, analyzerName=None):
        '''Data/MC plotter adapted to razor multijet analysis.
        The plotter takes a collection of trees in input. The trees are found according
        to the dictionary of selected components selComps.
        The global weighting information for each component is read from the weights dictionary.
        The weight parameter is the name of an event weight variable that can be found in the tree.
        The default is "weight" (full event weight computed at python analysis stage),
        but you can build up the weight string you want before calling this constructor.
        To do an unweighted plot, choose weight="1" (the string, not the number).        
        '''
        if treeName is None:
            treeName = 'MultiJetAnalysis'
        self.treeName = treeName
        self.selComps = []
        for layer, (compName, comp) in enumerate( sorted(selComps.iteritems()) ) :
            for subdir in os.listdir(directory +'/'+comp.dir) :
                if (subdir == 'config.txt') or (subdir == 'config.pck'): continue
                self.selComps.append({"layer":layer, "compName" :subdir, "comp":compName})
        self.varName = varName
        self.lines = {}
        self.cut = cut
        self.eventWeight = weight
        self.bins = bins
        self.xmin = xmin
        self.xmax = xmax
        self.analyzerName = self.treeName
        label = re.sub(' ','', cut)
        self.file = open(options.hist + label+'.txt','w')
        super(AnalysisPlot, self).__init__(varName, directory, weights)

        self.legendBorders = 0.651, 0.463, 0.895, 0.892


    def _mDeltaLine(self, tree, compName):
        tmp = TH1F( 'tmp', '', self.bins, self.xmin, self.xmax )
        tree.Draw("mDelta>>tmp")
        mDelta = tmp.GetMean()
        self.lines[compName] = self.line(mDelta,0., mDelta, 0.05,self._GetHistPref( compName ))

    def line(self, x1, x2, y1, y2, pref):
        tline = TLine(x1, x2, y1, y2)
        tline.SetLineColor(pref['style'].markerColor)
        tline.SetLineWidth(4)
        return tline

    def _BuildHistogram(self, tree, comp, compName, varName, cut, layer ):
        '''Build one histogram, for a given component'''

        histName = '_'.join( [compName, self.varName] )

        hist = None
        hist = TH1F( histName, '', self.bins, self.xmin, self.xmax )
        hist.Sumw2()
        weight = self.eventWeight
        if tree == None:
            raise ValueError('tree does not exist for component '+compName)
        var = varName
        tree.Project( histName, var, '{cut}'.format(cut=cut) )
        hist.SetStats(1)
        hist.SetTitle(var)
        componentName = compName
        legendLine = re.sub('Analysis_','',compName)
        self.AddHistogram( componentName, hist, layer, legendLine)
        self.Hist(componentName).realName = compName
        self.Hist(componentName).stack = True
        self._mDeltaLine(tree, compName)
       

    def _ReadHistograms(self, directory):
        '''Build histograms for all components.'''
        for item in  self.selComps  :
            fileName = '/'.join([ directory,
                                  item['comp'],
                                  item['compName'],
                                  '{analyzerName}_tree.root'.format(analyzerName=self.analyzerName)] )

            file = self.__class__.keeper[ fileName + str(self.__class__.HINDEX) ] = TFile(fileName) 
            self.__class__.HINDEX+=1

            tree = file.Get( self.treeName )

            self._BuildHistogram(tree, item['compName'], item['comp'], self.varName,
                                 self.cut, item['layer'] )     

        self._ApplyWeights()
        self._ApplyPrefs()

        for item in  self.selComps  :
            componentName = item['comp']
            self.file.write('\n')
            self.file.write(componentName)
            self.file.write('\n')
            self.file.write(str(self.Hist(componentName).Yield()))
          
    def _InitPrefs(self):
        '''Definine preferences for each component'''
        self.histPref = {}
        #self.histPref['T2tt*'] = {'style':sBlackSquares, 'layer':2}
        i=0
        for mStop in range(200, 900, 100):
            i+=1
            style = Style(markerColor=kOrange+i, fillColor=kOrange+i, lineColor=kOrange+i)
            self.histPref['T2tt_'+str(mStop)] = {'style':style, 'layer':6, 'stack':False}
        i=0
        for label in ['100','250','500','1000']:
            style = Style(markerColor=kBlue+i, fillColor=kBlue+i, lineColor=kBlue+i)
            self.histPref['QCD'+label] = {'style':style, 'layer':1+i, 'stack':True} 
            i+=1
        
        self.histPref['TTJets'] = {'style':sGreen, 'layer':5, 'stack':False}

      #  self.histPref['*'] = {'style':sYellow, 'layer':3}  
       

def filterComps(comps, filterString=None): 
    filteredComps = copy.copy(comps)
    if filterString:
        filters = filterString.split(';')
        filteredComps = {}
        for comp in comps.values():
            for filter in filters:
                pattern = re.compile( filter )
                if pattern.search( comp.name ):
                    filteredComps[comp.name] = comp 
    return filteredComps


if __name__ == '__main__':


    import copy
    import imp
    import re 
    from optparse import OptionParser
    from CMGTools.RootTools.RootInit import *
    from CMGTools.H2TauTau.proto.plotter.rootutils import buildCanvas, draw
    from CMGTools.Razor.plotter.prepareComponents import prepareComponents

    gStyle.SetOptStat(0)
    
    parser = OptionParser()
    parser.usage = '''
    %prog <anaDir> <cfgFile>

    cfgFile: analysis configuration file, see CMGTools.H2TauTau.macros.MultiLoop
    anaDir: analysis directory containing all components, see CMGTools.H2TauTau.macros.MultiLoop.
    hist: histogram you want to plot
    '''
    parser.add_option("-H", "--hist", 
                      dest="hist", 
                      help="histogram list",
                      default='mt')
    parser.add_option("-C", "--cut", 
                      dest="cut", 
                      help="cut to apply in TTree::Draw",
                      default='')
    parser.add_option("-n", "--nbins", 
                      dest="nbins", 
                      help="Number of bins",
                      default=None)
    parser.add_option("-m", "--min", 
                      dest="xmin", 
                      help="xmin",
                      default=None)
    parser.add_option("-M", "--max", 
                      dest="xmax", 
                      help="xmax",
                      default=None)
    parser.add_option("-f", "--filter", 
                      dest="filter", 
                      help="Regexp filter to select components",
                      default=None)
    parser.add_option("-t", "--treeName", 
                      dest="treeName", 
                      help="treeName",
                      default=None)
    parser.add_option("-a", "--analyzerName", 
                      dest="analyzerName", 
                      help="analyzerName",
                      default=None)

    
    (options,args) = parser.parse_args()
    if len(args) != 2:
        parser.print_help()
        sys.exit(1)

    NBINS = int(options.nbins)
    XMIN  = float(options.xmin)
    XMAX  = float(options.xmax)

    cutstring = options.cut
    
    weight='weight'
    anaDir = args[0].rstrip('/')
        
    cfgFileName = args[1]
    file = open( cfgFileName, 'r' )
    cfg = imp.load_source( 'cfg', cfgFileName, file)


    selComps, weights = prepareComponents(anaDir, cfg.config)
    filteredComps = filterComps(selComps, options.filter)
     #can, pad, padr = buildCanvas()
    plot = AnalysisPlot( options.hist, anaDir, filteredComps, weights, NBINS, XMIN, XMAX, options.cut,
                       weight=weight, treeName=options.treeName, analyzerName=options.analyzerName )
    gPad.SetLogy()
    plot.Draw()
#    plot.DrawStack()
    #plot.DrawNormalized()
   ##  for key, line in  plot.lines.iteritems():
##         line.Draw("SAME")
    label = re.sub(' ','', options.cut)
    gPad.SaveAs(options.hist + label+'.png')

    #plot.DrawRatio()
   
