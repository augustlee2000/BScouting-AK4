# -*- coding: utf-8
import os
import array
from array import *
import numpy as np
import glob
import math
from math import pi, cos, asinh, sqrt,sin,log
import random
import ROOT
import sys
import matplotlib.pyplot as plt
import pandas as pd
import uproot
import awkward as ak
import glob
from scipy.stats import cauchy
import pickle
import mplhep as hep

def neutrino(jet,muon, pt_v, phi_v):
    pt_l = muon.Pt()
    phi_l = muon.Phi()
    pz_l = muon.Pz()
    E_l = muon.E()
    mu = mu_calc(pt_l, pt_v, phi_l, phi_v)
    square_root = (((mu**2 * pz_l**2)/(pt_l**4)) - (((E_l**2 * pt_v**2) - mu**2) /(pt_l**2)))
    real_part = ((mu*pz_l)/(pt_l**2))
    if square_root < 0:
        pz_v = real_part
        neutrino = neutrino_vec(pt_v*cos(phi_v), pt_v*sin(phi_v), pz_v)

        top = jet + muon + neutrino

        w = muon + neutrino

        return top.M(), top
        
        
    else:
        chi2 = []
        pz_v = [real_part + sqrt(square_root), real_part - sqrt(square_root) ]

        neutrino_0 = neutrino_vec(pt_v*cos(phi_v), pt_v*sin(phi_v), pz_v[0])
        neutrino_1 = neutrino_vec(pt_v*cos(phi_v), pt_v*sin(phi_v), pz_v[1])

        top_0 = jet + muon + neutrino_0
        w1 = muon + neutrino_0
        top_1 = jet + muon + neutrino_1
        w2 = muon + neutrino_1

        if abs(top_0.M() - 172) < abs(top_1.M() - 172):
            return top_0.M(), top_0
        else:
            return top_1.M(), top_1
                  
def mu_calc(pt_l, pt_v, phi_l, phi_v):
    return ( 3230.23 + (pt_l * pt_v* cos(phi_v - phi_l)))

def neutrino_vec(px,py,pz):
    v_E = sqrt(px**2 + py**2 + pz**2)
    v = ROOT.TLorentzVector()
    v.SetPxPyPzE(px,py,pz,v_E)
    return v

def chi2_function(top_l, top_h):
    chi2 = (172.76 - top_l)**2 + (172.76 - top_h)**2
    return chi2/172.76
def HistNorm(hist):
    integral = hist.Integral()
    hist.Scale(1./integral)

def MakeHist(N,colors,names,title,x_axis,y_axis,high,low,bins):
    hist = []
    for i in range(N):
        hists = ROOT.TH1F(names[i],title,bins,low,high)
        hists.SetLineColor(colors[i])
        #hists.SetFillColor(colors[i])
        hists.GetXaxis().SetTitle(x_axis)
        hists.GetYaxis().SetTitle(y_axis)
        hist.append(hists)
    return hist

def legends(hists):
    print("name = ",hists.GetName())
    hists_legend.AddEntry(hists,hists.GetName(),"lp")

def deltaR(eta1, phi1, eta2, phi2):
    dphi = abs(phi1 - phi2)
    if dphi > math.pi:
        dphi = 2 * math.pi - dphi
    deta = eta1 - eta2
    return math.sqrt(deta**2 + dphi**2)

def gen_match(eta,phi,parton, j_eta, j_phi):
    genjets_ = list(zip(eta, phi, parton))
    ak4_jets = list(zip(j_eta, j_phi))

    dR_ = 0.4  # Example deltaR cut-off value
    genmatch_resultmap = {}
    genmatch_unmatched = []
    pairlist = []

    for i, ak4_jet in enumerate(ak4_jets):
        found_match = False
        for j, genjet in enumerate(genjets_):
            dR = deltaR(ak4_jet[0], ak4_jet[1], genjet[0], genjet[1])
            if dR < dR_:
                pairlist.append((i, j, dR))
                found_match = True
        if not found_match:
            genmatch_unmatched.append(i)

    pairlist.sort(key=lambda x: x[2])

    while pairlist:
        closest_pair = pairlist.pop(0)
        i, j, dR = closest_pair
        genjet_assn = genjets_[j][2]  # Assuming genjet_assn corresponds to hadron flavor
        genmatch_resultmap[i] = genjet_assn
        
        pairlist = [pair for pair in pairlist if pair[0] != i and pair[1] != j]
    if len(genmatch_resultmap) == 0:
        return False, 9999
    else:
        for ak4_idx, parton_flavor in genmatch_resultmap.items():
            
            if abs(parton_flavor) == 5:
                return True, ak4_idx
            else:
                return False, ak4_idx
        
