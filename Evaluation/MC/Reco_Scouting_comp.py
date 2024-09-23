import uproot
import numpy as np
import glob
import os
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

# Function to calculate delta R
def delta_r(eta1, phi1, eta2, phi2):
    dphi = np.abs(phi1 - phi2)
    dphi = np.where(dphi > np.pi, 2 * np.pi - dphi, dphi)  # Handle wrap-around in phi
    deta = eta1 - eta2
    return np.sqrt(deta**2 + dphi**2)

# Function to extract event data, including b_tagging, jet_eta, and jet_phi
def extract_event_data_RECO(file_path, tree_name="Events", event_branch="event", b_tagging_branch="Jet_btagPNetB", 
                       eta_branch="Jet_eta", phi_branch="Jet_phi", pt_branch="Jet_pt"):
    with uproot.open(file_path) as file:
        tree = file[tree_name]
        event_numbers = tree[event_branch].array(library="np")
        b_tagging_values = tree[b_tagging_branch].array(library="np")
        jet_eta_values = tree[eta_branch].array(library="np")
        jet_phi_values = tree[phi_branch].array(library="np")
        jet_pt_values = tree[pt_branch].array(library="np")
    sorted_indices = np.argsort(event_numbers)
    return (event_numbers[sorted_indices], b_tagging_values[sorted_indices], 
            jet_eta_values[sorted_indices], jet_phi_values[sorted_indices], jet_pt_values[sorted_indices])

def extract_event_data_Scouting(file_path, tree_name="Events", event_branch="event", b_tagging_branch="ScoutingJet_particleNet_prob_b", 
                       eta_branch="ScoutingJet_eta", phi_branch="ScoutingJet_phi", pt_branch="ScoutingJet_pt"):
    with uproot.open(file_path) as file:
        tree = file[tree_name]
        event_numbers = tree[event_branch].array(library="np")
        b_tagging_values = tree[b_tagging_branch].array(library="np")
        jet_eta_values = tree[eta_branch].array(library="np")
        jet_phi_values = tree[phi_branch].array(library="np")
        jet_pt_values = tree[pt_branch].array(library="np")
    sorted_indices = np.argsort(event_numbers)
    return (event_numbers[sorted_indices], b_tagging_values[sorted_indices], 
            jet_eta_values[sorted_indices], jet_phi_values[sorted_indices], jet_pt_values[sorted_indices])

# Compare b_tagging after event matching and delta R jet matching
def compare_b_tagging(nano_files, scouting_files, delta_r_threshold=0.4):
    reco_data = {}
    scouting_data = {}

    # Load data from NANO files
    for file in nano_files:
        event_numbers, b_tagging_values, jet_eta_values, jet_phi_values, jet_pt = extract_event_data_RECO(file)
        reco_data[file] = (event_numbers, b_tagging_values, jet_eta_values, jet_phi_values, jet_pt)

    # Load data from scouting files
    for file in scouting_files:
        event_numbers, b_tagging_values, jet_eta_values, jet_phi_values, jet_pt = extract_event_data_Scouting(file)
        scouting_data[file] = (event_numbers, b_tagging_values, jet_eta_values, jet_phi_values, jet_pt)

    y_true = []
    y_pred_prob = []
    variable = []

    # Match events and jets, then compare b_tagging values
    for reco_file, (reco_event_numbers, reco_b_tagging, reco_eta, reco_phi, reco_pt) in reco_data.items():
        for scouting_file, (scouting_event_numbers, scouting_b_tagging, scouting_eta, scouting_phi, scouting_pt) in scouting_data.items():
            common_events, reco_indices, scouting_indices = np.intersect1d(
                reco_event_numbers, scouting_event_numbers, return_indices=True
            )

            if common_events.size > 0:
                # Iterate over each matching event
                for i in range(common_events.size):
                    reco_event_idx = reco_indices[i]
                    scouting_event_idx = scouting_indices[i]

                    # Perform delta R matching between jets in the same event
                    for reco_jet_idx in range(len(reco_eta[reco_event_idx])):
                        best_match_idx = -1
                        best_delta_r = delta_r_threshold

                        # Find the best matching jet in the scouting event
                        for scout_jet_idx in range(len(scouting_eta[scouting_event_idx])):
                            dR = delta_r(reco_eta[reco_event_idx][reco_jet_idx], reco_phi[reco_event_idx][reco_jet_idx],
                                         scouting_eta[scouting_event_idx][scout_jet_idx], scouting_phi[scouting_event_idx][scout_jet_idx])

                            if dR < best_delta_r:
                                best_delta_r = dR
                                best_match_idx = scout_jet_idx

                        # If a match is found, compare the b_tagging values
                        if best_match_idx != -1:
                            reco_btag = reco_b_tagging[reco_event_idx][reco_jet_idx]
                            scouting_btag = scouting_b_tagging[scouting_event_idx][best_match_idx]
                            variable_value =scouting_pt[scouting_event_idx][best_match_idx]

                            # Apply threshold: > 0.5 is considered "tagged"
                            y_true.append(reco_btag > 0.8767)
                            #y_pred_prob.append(scouting_btag)
                            y_pred_prob.append(scouting_btag > 0.8767)
                            variable.append(variable_value)

    # Generate the confusion matrix
    
    return np.array(y_true), np.array(y_pred_prob), np.array(variable)

