///////////////////////////////////////////////////////////////////////
// Author: David Bjergaard
// 
// Library for Generic Sideband Subtraction Methods.
//
// This library is designed to be a tool which serves two purposes.
// Its primary purpose is to provide a generic framework for doing
// sideband subtraction.  It will also plug into current tag and probe
// modules to prevent code duplication and redundancy.  Many of the
// methods are  inspired heavily by current TagAndProbe code.
//
///////////////////////////////////////////////////////////////////////

#include "PhysicsTools/Utilities/interface/SideBandSubtraction.h"
// System includes
#include <iostream>
#include <sstream>

// ROOT includes
#include <TCanvas.h>
#include <TFile.h>
#include <TF1.h>
#include <TH1F.h>
#include <TString.h>
#include <TKey.h>
#include <TClass.h>

// RooFit includes
#include <RooFitResult.h>
#include <RooRealVar.h>
#include "RooAbsPdf.h"
#include "RooDataSet.h"
#include "RooPlot.h"

using namespace RooFit;
using std::cout;
using std::endl;
using std::string;
using std::vector;

template <class T>
inline std::string stringify(const T& t)
{
  std::ostringstream o;
  if (!(o << t))
    return "err";
  return o.str();
} 
Double_t SideBandSubtract::getYield(std::vector<SbsRegion> Regions, RooAbsPdf *PDF)
{
  Double_t yield=0;
  RooAbsReal* intPDF;
  for(unsigned int i=0; i < Regions.size(); i++)
    {
      if(verbose)
	cout<<"Integrating over Range: "<<Regions[i].RegionName<<" from "<<Regions[i].min<<" to "<<Regions[i].max<<endl;
      intPDF = PDF->createIntegral(*SeparationVariable, Range(Regions[i].RegionName.c_str()));
      yield += intPDF->getVal();
      if(verbose)
	cout<<"Current yield: "<<yield<<endl;
    }
  return yield;
}
static void setHistOptions(TH1F* histo, string name, string title, string axis_label)
{

  histo->SetName(name.c_str());
  histo->SetTitle(title.c_str());
  if(axis_label == "GeV/c^2")
    axis_label = "Mass (" + axis_label + ")";
  if(axis_label == "GeV/c")
    axis_label = "Momentum (" + axis_label + ")";
  histo->GetXaxis()->SetTitle(axis_label.c_str());
}
int SideBandSubtract::doSubtraction(RooRealVar* variable, Double_t stsratio,Int_t index) //stsratio -> signal to sideband ratio
{
  TH1F* SideBandHist = (TH1F*)BaseHistos[index]->Clone();
  setHistOptions(SideBandHist,(string)variable->GetName()+"Sideband",(string)SideBandHist->GetTitle() + " Sideband",(string)variable->getUnit());

  TH1F* SignalHist = (TH1F*)BaseHistos[index]->Clone();
  setHistOptions(SignalHist,(string)variable->GetName()+"SignalHist",(string)SignalHist->GetTitle() + " Raw Signal",(string)variable->getUnit());

  //Begin a loop over the data to fill our histograms. I should figure
  //out how to do this in one shot to avoid a loop
  //O(N_vars*N_events)...
  TIterator* iter = (TIterator*) Data->get()->createIterator();
  RooAbsArg *var=NULL;
  RooRealVar *sep_var=NULL;
  while((var = (RooAbsArg*)iter->Next()))
    {
      if((string)var->GetName()==(string)SeparationVariable->GetName())
	{
	  sep_var = (RooRealVar*)var;
	  break;
	}
    }
  for(int i=0; i < Data->numEntries(); i++)
    {
      Data->get(i);
      Double_t value = variable->getVal();
      Double_t cutval = sep_var->getVal();

      for(unsigned int j=0; j < SideBandRegions.size(); j++) //UGLY!  Find better solution!
	{
	  if(cutval > SideBandRegions[j].min && cutval < SideBandRegions[j].max)
	    SideBandHist->Fill(value);
	}
      for(unsigned int j=0; j < SignalRegions.size(); j++)
	{
	  if(cutval > SignalRegions[j].min && cutval < SignalRegions[j].max)
	    SignalHist->Fill(value);
	}
    }
  //Save pre-subtracted histo
  SignalHist->Sumw2(); SideBandHist->Sumw2(); 
  RawHistos.push_back(*SignalHist);

  SignalHist->Add(SideBandHist, -stsratio);

  newtitle = oldtitle + " SBS Signal";  
  SignalHist->SetTitle(newtitle.c_str());
  //Save subtracted histo
  SBSHistos.push_back(*SignalHist);
  //Save Sideband histo
  SideBandHistos.push_back(*SideBandHist);

  if(SideBandHist) delete SideBandHist;
  return 0;
}
static void print_histo(TH1F* plot, string outname)
{
  TCanvas genericCanvas;
  plot->Draw("E1P0");
  outname = outname + ".eps";
  genericCanvas.SaveAs(outname.c_str());
  outname.replace(outname.size()-3,3,"gif");
  genericCanvas.SaveAs(outname.c_str());
}
void SideBandSubtract::printResults(string prefix)
{//handles *all* printing
  //spool over vectors of histograms and print them, then print
  //separation variable plots and the results text file.

  string filename; //output file name
  for(unsigned int i=0; i < RawHistos.size(); ++i)
    {
      filename=prefix + "Raw_" + (string)RawHistos[i].GetName();
      print_histo(&RawHistos[i], filename);
    }
  for(unsigned int i=0; i < SBSHistos.size(); ++i)
    {
      filename=prefix + "SBS_" + (string)RawHistos[i].GetName();
      print_histo(&SBSHistos[i], filename);
    }
  if(verbose)
    {
      for(unsigned int i=0; i < SideBandHistos.size(); ++i)
	{
	  filename=prefix + "SideBand_" + (string)RawHistos[i].GetName();
	  print_histo(&SideBandHistos[i], filename);
	}
    }

  string outname = prefix + (string)SeparationVariable->GetName() + "_fitted.eps";
  RooPlot *SepVarFrame = SeparationVariable->frame();
  Data->plotOn(SepVarFrame);
  ModelPDF->plotOn(SepVarFrame);
  TCanvas Canvas;
  SepVarFrame->Draw();
  Canvas.SaveAs(outname.c_str());
  outname.replace(outname.size()-3,3,"gif");
  Canvas.SaveAs(outname.c_str());

  string result_outname = prefix + "_fit_results.txt";
  ofstream output(result_outname.c_str(),ios::out);
  if(!output)
    {
      cout <<"ERROR: Could not open file for writing!\n";
      return;
    }

  if(fit_result!=NULL)
    {
#if ROOT_VERSION_CODE <= ROOT_VERSION(5,19,0)
      fit_result->printToStream(output,Verbose);
#else
      fit_result->printMultiline(output,kTRUE);
#endif
    }
}