def all_unique(sequence):
    return len(sequence) == len(set(sequence))

def btagging_efficenty_v2(file, weights, kde, location, scale):  #, hist_0, hist_1, hist_2):
    infile_name = file #takes in the current file

    try:
        infile = uproot.open(infile_name)
        tree = infile['Events']  # Get the event tree
    except OSError as e:
        print(f"Error opening file {infile_name}: {e}")
        # Return empty arrays or any appropriate default values if needed

        return np.array([]), np.array([]), np.array([]), np.array([]), np.array([])




    #Get the ML scores if it greater than .3 then it is 1 if it less then is 0
    b_jets = tree["ScoutingJet_particleNet_prob_b"].array()
    b_jets_btagged  = np.where(b_jets > .5 ,1, 0)


    #applying muon and jet cuts on the data
    muons = tree["nScoutingMuonVtx"].array()
    B_jet_mask = np.sum(b_jets_btagged == 1, axis=1)
    b_jets_cut = B_jet_mask > -1
    muons_cut = muons > 0

    jet_eta = tree["ScoutingJet_eta"].array()
    jet_pt = tree["ScoutingJet_pt"].array()
    eta_cut = np.abs(jet_eta) < 2.5
    pt_cut = jet_pt >= 30
    combined = pt_cut & eta_cut
    filtered_jet_pt = jet_pt[combined]
    num_jets_after_cut = ak.num(filtered_jet_pt)
    number_of_events_cut = num_jets_after_cut == 4

    trigger_HT = tree["DST_PFScouting_SingleMuon"].array()
    

    met_pt_cut = tree["ScoutingMET_pt"].array() > 30

    event_mask = b_jets_cut & number_of_events_cut & muons_cut & met_pt_cut & trigger_HT

    #making a cut on individual muons

    temp_pt = tree["ScoutingJet_pt"].array()[event_mask]
    temp_eta =  tree["ScoutingJet_eta"].array()[event_mask]

    cut1 = np.abs(temp_eta) < 2.5
    cut2 = np.abs(temp_pt) >= 30

    fcut = cut1 & cut2

    #making the cut on all the branches that I need
    cut_b_jets = b_jets_btagged[event_mask][fcut]
    cut_phi = tree["ScoutingJet_phi"].array()[event_mask][fcut]
    cut_eta = tree["ScoutingJet_eta"].array()[event_mask][fcut]
    cut_mass = tree["ScoutingJet_mass"].array()[event_mask][fcut]
    cut_pt = tree["ScoutingJet_pt"].array()[event_mask][fcut]

    full_phi = tree["ScoutingJet_phi"].array()[event_mask]
    full_eta = tree["ScoutingJet_eta"].array()[event_mask]
    full_mass = tree["ScoutingJet_mass"].array()[event_mask]
    full_pt = tree["ScoutingJet_pt"].array()[event_mask]

    n_muon = tree["nScoutingMuonVtx"].array()[event_mask]
    muon_pt = tree["ScoutingMuonVtx_pt"].array()[event_mask]
    muon_eta = tree["ScoutingMuonVtx_eta"].array()[event_mask]
    muon_phi = tree["ScoutingMuonVtx_phi"].array()[event_mask]
    muon_mass = tree["ScoutingMuonVtx_m"].array()[event_mask]
    met_pt = tree["ScoutingMET_pt"].array()[event_mask]
    met_phi = tree["ScoutingMET_phi"].array()[event_mask]
    muon_ecal_iso = tree["ScoutingMuonVtx_ecalIso"].array()[event_mask]
    muon_hcal_iso =tree["ScoutingMuonVtx_hcalIso"].array()[event_mask]
    muon_track_iso = tree["ScoutingMuonVtx_trackIso"].array()[event_mask]
    

    # eta = tree["GenJet_eta"].array()[event_mask]
    # phi = tree["GenJet_phi"].array()[event_mask]
    # mass = tree["GenJet_mass"].array()[event_mask]
    # pt = tree["GenJet_pt"].array()[event_mask]
    # hadron = tree["GenJet_hadronFlavour"].array()[event_mask]
    # parton = tree["GenJet_partonFlavour"].array()[event_mask]

    # genPartIdxMother = tree["GenPart_genPartIdxMother"].array()[event_mask]
    # genPartStatusFlags= tree["GenPart_statusFlags"].array()[event_mask]
    # genPartpdgId = tree["GenPart_pdgId"].array()[event_mask]
    # genPartStatus = tree["GenPart_status"].array()[event_mask]

    # etaPart = tree["GenPart_eta"].array()[event_mask]
    # phiPart = tree["GenPart_phi"].array()[event_mask]
    # massPart = tree["GenPart_mass"].array()[event_mask]
    # ptPart = tree["GenPart_pt"].array()[event_mask]


    muon_iso = (muon_ecal_iso + muon_hcal_iso + muon_track_iso)/muon_pt

    sigma2 = np.array([[25, 1], [1, 25]])
    idx_combo = [[0,1,2,3],[0,2,1,3],[0,3,1,2], [1,0,2,3], [1,2,0,3], [1,3,0,2], [2,0,1,3], [2,1,0,3], [2,3,0,1], [3,0,1,2], [3,1,0,2], [3,2,0,1]]
    tag = 0
    probe = 0
    veto = 0
    pt1 = np.array([])
    pt2 = np.array([])
    pt3 = np.array([])
    pt4 = np.array([])
    pt5 = np.array([])
    #loop over all events that are left
    for i in range(len(cut_b_jets)): #len(cut_b_jets)
        ht = cut_pt[i][0] + cut_pt[i][1] + cut_pt[i][2] + cut_pt[i][3] + muon_pt[i][0] + met_pt[i]
        if muon_pt[i][0] > 30 and abs(muon_iso[i][0]) < .3 and ht > 650:
            lep_top_mass = []
            prob = []
            lep_array = []
            lep_top = []
            had_top_mass = []
            top_quark_had = []
            top_quark_lep = []

            jet_0 = ROOT.TLorentzVector()
            jet_1 = ROOT.TLorentzVector()
            jet_2 = ROOT.TLorentzVector()
            jet_3 = ROOT.TLorentzVector()
            muon = ROOT.TLorentzVector()
            jet_0.SetPtEtaPhiM(cut_pt[i][0], cut_eta[i][0], cut_phi[i][0], cut_mass[i][0])
            jet_1.SetPtEtaPhiM(cut_pt[i][1], cut_eta[i][1], cut_phi[i][1], cut_mass[i][1])
            jet_2.SetPtEtaPhiM(cut_pt[i][2], cut_eta[i][2], cut_phi[i][2], cut_mass[i][2])
            jet_3.SetPtEtaPhiM(cut_pt[i][3], cut_eta[i][3], cut_phi[i][3], cut_mass[i][3])
            muon.SetPtEtaPhiM(muon_pt[i][0], muon_eta[i][0], muon_phi[i][0], muon_mass[i][0])
            jet_array = [jet_0, jet_1, jet_2, jet_3]
            lep_top_0, top_0_q = neutrino(jet_0, muon, met_pt[i], met_phi[i])
            lep_top_1, top_1_q = neutrino(jet_1, muon, met_pt[i], met_phi[i])
            lep_top_2, top_2_q = neutrino(jet_2, muon, met_pt[i], met_phi[i])
            lep_top_3, top_3_q = neutrino(jet_3, muon, met_pt[i], met_phi[i])

            lep_prob_0 = cauchy.pdf(lep_top_0, location, scale)
            lep_prob_1 = cauchy.pdf(lep_top_1, location, scale)
            lep_prob_2 = cauchy.pdf(lep_top_2, location, scale)
            lep_prob_3 = cauchy.pdf(lep_top_3, location, scale)

            top_quark_lep_array = [top_0_q, top_1_q, top_2_q, top_3_q]
            lep_array = [lep_top_0, lep_top_1, lep_top_2, lep_top_3]
            lep_top_prob = [lep_prob_0, lep_prob_1, lep_prob_2, lep_prob_3]


            for j in range(len(idx_combo)): # 0: leptonic b, 1: hadronic b, 2: w, 3: w index
                w_quark = jet_array[idx_combo[j][2]] + jet_array[idx_combo[j][3]]
                w_mass = w_quark.M()
                top_quark = w_quark + jet_array[idx_combo[j][1]]
                top_mass = top_quark.M()

                prob_array = np.array([top_mass, w_mass])

                had_top_prob = kde(prob_array)
                lep_top.append(lep_array[idx_combo[j][0]])

                if had_top_prob != 0 and lep_top_prob[idx_combo[j][0]] != 0:
                    final_prob = -1*log(had_top_prob) - log(lep_top_prob[idx_combo[j][0]])
                else:
                    final_prob = 999999 

                lep_top_mass.append(lep_array[idx_combo[j][0]])
                had_top_mass.append(top_mass)
                prob.append(final_prob)
                top_quark_had.append(top_quark)
                top_quark_lep.append(top_quark_lep_array[idx_combo[j][0]])

            min_idx = np.argmin(prob)
            if prob[min_idx] < 15:
                min_jet_idx = idx_combo[min_idx]
                # j_eta =[]
                # j_phi = []
                # j_eta.append(cut_eta[i][min_jet_idx[0]])
                # j_phi.append(cut_phi[i][min_jet_idx[0]])
                #TrueFalse, junk = gen_match(eta[i],phi[i],hadron[i], j_eta, j_phi)
                
                if lep_top_mass[min_idx] < 250:
                    if cut_pt[i][min_jet_idx[0]] < 150:
                        #if TrueFalse == True:
                        if cut_b_jets[i][min_jet_idx[0]] == 1:
                            h1.Fill(lep_top_mass[min_idx],weights)
                            pt1 = np.append(pt1, cut_pt[i][min_jet_idx[0]])
                            #hists_c.Fill(lep_top_mass[min_idx], had_top_mass[min_idx])
                            #fill correct histogram
                        else:
                            h0.Fill(lep_top_mass[min_idx],weights)
                            pt1 = np.append(pt1, cut_pt[i][min_jet_idx[0]])
                            #hists_i.Fill(lep_top_mass[min_idx], had_top_mass[min_idx])
                            #fill wrong histogram
                    elif cut_pt[i][min_jet_idx[0]] > 150 and cut_pt[i][min_jet_idx[0]] < 200:
                        #if TrueFalse == True:
                        if cut_b_jets[i][min_jet_idx[0]] == 1:
                            h3.Fill(lep_top_mass[min_idx],weights)
                            pt2 = np.append(pt2, cut_pt[i][min_jet_idx[0]])
                            #hists_c.Fill(lep_top_mass[min_idx], had_top_mass[min_idx])
                            #fill correct histogram
                        else:
                            h2.Fill(lep_top_mass[min_idx],weights)
                            pt2 = np.append(pt2, cut_pt[i][min_jet_idx[0]])
                            #hists_i.Fill(lep_top_mass[min_idx], had_top_mass[min_idx])
                            #fill wrong histogram
                    elif cut_pt[i][min_jet_idx[0]] > 200 and cut_pt[i][min_jet_idx[0]] < 250:
                        #if TrueFalse == True:
                        if cut_b_jets[i][min_jet_idx[0]] == 1:
                            h5.Fill(lep_top_mass[min_idx],weights)
                            pt3 = np.append(pt3, cut_pt[i][min_jet_idx[0]])
                            #hists_c.Fill(lep_top_mass[min_idx], had_top_mass[min_idx])
                            #fill correct histogram
                        else:
                            h4.Fill(lep_top_mass[min_idx],weights)
                            pt3 = np.append(pt3, cut_pt[i][min_jet_idx[0]])
                            #hists_i.Fill(lep_top_mass[min_idx], had_top_mass[min_idx])
                            #fill wrong histogram
                    elif cut_pt[i][min_jet_idx[0]] > 250 and cut_pt[i][min_jet_idx[0]] < 300:
                        #if TrueFalse == True:
                        if cut_b_jets[i][min_jet_idx[0]] == 1:
                            h7.Fill(lep_top_mass[min_idx],weights)
                            pt4 = np.append(pt4, cut_pt[i][min_jet_idx[0]])
                            #hists_c.Fill(lep_top_mass[min_idx], had_top_mass[min_idx])
                            #fill correct histogram
                        else:
                            h6.Fill(lep_top_mass[min_idx],weights)
                            pt4 = np.append(pt4, cut_pt[i][min_jet_idx[0]])
                            #hists_i.Fill(lep_top_mass[min_idx], had_top_mass[min_idx])
                            #fill wrong histogram
                    elif cut_pt[i][min_jet_idx[0]] > 300:
                        #if TrueFalse == True:
                        if cut_b_jets[i][min_jet_idx[0]] == 1:
                            h9.Fill(lep_top_mass[min_idx],weights)
                            pt5 = np.append(pt5, cut_pt[i][min_jet_idx[0]])
                            #hists_c.Fill(lep_top_mass[min_idx], had_top_mass[min_idx])
                            #fill correct histogram
                        else:
                            h8.Fill(lep_top_mass[min_idx],weights)
                            pt5 = np.append(pt5, cut_pt[i][min_jet_idx[0]])
                            #hists_i.Fill(lep_top_mass[min_idx], had_top_mass[min_idx])
                            #fill wrong histogram
    return pt1, pt2, pt3, pt4, pt5



