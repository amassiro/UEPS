{
 #include <algorithm>

 TFile* fCMS   = new TFile ("/tmp/amassiro/WW1Mevents_TUNE_CMS_dump_tree.root");
 TFile* fATLAS = new TFile ("/tmp/amassiro/WW1Mevents_TUNE_ATLAS_dump_tree.root");
//  TFile* fHerwig  = new TFile ("/tmp/amassiro/WW1Mevents_TUNE_Herwig_dump_tree_2.root");
//  TFile* fHerwig  = new TFile ("/tmp/amassiro/WW1Mevents_TUNE_Herwig_dump_tree.root");
 TFile* fHerwig  = new TFile ("/tmp/amassiro/WW1Mevents_TUNE_Herwig_UE_dump_tree.root");
 TFile* fCMS_Z2Lep = new TFile ("/tmp/amassiro/WW1Mevents_TUNE_CMS_Z2Lep_dump_tree.root");

 TTree* tCMS   =  (TTree*) fCMS   -> Get ("Analyzer/myTree");
 TTree* tATLAS =  (TTree*) fATLAS -> Get ("Analyzer/myTree");
 TTree* tHerwig  =  (TTree*) fHerwig  -> Get ("Analyzer/myTree");
 TTree* tCMS_Z2Lep   =  (TTree*) fCMS_Z2Lep -> Get ("Analyzer/myTree");

 Double_t X[200];
 Double_t Y_e0_CMS[200];
 Double_t Y_e0_ATLAS[200];
 Double_t Y_e0_Herwig[200];
 Double_t Y_e0_CMS_Z2Lep[200];
 Double_t Y_Delta_e0_up[200];
 Double_t Y_Delta_e0_do[200];

 Double_t Y_Delta_e0_overE_up[200];
 Double_t Y_Delta_e0_overE_do[200];

 Double_t Y_Delta_e0_overE_ATLAS_vs_CMS_up[200];
 Double_t Y_Delta_e0_overE_ATLAS_vs_CMS_do[200];

 Double_t Y_Delta_e0_overE_Pythia_vs_Herwig_up[200];
 Double_t Y_Delta_e0_overE_Pythia_vs_Herwig_do[200];

 Double_t Y_One[200];
 Double_t X_Zero[200];

 TString additionalCut = Form ("lhept1>20 && lhept2>20 && abs(lheeta1)<2.5 && abs(lheeta2)<2.5");
//  int n = 50;
 int n = 70;
 float totCMS   = tCMS   -> GetEntries( additionalCut.Data() );
 float totATLAS = tATLAS -> GetEntries( additionalCut.Data() );
 float totHerwig  = tHerwig  -> GetEntries( additionalCut.Data() );
 float totCMS_Z2Lep  = tCMS_Z2Lep  -> GetEntries( additionalCut.Data() );
 
 
 for (int i=0; i<n; i++) {
  double threshold =  0+i*2;
//   double threshold = 10+i*2;
  std::cout << " n[" << i << "]:: threshold = " << threshold;
// double threshold = 25+i;
  X[i] = threshold;
  TString s1 = Form ("%s && jetpt1<%f", additionalCut.Data(), threshold);

  float temp;

  temp = tCMS   -> GetEntries(s1.Data());    Y_e0_CMS[i]     = temp  / totCMS;
  temp = tATLAS -> GetEntries(s1.Data());    Y_e0_ATLAS[i]   = temp  / totATLAS;
  temp = tHerwig     -> GetEntries(s1.Data());  Y_e0_Herwig[i]  = temp  / totHerwig;
  temp = tCMS_Z2Lep  -> GetEntries(s1.Data());  Y_e0_CMS_Z2Lep[i]  = temp  / totCMS_Z2Lep;

  float delta[3];
  delta[0] = Y_e0_CMS[i] - Y_e0_ATLAS[i];
  delta[1] = Y_e0_CMS[i] - Y_e0_Herwig[i];
  delta[2] = Y_e0_CMS[i] - Y_e0_CMS_Z2Lep[i];

  Y_Delta_e0_do[i] =        *std::max_element(delta,delta+3);
  Y_Delta_e0_up[i] = -1. * (*std::min_element(delta,delta+3));

  Y_Delta_e0_overE_up[i] = Y_Delta_e0_up[i] / Y_e0_CMS[i];
  Y_Delta_e0_overE_do[i] = Y_Delta_e0_do[i] / Y_e0_CMS[i];

  if (delta[0]>0) {
   Y_Delta_e0_overE_ATLAS_vs_CMS_up[i] = delta[0] / Y_e0_CMS[i];
   Y_Delta_e0_overE_ATLAS_vs_CMS_do[i] = 0;
  }
  else {
   Y_Delta_e0_overE_ATLAS_vs_CMS_up[i] = 0;
   Y_Delta_e0_overE_ATLAS_vs_CMS_do[i] = -delta[0] / Y_e0_CMS[i];
  }

  if (delta[1]>0) {
   Y_Delta_e0_overE_Pythia_vs_Herwig_up[i] = delta[1] / Y_e0_CMS[i];
   Y_Delta_e0_overE_Pythia_vs_Herwig_do[i] = 0;
  }
  else {
   Y_Delta_e0_overE_Pythia_vs_Herwig_up[i] = 0;
   Y_Delta_e0_overE_Pythia_vs_Herwig_do[i] = -delta[1] / Y_e0_CMS[i];
  }

 //   std::cout << " Y_Delta_e0_overE_ATLAS_vs_CMS_up[" << i << "] = " << Y_Delta_e0_overE_ATLAS_vs_CMS_up[i] << std::endl;
  Y_One[i]  = 1.;
  X_Zero[i] = 0.;

  std::cout << " :: eff[" << s1.Data() << "] = " << Y_e0_CMS[i] << std::endl;
 }


 //--------------------------
 TGraph* g_e0_CMS   = new TGraph(n,X,Y_e0_CMS);
 TGraph* g_e0_ATLAS = new TGraph(n,X,Y_e0_ATLAS);
 TGraph* g_e0_Herwig  = new TGraph(n,X,Y_e0_Herwig);
 TGraph* g_e0_CMS_Z2Lep  = new TGraph(n,X,Y_e0_CMS_Z2Lep);

 g_e0_CMS->SetMarkerSize(1);
 g_e0_CMS->SetMarkerStyle(20);
 g_e0_CMS->SetMarkerColor(kRed);
 g_e0_CMS->SetLineColor(kRed);
 g_e0_CMS->GetXaxis()->SetTitle("jet p_{T} threshold [GeV]");
 g_e0_CMS->GetYaxis()->SetTitle("0 jet efficiency");

 g_e0_ATLAS->SetMarkerSize(1);
 g_e0_ATLAS->SetMarkerStyle(21);
 g_e0_ATLAS->SetMarkerColor(kBlue);
 g_e0_ATLAS->SetLineColor(kBlue);
 g_e0_ATLAS->GetXaxis()->SetTitle("jet p_{T} threshold [GeV]");

 g_e0_Herwig->SetMarkerSize(1);
 g_e0_Herwig->SetMarkerStyle(22);
 g_e0_Herwig->SetMarkerColor(kGreen);
 g_e0_Herwig->SetLineColor(kGreen);
 g_e0_Herwig->GetXaxis()->SetTitle("jet p_{T} threshold [GeV]");

 g_e0_CMS_Z2Lep->SetMarkerSize(1);
 g_e0_CMS_Z2Lep->SetMarkerStyle(23);
 g_e0_CMS_Z2Lep->SetMarkerColor(kTeal);
 g_e0_CMS_Z2Lep->SetLineColor(kTeal);
 g_e0_CMS_Z2Lep->GetXaxis()->SetTitle("jet p_{T} threshold [GeV]");

 TLegend* leg = new TLegend(0.1,0.7,0.5,0.9);
//  leg->SetHeader("The Legend Title");
 leg->AddEntry(g_e0_Herwig,"Herwig PS","lp");
 leg->AddEntry(g_e0_CMS,"Pythia CMS tune","lp");
 leg->AddEntry(g_e0_ATLAS,"Pythia ATLAS tune","lp");
 leg->AddEntry(g_e0_CMS_Z2Lep,"Pythia CMS Z2*Lep tune","lp");
 leg->SetFillColor(0);

 TCanvas* ce0 = new TCanvas ("ce0","ce0",800,600);

 TMultiGraph *mg = new TMultiGraph();
 mg->Add(g_e0_CMS,"lp");
 mg->Add(g_e0_ATLAS,"lp");
 mg->Add(g_e0_Herwig,"lp");
 mg->Add(g_e0_CMS_Z2Lep,"lp");
 mg->Draw("a");
 mg->GetXaxis()->SetTitle("jet p_{T} threshold [GeV]");
 mg->GetYaxis()->SetTitle("0 jet efficiency");
 leg->Draw();
 ce0->SetGrid();


 TGraphAsymmErrors* grErr =  new TGraphAsymmErrors(n, X, Y_One, X_Zero, X_Zero, Y_Delta_e0_overE_do, Y_Delta_e0_overE_up);
 TGraphAsymmErrors* grErr_ATLAS_vs_CMS =  new TGraphAsymmErrors(n, X, Y_One, X_Zero, X_Zero, Y_Delta_e0_overE_ATLAS_vs_CMS_do, Y_Delta_e0_overE_ATLAS_vs_CMS_up);
 TGraphAsymmErrors* grErr_Pythia_vs_Herwig =  new TGraphAsymmErrors(n, X, Y_One, X_Zero, X_Zero, Y_Delta_e0_overE_Pythia_vs_Herwig_do, Y_Delta_e0_overE_Pythia_vs_Herwig_up);
 TCanvas* ce0relative = new TCanvas ("ce0relative","ce0relative",800,600);
 grErr->SetMarkerSize(1);
 grErr->SetMarkerStyle(21);
 grErr->SetMarkerColor(kBlack);
 grErr->SetLineColor(kBlack);
 grErr->GetXaxis()->SetTitle("jet p_{T} threshold [GeV]");
 grErr->GetYaxis()->SetTitle("Relative error on efficiency");

 grErr->Draw ("apl");

 grErr_ATLAS_vs_CMS->SetMarkerSize(0);
 grErr_ATLAS_vs_CMS->SetMarkerStyle(21);
 grErr_ATLAS_vs_CMS->SetMarkerColor(kBlue);
 grErr_ATLAS_vs_CMS->SetLineColor(kBlue);
 grErr_ATLAS_vs_CMS->SetLineStyle(2);
 grErr_ATLAS_vs_CMS->SetLineWidth(2);
 grErr_ATLAS_vs_CMS->Draw ("pl");

 grErr_Pythia_vs_Herwig->SetMarkerSize(0);
 grErr_Pythia_vs_Herwig->SetMarkerStyle(21);
 grErr_Pythia_vs_Herwig->SetMarkerColor(kRed);
 grErr_Pythia_vs_Herwig->SetLineColor(kRed);
 grErr_Pythia_vs_Herwig->SetLineStyle(3);
 grErr_Pythia_vs_Herwig->SetLineWidth(2);
 grErr_Pythia_vs_Herwig->Draw ("pl");
 ce0relative->SetGrid();


 //--------------------------
 TH1F* h_e0_CMS   = new TH1F("CMS","",50,0,200);
 TH1F* h_e0_ATLAS = new TH1F("ATLAS","",50,0,200);
 TH1F* h_e0_Herwig  = new TH1F("Herwig","",50,0,200);

//  TH1F* h_e0_CMS   = new TH1F("CMS","",n,10,10+n*2X);
//  TH1F* h_e0_ATLAS = new TH1F("ATLAS","",n,10,10+n*2X);
//  TH1F* h_e0_Herwig  = new TH1F("Herwig","",n,10,10+n*2X);

 tCMS->Draw("jetpt1 >> CMS","","goff");
 tATLAS->Draw("jetpt1 >> ATLAS","","goff");
 tHerwig->Draw("jetpt1 >> Herwig","","goff");

 h_e0_CMS->SetMarkerColor(kRed);
 h_e0_CMS->SetLineWidth(2);
 h_e0_CMS->SetLineColor(kRed);
 h_e0_CMS->GetXaxis()->SetTitle("jet p_{T} [GeV]");
 h_e0_CMS->GetYaxis()->SetTitle("evetns");

 h_e0_ATLAS->SetMarkerColor(kBlue);
 h_e0_ATLAS->SetLineColor(kBlue);
 h_e0_ATLAS->SetLineWidth(2);
 h_e0_ATLAS->GetXaxis()->SetTitle("events");

 h_e0_Herwig->SetMarkerColor(kGreen);
 h_e0_Herwig->SetLineColor(kGreen);
 h_e0_Herwig->SetLineWidth(2);
 h_e0_Herwig->GetXaxis()->SetTitle("events");

 TCanvas* cn = new TCanvas ("cn","cn",800,600);
 h_e0_CMS->DrawNormalized();
 h_e0_ATLAS->DrawNormalized("same");
 h_e0_Herwig->DrawNormalized("same");
 leg->Draw();
 cn->SetGrid();

}