# Function to plot the ROC curve
def plot_roc_curve(y_true, y_pred_prob):
    fpr, tpr, thresholds = roc_curve(y_true, y_pred_prob)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Tight 0.8767 RECO vs Scouting')
    plt.legend(loc="lower right")
    plt.savefig("roc_curve_RECO_Scouting_Loose.png")

def plot_stuff(y_true, y_pred_prob, variable):
    bins = np.array([0,20,30,40,50,60,70,80,90,100,125,150,175,200,237.5,275,350,500])
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    bin_indices = np.digitize(variable, bins)
    average_y_pred_prob = []
    y_errors=[]
    for i in range(1, len(bins)):
        # Get indices of jet_pt values in the current bin
        bin_mask = (bin_indices == i)
        
        # Get y_pred_prob values where y_pred_prob equals y_true
        total_events = len(y_true[bin_mask])
        correct_predictions = y_pred_prob[bin_mask & (y_pred_prob > y_true)]
        correct_count = len(correct_predictions)
        
        # Calculate average of filtered y_pred_prob
        if total_events > 0:
            avg_y_pred_prob = correct_count / total_events
            y_error = np.sqrt(avg_y_pred_prob * (1 - avg_y_pred_prob) / total_events)
        else:
            avg_y_pred_prob = np.nan  # Handle empty bins
            y_error = 0

        average_y_pred_prob.append(avg_y_pred_prob)
        y_errors.append(y_error)
    plt.figure(figsize=(10, 6))
    plt.errorbar(bin_centers, average_y_pred_prob, yerr=y_errors, fmt='o', capsize=5, linestyle='-', label='Efficiency')
    plt.xlabel('Jet PT (GeV)')
    plt.ylabel('How often Scouting predicts a b-jet while RECO does not')
    plt.title('How often Scouting predicts a b-jet while RECO does not vs Jet PT')
    plt.grid(True)
    plt.savefig("RECO_Scouting_b_miss_id_Tight.png")

# Define the directories and patterns

scouting_directory = "/scratch365/alee43/aulee/TT_TuneCP5_13p6TeV_powheg-pythia8/btagging_V5_TTBar_1/240619_170816/0000/"

# Use glob to dynamically find the ROOT files
nano_files = ["/cms/cephfs/data/store/user/alee43/ttbar_reco/ttbar_reco_2.root"]
scouting_files = glob.glob(os.path.join(scouting_directory, "*.root"))

# Compare b_tagging and generate the confusion matrix
y_true, y_pred_prob, variable = compare_b_tagging(nano_files, scouting_files)
plot_stuff(y_true, y_pred_prob, variable)
#plot_roc_curve(y_true, y_pred_prob)