def efficency(file,weights, kde, location, scale):
    file_array= glob.glob(file)
    number = 0 
    pt1_array = np.array([])
    pt2_array = np.array([])
    pt3_array = np.array([])
    pt4_array = np.array([])
    pt5_array = np.array([])
    if len(file_array) < 100000:
        number = len(file_array)
    else:
        number = 100000
    print(number)
    for i in range(number): #len(file)
        print(i)
        pt1,pt2, pt3, pt4, pt5=btagging_efficenty_v2(file_array[i],weights, kde, location, scale)
        pt1_array = np.append(pt1_array, pt1)
        pt2_array = np.append(pt2_array, pt2)
        pt3_array = np.append(pt3_array, pt3)
        pt4_array = np.append(pt4_array, pt4)
        pt5_array = np.append(pt5_array, pt5)
    return pt1_array, pt2_array, pt3_array, pt4_array, pt5_array


#files = ["/scratch365/alee43/aulee/QCD_PT-30to50_TuneCP5_13p6TeV_pythia8/btagging_V3_QCD_30_50_1/240606_202328/0000/*.root", "/cms/cephfs/data/store/user/aulee/QCD_PT-50to80_TuneCP5_13p6TeV_pythia8/btagging_V1_QCD_50_80/240506_031257/0000/*.root", "/cms/cephfs/data/store/user/aulee/QCD_PT-80to120_TuneCP5_13p6TeV_pythia8/btagging_V1_QCD_80_120/240506_031024/0000/*.root","/cms/cephfs/data/store/user/aulee/QCD_PT-120to170_TuneCP5_13p6TeV_pythia8/btagging_V1_QCD_120_170/240506_032100/0000/*.root", "/cms/cephfs/data/store/user/aulee/QCD_PT-300to470_TuneCP5_13p6TeV_pythia8/btagging_V1_QCD_300_470/240506_031558/0000/*.root", "/cms/cephfs/data/store/user/aulee/QCD_PT-470to600_TuneCP5_13p6TeV_pythia8/btagging_V1_QCD_470_600/240506_031340/0000/*.root", "/cms/cephfs/data/store/user/aulee/QCD_PT-600to800_TuneCP5_13p6TeV_pythia8/btagging_V1_QCD_600_800/240506_031207/0000/*.root", "/cms/cephfs/data/store/user/aulee/QCD_PT-800to1000_TuneCP5_13p6TeV_pythia8/btagging_V1_QCD_800_1000/240506_031116/0000/*.root", "/cms/cephfs/data/store/user/aulee/QCD_PT-1000to1400_TuneCP5_13p6TeV_pythia8/btagging_V1_QCD_1000_1400/240506_032151/0000/*.root", "/cms/cephfs/data/store/user/aulee/QCD_PT-1400to1800_TuneCP5_13p6TeV_pythia8/btagging_V1_QCD_1400_1800/240506_032009/0000/*.root", "/cms/cephfs/data/store/user/aulee/QCD_PT-1800to2400_TuneCP5_13p6TeV_pythia8/btagging_V1_QCD_1800_2400/240506_031839/0000/*.root", "/cms/cephfs/data/store/user/aulee/QCD_PT-2400to3200_TuneCP5_13p6TeV_pythia8/btagging_V1_QCD_2400_3200/240506_031652/0000/*.root", "/scratch365/alee43/aulee/QCD_PT-3200_TuneCP5_13p6TeV_pythia8/btagging_V1_QCD_3200/240506_031428/0000/*.root" ,"/scratch365/alee43/aulee/TT_TuneCP5_13p6TeV_powheg-pythia8/btagging_V5_TTBar_1/240619_170816/0000/*.root" ]
#weights = [9480855899, 6034985633,575464413.9, 505872340.4, 3921334.675, 4.121052632, 64130.39027, 3975.546604, 10822.6181, 813.5857882, 371.6222414, 31.74374941, 3.867216343, 3.156825569, 10288.10333 ]

