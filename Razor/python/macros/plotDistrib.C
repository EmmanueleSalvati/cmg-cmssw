

//void plotDistrib(TString mStop, TString mLSP, TString box)
void plotDistrib(TString mStop, TString mLSP,double mS, double mX, TString box)
{    
  gStyle->SetOptStat(0);
  
  TCanvas *c = new TCanvas("c","c", 1200, 400);
  TString name = "T2tt_mStop_"+mStop+"_"+mLSP+"_"+box;
  c->SetTitle(name);
  c->Divide(3,2);
  TLegend *leg = new TLegend(0.5,0.8,0.9,0.9);
  Double_t MRbins[9] = {500.0, 550.0, 650.0, 790.0, 1000, 1500, 2200, 3000, 4000.0};

  TString filenameTTbar = "/data/wreece/RazorMultijet_2012/231112/Datasets/MC/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola-Summer12_DR53X-PU_S10_START53_V7A-v1-wreece_231112-Combo_MR450.0_R0.173205080757_"+box+".root";
  TFile *fileTTbar = new TFile(filenameTTbar);
  RooDataSet *RMRTreeTTbar = fileTTbar -> Get("RMRTree");
  if (box == TString("BJetHS") || box == TString("BJetLS")){
    RMRTreeTTbar2 = RMRTreeTTbar -> reduce("MR > 500.");
    double scaleTTbar = 234. * 0.46 / 5399318. / (12. * 0.46 / 177151.);
  }
  else {
    RMRTreeTTbar2 = RMRTreeTTbar -> reduce("MR > 450.");
    double scaleTTbar = 234. * 0.16 / 5399318./ (12. * 0.16 / 177151.);
  }
  distrib1DMRTTbar  = RMRTreeTTbar2 -> createHistogram("MR");
  distrib1DMRTTbar  -> SetLineColor(kBlack);
  distrib1DMRTTbar  -> Scale(scaleTTbar);
  distrib1DRsqTTbar = RMRTreeTTbar2 -> createHistogram("Rsq");
  distrib1DRsqTTbar -> SetLineColor(kBlack);
  distrib1DRsqTTbar -> Scale(scaleTTbar);

  ///Signal
  if (box == TString("BJetHS") || box == TString("BJetLS")){
    TString filename = "/afs/cern.ch/work/l/lucieg/public/forRazorStop/SMS-T2tt_mStop-Combo_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY/Datasets/mLSP"+mLSP+"/SMS-T2tt_mStop-Combo_mLSP_"+mLSP+"_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY_MR500.0_R0.22360679775_"+mStop+"_"+mLSP+"_"+box+".root";
  }
  else
    TString filename = "/afs/cern.ch/work/l/lucieg/public/forRazorStop/SMS-T2tt_mStop-Combo_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY/Datasets/mLSP"+mLSP+"/SMS-T2tt_mStop-Combo_mLSP_"+mLSP+"_8TeV-Pythia6Z-Summer12-START52_V9_FSIM-v1-SUSY_MR350.0_R0.22360679775_"+mStop+"_"+mLSP+"_"+box+".root";
  
  TFile *file = new TFile(filename);
  
  RooDataSet *RMRTree = file->Get("RMRTree");
  if (box == TString("BJetHS") || box == TString("BJetLS")){
     RMRTree2=RMRTree->reduce("MR > 500.");
     double scaleT2tt = 1.;//12. * 0.46 / 177151.;
  }
  else {
    RMRTree2=RMRTree->reduce("MR > 450.");
    double scaleT2tt = 1.;//12. * 0.16 / 177151.;
  }
  
  RMRTree2->Print("V");
  distrib2D = RMRTree2->createHistogram("MR:Rsq");
  distrib2D->SetTitle("Rsq, MR plane ; MR(GeV); Rsq");
  c->cd(1);
  distrib2D->Draw("colz");
 
  
  distrib1DMR = RMRTree2->createHistogram("MR");
  distrib1DMR->SetTitle("MR  ; MR(GeV)); #events");
  c->cd(2);
  distrib1DMR -> SetLineColor(kRed);
  distrib1DMR -> Scale(scaleT2tt);
  distrib1DMR -> Rebin(8, "distrib1DMR2",MRbins);
  distrib1DMR -> SetMaximum(10000);
  c->GetPad(2) -> SetLogy();
  distrib1DMR -> Draw();
  //distrib1DMRTTbar  -> Rebin(8, "distrib1DMRTTbar2", MRbins);
  distrib1DMRTTbar -> Draw("SAME");
  double mDelta = TMath::Sqrt(mS*mS - mX*mX);// /(2.*mS);
  TLine *line = new TLine(mDelta,0.,mDelta,10000);
  line ->SetLineWidth(2);
  line->Draw("SAME");

  leg->AddEntry(distrib1DMR,"T2tt","lep");
  leg->AddEntry(distrib1DMRTTbar,"TTjets","lep");
  leg->Draw("SAME");

  distrib1DRsq = RMRTree2->createHistogram("Rsq");
  distrib1DRsq->SetTitle("Rsq  ; Rsq; #events");
  c->cd(3);
  distrib1DRsq -> SetLineColor(kRed);
  distrib1DRsq -> Scale(scaleT2tt);
  distrib1DRsq -> SetMaximum(10000);
  c->GetPad(3) -> SetLogy();
  distrib1DRsq -> Draw();
  distrib1DRsqTTbar -> Draw("SAME");
  leg->Draw("SAME");

  TString fullName = "plots/" + name +".png";
  c->SaveAs(fullName);

 
  //fileTTbar->Close();
  //file->Close();
}


 
