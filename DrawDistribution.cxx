#include <algorithm>

void DrawDistribution(std::string var = "jetpt1", int NBIN = 1000, int MIN = 0, int MAX = 1000, std::string varHR = ""){

 if (varHR == "") {
  varHR = var;
 }

 gStyle->SetOptStat(0);


 TFile* fCMS   = new TFile ("/tmp/amassiro/WW1Mevents_TUNE_CMS_dump_tree.root");
 TFile* fATLAS = new TFile ("/tmp/amassiro/WW1Mevents_TUNE_ATLAS_dump_tree.root");
//  TFile* fHerwig  = new TFile ("/tmp/amassiro/WW1Mevents_TUNE_Herwig_dump_tree_2.root");
//  TFile* fHerwig  = new TFile ("/tmp/amassiro/WW1Mevents_TUNE_Herwig_dump_tree.root");
 TFile* fHerwig  = new TFile ("/tmp/amassiro/WW1Mevents_TUNE_Herwig_UE_dump_tree.root");
 TFile* fCMS_Z2Lep = new TFile ("/tmp/amassiro/WW1Mevents_TUNE_CMS_Z2Lep_dump_tree.root");



 TTree* tCMS   =  (TTree*) fCMS   -> Get ("Analyzer/myTree");
 TTree* tATLAS =  (TTree*) fATLAS -> Get ("Analyzer/myTree");
 TTree* tHerwig      =  (TTree*) fHerwig    -> Get ("Analyzer/myTree");
 TTree* tCMS_Z2Lep   =  (TTree*) fCMS_Z2Lep -> Get ("Analyzer/myTree");


 //--------------------------
 TH1F* h_e0_CMS   = new TH1F("CMS",varHR.c_str(),NBIN,MIN,MAX);
 TH1F* h_e0_ATLAS = new TH1F("ATLAS",varHR.c_str(),NBIN,MIN,MAX);
 TH1F* h_e0_Herwig  = new TH1F("Herwig",varHR.c_str(),NBIN,MIN,MAX);
 TH1F* h_e0_CMS_Z2Lep   = new TH1F("CMS_Z2Lep",varHR.c_str(),NBIN,MIN,MAX);

 TString toDraw;

 toDraw = Form ("%s >> CMS",var.c_str());       tCMS       -> Draw(toDraw.Data(),"","goff");
 toDraw = Form ("%s >> ATLAS",var.c_str());     tATLAS     -> Draw(toDraw.Data(),"","goff");
 toDraw = Form ("%s >> Herwig",var.c_str());    tHerwig    -> Draw(toDraw.Data(),"","goff");
 toDraw = Form ("%s >> CMS_Z2Lep",var.c_str()); tCMS_Z2Lep -> Draw(toDraw.Data(),"","goff");


 h_e0_CMS->SetMarkerColor(kRed);
 h_e0_CMS->SetLineWidth(2);
 h_e0_CMS->SetLineColor(kRed);
 h_e0_CMS->GetXaxis()->SetTitle(varHR.c_str());
 h_e0_CMS->GetYaxis()->SetTitle("evetns");

 h_e0_ATLAS->SetMarkerColor(kBlue);
 h_e0_ATLAS->SetLineColor(kBlue);
 h_e0_ATLAS->SetLineWidth(2);
 h_e0_ATLAS->GetXaxis()->SetTitle("events");

 h_e0_Herwig->SetMarkerColor(kGreen);
 h_e0_Herwig->SetLineColor(kGreen);
 h_e0_Herwig->SetLineWidth(2);
 h_e0_Herwig->GetXaxis()->SetTitle("events");

 h_e0_CMS_Z2Lep->SetMarkerColor(kTeal);
 h_e0_CMS_Z2Lep->SetLineWidth(2);
 h_e0_CMS_Z2Lep->SetLineColor(kTeal);
 h_e0_CMS_Z2Lep->GetXaxis()->SetTitle(varHR.c_str());
 h_e0_CMS_Z2Lep->GetYaxis()->SetTitle("evetns");


 TLegend* leg = new TLegend(0.5,0.7,0.9,0.9);
 leg->AddEntry(h_e0_Herwig,"Herwig PS","lp");
 leg->AddEntry(h_e0_CMS,"Pythia CMS tune","lp");
 leg->AddEntry(h_e0_ATLAS,"Pythia ATLAS tune","lp");
 leg->AddEntry(h_e0_CMS_Z2Lep,"Pythia CMS Z2Lep tune","lp");
 leg->SetFillColor(0);

 TCanvas* cn = new TCanvas ("cn","cn",800,600);
 h_e0_CMS->DrawNormalized();
 h_e0_ATLAS->DrawNormalized("same");
 h_e0_Herwig->DrawNormalized("same");
 h_e0_CMS_Z2Lep->DrawNormalized("same");
 leg->Draw();
 cn->SetGrid();

}