# files = ["/scratch365/alee43/aulee/TT_TuneCP5_13p6TeV_powheg-pythia8/btagging_V5_TTBar_1/240619_170816/0000/*.root"]
# weights = [1]

#data
#files = ["/cms/cephfs/data/store/user/aulee/ScoutingPFRun3/Scouting_Run2024D_V5/240907_162053/0000/*.root","/cms/cephfs/data/store/user/aulee/ScoutingPFRun3/Scouting_Run2024D_V5/240907_162053/0001/*.root","/cms/cephfs/data/store/user/aulee/ScoutingPFRun3/Scouting_Run2024D_V5/240907_162053/0002/*.root","/cms/cephfs/data/store/user/aulee/ScoutingPFRun3/Scouting_Run2024D_V5/240907_162053/0003/*.root","/cms/cephfs/data/store/user/aulee/ScoutingPFRun3/Scouting_Run2024D_V5/240907_162053/0004/*.root"]
weights = [1]
file = sys.argv[1]
print(file)
files = [file + "*.root"]
print(files)

h0 = ROOT.TH1F("Incorrect_pt_less_150","Incorrect_pt_less_150",25,0,250)
h1 = ROOT.TH1F("Correct_pt_less_150","Correct_pt_less_150",25,0,250)
h2 = ROOT.TH1F("Incorrect_pt_150_200","Incorrect_pt_150_200",25,0,250)
h3 = ROOT.TH1F("Correct_pt_150_200","Correct_pt_150_200",25,0,250)
h4 = ROOT.TH1F("Incorrect_pt_200_250","Incorrect_pt_200_250",25,0,250)
h5 = ROOT.TH1F("Correct_pt_200_250","Correct_pt_200_250",25,0,250)
h6 = ROOT.TH1F("Incorrect_pt_250_300","Incorrect_pt_250_300",25,0,250)
h7 = ROOT.TH1F("Correct_pt_250_300","Correct_pt_250_300",25,0,250)
h8 = ROOT.TH1F("Incorrect_pt_greater_300","Incorrect_pt_greater_300",25,0,250)
h9 = ROOT.TH1F("Correct_pt_greater_300","Correct_pt_greater_300",25,0,250)



