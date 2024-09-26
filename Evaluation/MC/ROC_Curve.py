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
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve, confusion_matrix
plt.style.use(hep.style.ROOT)


def deltaR(eta1, phi1, eta2, phi2):
    dphi = abs(phi1 - phi2)
    dphi = np.arctan2(np.sin(dphi), np.cos(dphi))
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

def Truth_Label_Array(file):
    infile_name = file #takes in the current file

    try:
        infile = uproot.open(infile_name)
        tree = infile['Events']  # Get the event tree
    except OSError as e:
        print(f"Error opening file {infile_name}: {e}")
        # Return empty arrays or any appropriate default values if needed

        return np.array([]), np.array([])
    

    met_pt_cut = tree["ScoutingMET_pt"].array() > 0
    event_mask = met_pt_cut

    temp_eta =  tree["ScoutingJet_eta"].array()[event_mask]
    cut1 = np.abs(temp_eta) < 2.5
    fcut = cut1

    cut_phi = tree["ScoutingJet_phi"].array()[event_mask][fcut]
    cut_eta = tree["ScoutingJet_eta"].array()[event_mask][fcut]
    b_jets = tree["ScoutingJet_particleNet_prob_b"].array()[event_mask][fcut]

    eta = tree["GenJet_eta"].array()[event_mask]
    phi = tree["GenJet_phi"].array()[event_mask]
    hadron = tree["GenJet_hadronFlavour"].array()[event_mask]
    parton = tree["GenJet_partonFlavour"].array()[event_mask]

    y_true = np.array([])
    y_pred = np.array([])

    for i in range(len(cut_phi)):
        for j in range(len(cut_phi[i])):
            j_eta =[]
            j_phi = []
            j_eta.append(cut_eta[i][j])
            j_phi.append(cut_phi[i][j])
            TrueFalse, index = gen_match(eta[i],phi[i],hadron[i], j_eta, j_phi)
            if TrueFalse == False and index < 9999:
                y_true = np.append(y_true, 0)
                y_pred = np.append(y_pred, b_jets[i][j])
            elif TrueFalse == True and index < 9999:
                y_true = np.append(y_true, 1)
                y_pred = np.append(y_pred, b_jets[i][j])
    return y_true, y_pred


y_true, y_pred = Truth_Label_Array("/scratch365/alee43/aulee/TT_TuneCP5_13p6TeV_powheg-pythia8/btagging_V5_TTBar_1/240619_170816/0000/step1_1.root")

print(sum(y_true), len(y_true))
f, ax = plt.subplots()

fpr, tpr, thresholds = roc_curve(y_true, y_pred)
auc = roc_auc_score(y_true, y_pred)
print(auc)
style = '-'
colour = 'blue'
name = 'ROC Curve'
comp_text=''
ax.plot(tpr, fpr, style, label='%s (AUC = %.4f)'%(name, auc), color=colour)

# Add CMS Internal label
plt.text(0.05, 0.95, 'CMS Internal', 
         fontsize=14, fontweight='bold', 
         transform=plt.gca().transAxes, 
         verticalalignment='top')

ax.legend(bbox_to_anchor=(1.04,1), loc="best")
ax.set_yscale('log')
ax.set_ylim(1e-5 if auc > 0.999 else 1e-4, 1)
ax.set_xlim(0.9 if auc > 0.999 else 0, 1)
ax.set_xlabel('Signal efficiency', horizontalalignment='right', x=1.0)
ax.set_ylabel('Background efficiency', horizontalalignment='right', y=1.0)
ax.text(0.03, 0.95, comp_text, transform=ax.transAxes, fontsize=20, weight='bold')
ax.text(.03,.9, r'')

f.savefig('ROC_Curve.png', bbox_inches='tight')