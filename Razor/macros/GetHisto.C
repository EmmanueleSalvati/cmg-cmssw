TH1F* GetHisto(TString filename, TString var, TString label, TString cut = "MR > 0."){

  TFile *file         = new TFile(filename);
  RooDataSet *RMRTree = file->Get("RMRTree");
  RMRTree             -> reduce(cut);
  histo               = RMRTree->createHistogram(var);
  TH1F* test = histo->Clone(label);
  return test;

}

TH2F* GetHisto2D(TString filename, TString var1, TString var2 , TString label, TString cut = "MR > 0."){

  TFile *file         = new TFile(filename);
  RooDataSet *RMRTree = file->Get("RMRTree");
  RMRTree             -> reduce(cut);
  histo               = RMRTree->createHistogram(var1+":"+var2);
  TH2F* test = histo->Clone(label);
  return test;

}