with open('final_pdf.pkl', 'rb') as f:
    saved_data = pickle.load(f)
    lep_pdf = saved_data['lep_pdf']
    hadronic_pdf = saved_data['hadronic_pdf']
    mu = lep_pdf['Top_Leptonic_mu']
    std = lep_pdf['Top_Leptonic_std']

eff = []
for i in range(len(files)):
    
    print(files[i])
    pt1,pt2,pt3,pt4,pt5=efficency(files[i],weights[i], hadronic_pdf, mu, std)



# Open a new ROOT file
new_file = ROOT.TFile("Data_Efficency_Histograms.root", "RECREATE")

# Write individual histograms to the file
h0.Write()
h1.Write()
h2.Write()
h3.Write()
h4.Write()
h5.Write()
h6.Write()
h7.Write()
h8.Write()
h9.Write()

# Close the file
new_file.Close()





#Moving to different python file

# Stack_Mass_1 = ROOT.THStack("Stack_Mass","Leptonic Top Mass Prob < 15 and HT > 500; PT < 150")
# Stack_Mass_1.Add(hist_array[0])
# Stack_Mass_1.Add(hist_array[1])

# Stack_Mass_2 = ROOT.THStack("Stack_Mass","Leptonic Top Mass Prob < 15 and HT > 500; PT > 150 and PT < 200")
# Stack_Mass_2.Add(hist_array[2])
# Stack_Mass_2.Add(hist_array[3])