void SideBandSubtract::saveResults(string outname)
{
  //saves the ephemeral stuff to a root file for future
  //use/modification (ie everything printed by printResults())

  TFile output(outname.c_str(),"UPDATE"); //open the output file,
					  //create it if it doesn't
					  //exist
  //Since keys are only available from files on disk, we need to write
  //out a new file.  If the file already existed, then we opened to
  //update, and are writing nothing new.  
  output.Write();
  TString dirname;
  TIter nextkey(output.GetListOfKeys());
  TKey *key;
  
  while((key=(TKey*)nextkey.Next()))
    {

      if(key==NULL)
	break;
      TObject *obj = key->ReadObj();
      if(obj->IsA()->InheritsFrom("TDirectory"))
	  dirname=obj->GetName();

    }

  if(dirname=="")
    {
      //we didn't find any directories so, we'll make a new one
      output.mkdir("run0","Run 0");
      output.cd("run0");
    }
  else
    {
      //manipulate last dir string, make a new one, and get ready to fill
      dirname.Remove(0,3);
      Int_t run_num = dirname.Atoi();
      run_num++;
      dirname = "run" + stringify(run_num);
      output.mkdir(dirname.Data(),("Run "+stringify(run_num)).c_str());
      output.cd(dirname.Data());
    }

  //these should all be the same size, but to be pedantic we'll loop
  //over each one individually...
  for(unsigned int i=0; i < SideBandHistos.size(); ++i)
      SideBandHistos[i].Write();
  for(unsigned int i=0; i < RawHistos.size(); ++i)
      RawHistos[i].Write();
  for(unsigned int i=0; i < SBSHistos.size(); ++i)
      SBSHistos[i].Write();

  RooPlot *sep_varFrame = SeparationVariable->frame();
  Data->plotOn(sep_varFrame);
  ModelPDF->plotOn(sep_varFrame);
  BackgroundPDF->plotOn(sep_varFrame);
  sep_varFrame->Write();

  output.Write();

}
void SideBandSubtract::setDataSet(RooDataSet* newData)
{
  if(newData!=NULL)
    Data=newData;
}
void SideBandSubtract::print_plot(RooRealVar* printVar,string outname)
{
  RooPlot *genericFrame = printVar->frame();
  Data->plotOn(genericFrame);
  ModelPDF->plotOn(genericFrame);
  TCanvas genericCanvas;
  genericFrame->Draw();
  outname = outname + ".eps";
  genericCanvas.SaveAs(outname.c_str());
  outname.replace(outname.size()-3,3,"gif");
  genericCanvas.SaveAs(outname.c_str());
}

