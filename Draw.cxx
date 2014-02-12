{
 #include <algorithm>

 TFile* fCMS   = new TFile ("/tmp/amassiro/WW1Mevents_TUNE_CMS_dump_tree.root");
 TFile* fATLAS = new TFile ("/tmp/amassiro/WW1Mevents_TUNE_ATLAS_dump_tree.root");
 TFile* fNoUE  = new TFile ("/tmp/amassiro/WW1Mevents_TUNE_NoUE_dump_tree.root");

 TTree* tCMS   =  (TTree*) fCMS   -> Get ("Analyzer/myTree");
 TTree* tATLAS =  (TTree*) fATLAS -> Get ("Analyzer/myTree");
 TTree* tNoUE  =  (TTree*) fNoUE  -> Get ("Analyzer/myTree");

 Double_t X[200];
 Double_t Y_e0_CMS[200];
 Double_t Y_e0_ATLAS[200];
 Double_t Y_e0_NoUE[200];
 Double_t Y_Delta_e0_up[200];
 Double_t Y_Delta_e0_do[200];

 Double_t Y_Delta_e0_overE_up[200];
 Double_t Y_Delta_e0_overE_do[200];

 Double_t Y_One[200];
 Double_t X_Zero[200];

 int n = 30;
 float totCMS   = tCMS   -> GetEntries();
 float totATLAS = tATLAS -> GetEntries();
 float totNoUE  = tNoUE  -> GetEntries();

 for (int i=0; i<n; i++) {
  double threshold = 10+i*2;
  std::cout << " n[" << i << "]:: threshold = " << threshold;
// double threshold = 25+i;
  X[i] = threshold;
  TString s1 = Form ("jetpt1<%f",threshold);

  float temp;

  temp = tCMS   -> GetEntries(s1.Data()); Y_e0_CMS[i]   = temp  / totCMS;
  temp = tATLAS -> GetEntries(s1.Data()); Y_e0_ATLAS[i] = temp  / totATLAS;
  temp = tNoUE  -> GetEntries(s1.Data()); Y_e0_NoUE[i]  = temp  / totNoUE;

  float delta[2];
  delta[0] = Y_e0_CMS[i] - Y_e0_ATLAS[i];
  delta[1] = Y_e0_CMS[i] - Y_e0_NoUE[i];

  Y_Delta_e0_do[i] =        *std::max_element(delta,delta+2);
  Y_Delta_e0_up[i] = -1. * (*std::min_element(delta,delta+2));

  Y_Delta_e0_overE_up[i] = Y_Delta_e0_up[i] / Y_e0_CMS[i];
  Y_Delta_e0_overE_do[i] = Y_Delta_e0_do[i] / Y_e0_CMS[i];

  Y_One[i]  = 1.;
  X_Zero[i] = 0.;

  std::cout << " :: eff[" << s1.Data() << "] = " << Y_e0_CMS[i] << std::endl;
 }


 //--------------------------
 TGraph* g_e0_CMS   = new TGraph(n,X,Y_e0_CMS);
 TGraph* g_e0_ATLAS = new TGraph(n,X,Y_e0_ATLAS);
 TGraph* g_e0_NoUE  = new TGraph(n,X,Y_e0_NoUE);

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

 g_e0_NoUE->SetMarkerSize(1);
 g_e0_NoUE->SetMarkerStyle(22);
 g_e0_NoUE->SetMarkerColor(kGreen);
 g_e0_NoUE->SetLineColor(kGreen);
 g_e0_NoUE->GetXaxis()->SetTitle("jet p_{T} threshold [GeV]");

 TLegend* leg = new TLegend(0.1,0.7,0.5,0.9);
//  leg->SetHeader("The Legend Title");
 leg->AddEntry(g_e0_NoUE,"No UE","lp");
 leg->AddEntry(g_e0_CMS,"CMS tune","lp");
 leg->AddEntry(g_e0_ATLAS,"ATLAS tune","lp");
 leg->SetFillColor(0);

 TCanvas* ce0 = new TCanvas ("ce0","ce0",800,600);

 TMultiGraph *mg = new TMultiGraph();
 mg->Add(g_e0_CMS,"lp");
 mg->Add(g_e0_ATLAS,"lp");
 mg->Add(g_e0_NoUE,"lp");
 mg->Draw("a");
 mg->GetXaxis()->SetTitle("jet p_{T} threshold [GeV]");
 mg->GetYaxis()->SetTitle("0 jet efficiency");
 leg->Draw();
 ce0->SetGrid();


 TGraphAsymmErrors* grErr =  new TGraphAsymmErrors(n, X, Y_One, X_Zero, X_Zero, Y_Delta_e0_overE_do, Y_Delta_e0_overE_up);
 TCanvas* ce0relative = new TCanvas ("ce0relative","ce0relative",800,600);
 grErr->SetMarkerSize(1);
 grErr->SetMarkerStyle(21);
 grErr->SetMarkerColor(kRed);
 grErr->SetLineColor(kRed);
 grErr->GetXaxis()->SetTitle("jet p_{T} threshold [GeV]");
 grErr->GetYaxis()->SetTitle("Relative error on efficiency");

 grErr->Draw ("apl");
 ce0relative->SetGrid();


 //--------------------------
 TH1F* h_e0_CMS   = new TH1F("CMS","",100,0,200);
 TH1F* h_e0_ATLAS = new TH1F("ATLAS","",100,0,200);
 TH1F* h_e0_NoUE  = new TH1F("NoUE","",100,0,200);

//  TH1F* h_e0_CMS   = new TH1F("CMS","",n,10,10+n*2X);
//  TH1F* h_e0_ATLAS = new TH1F("ATLAS","",n,10,10+n*2X);
//  TH1F* h_e0_NoUE  = new TH1F("NoUE","",n,10,10+n*2X);

 tCMS->Draw("jetpt1 >> CMS","","goff");
 tATLAS->Draw("jetpt1 >> ATLAS","","goff");
 tNoUE->Draw("jetpt1 >> NoUE","","goff");

 h_e0_CMS->SetMarkerColor(kRed);
 h_e0_CMS->SetLineWidth(2);
 h_e0_CMS->SetLineColor(kRed);
 h_e0_CMS->GetXaxis()->SetTitle("jet p_{T} [GeV]");
 h_e0_CMS->GetYaxis()->SetTitle("evetns");

 h_e0_ATLAS->SetMarkerColor(kBlue);
 h_e0_ATLAS->SetLineColor(kBlue);
 h_e0_ATLAS->SetLineWidth(2);
 h_e0_ATLAS->GetXaxis()->SetTitle("events");

 h_e0_NoUE->SetMarkerColor(kGreen);
 h_e0_NoUE->SetLineColor(kGreen);
 h_e0_NoUE->SetLineWidth(2);
 h_e0_NoUE->GetXaxis()->SetTitle("events");

 TCanvas* cn = new TCanvas ("cn","cn",800,600);
 h_e0_CMS->DrawNormalized();
 h_e0_ATLAS->DrawNormalized("same");
 h_e0_NoUE->DrawNormalized("same");
 cn->SetGrid();

}