# Stack_Mass_3 = ROOT.THStack("Stack_Mass","Leptonic Top Mass Prob < 15 and HT > 500; PT > 200 and PT < 250")
# Stack_Mass_3.Add(hist_array[4])
# Stack_Mass_3.Add(hist_array[5])

# Stack_Mass_4 = ROOT.THStack("Stack_Mass","Leptonic Top Mass Prob < 15 and HT > 500; PT > 250 and PT < 300")
# Stack_Mass_4.Add(hist_array[6])
# Stack_Mass_4.Add(hist_array[7])



# Stack_Mass_6 = ROOT.THStack("Stack_Mass","Leptonic Top Mass Prob < 15 and HT > 500; PT > 300")
# Stack_Mass_6.Add(hist_array[8])
# Stack_Mass_6.Add(hist_array[9])


# int0 = hist_array[0].Integral()
# int1 = hist_array[1].Integral()
# int2 = hist_array[2].Integral()
# int3 = hist_array[3].Integral()
# int4 = hist_array[4].Integral()
# int5 = hist_array[5].Integral()
# int6 = hist_array[6].Integral()
# int7 = hist_array[7].Integral()
# int8 = hist_array[8].Integral() 
# int9 = hist_array[9].Integral()
# # int10 = hist_array[10].Integral()
# # int11 = hist_array[11].Integral()