SideBandSubtract::SideBandSubtract(RooAbsPdf *model_shape, 
				   RooAbsPdf *bkg_shape, 
				   RooDataSet* data,
				   RooRealVar* sep_var,
				   const vector<TH1F*> base,
				   bool verb
				   )
  : BackgroundPDF(bkg_shape), 
    ModelPDF(model_shape), 
    Data(data),
    SeparationVariable(sep_var),
    verbose(verb),
    SignalRegions(),
    SideBandRegions(),
    SideBandHistos(0),
    RawHistos(0),
    SBSHistos(0),
    BaseHistos(base),
    fit_result(0),
    SignalSidebandRatio(0)
{
  //We aren't making anything here, so we just assign whats handed to us and leave...
}
SideBandSubtract::~SideBandSubtract()
{
  //**WARNING** 

  // We don't delete objects that we don't own (duh) so, all of our
  // pointers just hang out and get handled by other people :)

}
void SideBandSubtract::addSignalRegion(Double_t min, Double_t max)
{
  SbsRegion signal;
  signal.min=min;
  signal.max=max;
  signal.RegionName="Signal" + stringify(SignalRegions.size());
  SeparationVariable->setRange(signal.RegionName.c_str(),signal.min,signal.max);
  SignalRegions.push_back(signal);
  return;
}
void SideBandSubtract::addSideBandRegion(Double_t min, Double_t max)
{
  SbsRegion sideband;
  sideband.min=min;
  sideband.max=max;
  sideband.RegionName="SideBand" + stringify(SideBandRegions.size());
  SeparationVariable->setRange(sideband.RegionName.c_str(),sideband.min,sideband.max);
  SideBandRegions.push_back(sideband);
  return;
}
int SideBandSubtract::doGlobalFit()
{
  if(verbose)
    cout <<"Beginning SideBand Subtraction\n";

  fit_result = ModelPDF->fitTo(*Data,"r");

  Double_t SideBandYield=getYield(SideBandRegions,BackgroundPDF);
  Double_t  BackgroundInSignal=getYield(SignalRegions,BackgroundPDF);

  SignalSidebandRatio = BackgroundInSignal/SideBandYield;
  if(verbose)
    {
      cout <<"Finished fitting background!\n";
      cout <<"Attained a Signal to Sideband ratio of: " << SignalSidebandRatio<<endl;
    }
  //I can't see a way around a double loop for each variable.  Maybe I
  //can get a C++/RooFit guru to save me the trouble here?


  //need to grab sbs objects after each global fit, because they get reset
  resetSBSProducts();
  TIterator* iter = (TIterator*) Data->get()->createIterator();
  RooAbsArg *variable;
  while((variable = (RooAbsArg*)iter->Next()))
    {
      for(unsigned int i=0; i < BaseHistos.size(); i++)
	{
	  if((string)variable->GetName()!=(string)SeparationVariable->GetName() 
	     && (string)variable->GetName()==(string)BaseHistos[i]->GetName())
	    doSubtraction((RooRealVar*)variable,SignalSidebandRatio,i);
	}
    }

  //  clean up our memory...
  if(variable)      delete variable;
  if(iter)          delete iter;
  return 0;
}
void SideBandSubtract::doFastSubtraction(TH1F &Total, TH1F &Result, SbsRegion& leftRegion, SbsRegion& rightRegion)
{
  Int_t binMin = Total.FindBin(leftRegion.max,0.0,0.0);
  Int_t binMax = Total.FindBin(leftRegion.min,0.0,0.0);
  double numLeft = Total.Integral( binMin, binMax );

  binMin = Total.FindBin(rightRegion.max,0.0,0.0);
  binMax = Total.FindBin(rightRegion.min,0.0,0.0);
  double numRight = Total.Integral( binMin, binMax );
  
  const unsigned int nbinsx = Total.GetNbinsX();
  const double x1 = (leftRegion.max + leftRegion.min)/2.0;
  const double x2 = (rightRegion.max + rightRegion.min)/2.0;

  const double y1 = numLeft/(leftRegion.max - leftRegion.min);
  const double y2 = numRight/(rightRegion.max - rightRegion.min);
    
  const double Slope = (y2 - y1)/(x2 - x1);
  const double Intercept = y1 - Slope*x1;
  // Evantually we want to handle more complicated functions, but for
  // now... just use a linear one
  TF1 function("sbs_function_line", "[0]*x + [1]",Total.GetMinimum(), Total.GetMaximum());
  for ( unsigned int binx = 1;  binx <= nbinsx; ++binx ) 
    {
      double binWidth = Total.GetBinWidth(binx);
      function.SetParameter(0,Slope*binWidth);
      function.SetParameter(1,Intercept*binWidth);

      double xx = Total.GetBinCenter(binx);
      double cu = Total.GetBinContent(binx) - function.Eval(xx);    
      // TODO: Propogate the  error on the parameters in function.
      double error1 = Total.GetBinError(binx);
    
      Result.SetBinContent(binx, cu);
      Result.SetBinError(binx, error1);
    }
  Result.SetEntries(Result.Integral() );
}
RooFitResult* SideBandSubtract::getFitResult()
{
  return fit_result;
}
vector<TH1F> SideBandSubtract::getRawHistos()
{
  return RawHistos;
}
vector<TH1F> SideBandSubtract::getSBSHistos()
{
  return SBSHistos;
}
Double_t SideBandSubtract::getSTSRatio()
{
  return SignalSidebandRatio;
}
void SideBandSubtract::resetSBSProducts()
{
  SideBandHistos.erase(SideBandHistos.begin(),SideBandHistos.end());
  RawHistos.erase(RawHistos.begin(),RawHistos.end());
  SBSHistos.erase(SBSHistos.begin(),SBSHistos.end()); 
}
