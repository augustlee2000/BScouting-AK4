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
                y_pred = np.append(y_pred, b_jets[i][index])
    return y_true, y_pred


y_true, y_pred = Truth_Label_Array("/scratch365/alee43/aulee/TT_TuneCP5_13p6TeV_powheg-pythia8/btagging_V5_TTBar_1/240619_170816/0000/step1_1.root")

non_b_scores = y_pred

print(len(non_b_scores))

sorted_non_b_scores = np.sort(non_b_scores)[::-1]

# Find the 10%, 1%, and 0.1% indices
n_non_b = len(sorted_non_b_scores)
idx_10_percent = int(n_non_b * 0.10)
idx_1_percent = int(n_non_b * 0.01)
idx_0_1_percent = int(n_non_b * 0.001)

# Get the thresholds for the misidentification rates
threshold_10_percent = sorted_non_b_scores[idx_10_percent]
threshold_1_percent = sorted_non_b_scores[idx_1_percent]
threshold_0_1_percent = sorted_non_b_scores[idx_0_1_percent]

print(f"Threshold for 10% misidentification rate: {threshold_10_percent}")
print(f"Threshold for 1% misidentification rate: {threshold_1_percent}")
print(f"Threshold for 0.1% misidentification rate: {threshold_0_1_percent}")

# Number of non-b jets
n_non_b = len(non_b_scores)

# Define the misidentification rates (in fractions)
mistag_rate_10_percent = 0.10
mistag_rate_1_percent = 0.01
mistag_rate_0_1_percent = 0.001

# Calculate the binomial uncertainties for each working point
error_10_percent = np.sqrt(mistag_rate_10_percent * (1 - mistag_rate_10_percent) / n_non_b)
error_1_percent = np.sqrt(mistag_rate_1_percent * (1 - mistag_rate_1_percent) / n_non_b)
error_0_1_percent = np.sqrt(mistag_rate_0_1_percent * (1 - mistag_rate_0_1_percent) / n_non_b)

print(f"Error for 10% misidentification rate: {error_10_percent}")
print(f"Error for 1% misidentification rate: {error_1_percent}")
print(f"Error for 0.1% misidentification rate: {error_0_1_percent}")