# print(int0, int1, int2, int3, int4, int5, int6, int7, int8, int9)

# efficiency_1 = int1/(int0 + int1)
# efficiency_2 = int3/(int2 + int3)
# efficiency_3 = int5/(int4 + int5)
# efficiency_4 = int7/(int6 + int7)
# efficiency_5 = int9/(int8 + int9)
# #efficiency_6 = int11/(int10 + int11)

# efficency_error_1 = (1/(int0 + int1)**2)*sqrt(int0**2 * int1 + int0 * int1**2)
# efficency_error_2 = (1/(int2 + int3)**2)*sqrt(int2**2 * int3 + int2 * int3**2)
# efficency_error_3 = (1/(int4 + int5)**2)*sqrt(int4**2 * int5 + int4 * int5**2)
# efficency_error_4 = (1/(int6 + int7)**2)*sqrt(int6**2 * int7 + int6 * int7**2)
# efficency_error_5 = (1/(int8 + int9)**2)*sqrt(int8**2 * int9 + int8 * int9**2)
# #efficency_error_6 = (1/(int10 + int11)**2)*sqrt(int10**2 * int11 + int10 * int11**2)




# average1 = np.mean(pt1)
# average2 = np.mean(pt2)
# average3 = np.mean(pt3)
# average4 = np.mean(pt4)
# average5 = np.mean(pt5)

# efficency_error_array = np.array([efficency_error_1, efficency_error_2, efficency_error_3, efficency_error_4, efficency_error_5])
# efficency_array = np.array([efficiency_1, efficiency_2, efficiency_3, efficiency_4, efficiency_5])
# pt_array = np.array([average1, average2, average3, average4, average5])


# c1=ROOT.TCanvas()
# c1.Draw()
# c1.cd()
# Stack_Mass_1.Draw()
# Stack_Mass_1.GetXaxis().SetTitle("Leptonic Top Mass (GeV)")
# Stack_Mass_1.GetYaxis().SetTitle("Instances")
# c1.Update()
# hists_legend.Draw()
# c1.Print("Stack_Mass_Plot V2 Prob less than 15 and HT greater than 500; PT less than 150 - Tag: Data.png")
# c1.cd()

# c2=ROOT.TCanvas()
# c2.Draw()
# c2.cd()
# Stack_Mass_2.Draw()
# Stack_Mass_2.GetXaxis().SetTitle("Leptonic Top Mass (GeV)")
# Stack_Mass_2.GetYaxis().SetTitle("Instances")
# c2.Update()
# hists_legend.Draw()
# c2.Print("Stack_Mass_Plot V2 Prob less than 15 and HT greater than 500; PT greater 150 and less than 200 - Tag: Data.png")
# c2.cd()

# c3=ROOT.TCanvas()
# c3.Draw()
# c3.cd()
# Stack_Mass_3.Draw()
# Stack_Mass_3.GetXaxis().SetTitle("Leptonic Top Mass (GeV)")
# Stack_Mass_3.GetYaxis().SetTitle("Instances")
# c3.Update()
# hists_legend.Draw()
# c3.Print("Stack_Mass_Plot V2 Prob less than 15 and HT greater than 500; PT greater 200 and less than 250 - Tag: Data.png")
# c3.cd()

# c4=ROOT.TCanvas()
# c4.Draw()
# c4.cd()
# Stack_Mass_4.Draw()
# Stack_Mass_4.GetXaxis().SetTitle("Leptonic Top Mass (GeV)")
# Stack_Mass_4.GetYaxis().SetTitle("Instances")
# c4.Update()
# hists_legend.Draw()
# c4.Print("Stack_Mass_Plot V2 Prob less than 15 and HT greater than 500; PT greater 250 and less than 300 - Tag: Data.png")
# c4.cd()

# # c5=ROOT.TCanvas()
# # c5.Draw()
# # c5.cd()
# # Stack_Mass_5.Draw()
# # Stack_Mass_5.GetXaxis().SetTitle("Leptonic Top Mass (GeV)")
# # Stack_Mass_5.GetYaxis().SetTitle("Instances")
# # c5.Update()
# # hists_legend.Draw()
# # c5.Print("Stack_Mass_Plot V2 Prob less than 15 and HT greater than 500; PT greater 400 and less than 500.png")
# # c5.cd()

# c6=ROOT.TCanvas()
# c6.Draw()
# c6.cd()
# Stack_Mass_6.Draw()
# Stack_Mass_6.GetXaxis().SetTitle("Leptonic Top Mass (GeV)")
# Stack_Mass_6.GetYaxis().SetTitle("Instances")
# c6.Update()
# hists_legend.Draw()
# c6.Print("Stack_Mass_Plot V2 Prob less than 15 and HT greater than 500; PT greater 300 - Tag: Data.png")
# c6.cd()

# hep.style.use("CMS")
# plt.figure(figsize=(15,10))
# plt.errorbar(pt_array,efficency_array, xerr=0, yerr=efficency_error_array, fmt='o', color='g', label='Efficency')
# #plt.scatter(pt_array,efficency_array, color='g')
# plt.xlabel('B-jet Pt (GeV)')
# plt.ylabel('Efficency')
# plt.title('Efficiency vs Pt')
# plt.grid(True)
# plt.tight_layout()
# hep.cms.label(rlabel="")
# plt.legend()
# # Save the plot
# plt.savefig('Efficency_New_15 - Tag: Data.png')

print("done")