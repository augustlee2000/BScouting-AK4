from coffea.nanoevents import NanoEventsFactory, BaseSchema,NanoAODSchema, ScoutingNanoAODSchema
import awkward as ak
import uproot
import vector
import ROOT
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import random
import glob

#Setting Matplotlib Style
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetTitleFontSize(0.04)
ROOT.gStyle.SetLabelSize(0.03, "XYZ")
ROOT.gStyle.SetTitleSize(0.04, "XYZ")
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

vector.register_awkward()
NanoAODSchema.warn_missing_crossrefs = False

#importing file from local directory first file_list is MC while second is data
#file_list = glob.glob("/cms/cephfs/data/store/user/aulee/DYto2L_M-50_TuneCP5_13p6TeV_pythia8/Run3Btagging_CMSSW15/250731_034148/0000/step2_*.root")
file_list = glob.glob("/cms/cephfs/data/store/user/aulee/ScoutingPFRun3/Scouting_Run2023C_CMSSW15_Test/250708_192308/0000/ScoutingPFRun3_2023D_ScoutingNano_Data_Standalone_*.root")
file_list = sorted(file_list)[:100] # Limit to first 100 files for testing 

#setting up the NanoEventsFactory to read the files
events = NanoEventsFactory.from_root(
    {f: "Events" for f in file_list},
    schemaclass=ScoutingNanoAODSchema,
    metadata={"dataset": "DYto2L_M-50_TuneCP5_13p6TeV_pythia8"},
).events()

#selecting trigger and applying to events
trigger_mask = events["DST"]["HLTMuon_Run3_PFScoutingPixelTracking"]
events = events[trigger_mask]

#pulling the muon data from the events
muons = events["ScoutingMuon"]
 

# Build Lorentz vectors for all muons
muon_vectors = ak.zip(
    {
        "pt": muons.pt,
        "eta": muons.eta,
        "phi": muons.phi,
        "mass": muons.m,
        "charge": muons.charge,
        "normchi2": muons.normchi2,
        "trk_dxy": muons.trk_dxy,
        "trk_dz": muons.trk_dz,
        "trackIso": muons.trackIso,
        "ecalIso": muons.ecalIso,
        "hcalIso": muons.hcalIso,
    },
    with_name="Momentum4D"
)
#making sure we have at least 2 muons and pulling to top 2 pt muouns
mask = ak.num(muon_vectors) >= 2
mu1 = muon_vectors[mask][:, 0]
mu2 = muon_vectors[mask][:, 1]

mu1_eta = mu1.eta.compute()
mu2_eta = mu2.eta.compute()
mu1_charge = mu1.charge.compute()
mu2_charge = mu2.charge.compute()
mu1_normchi2 = mu1.normchi2.compute()
mu2_normchi2 = mu2.normchi2.compute()
mu1_trk_dxy = mu1.trk_dxy.compute()
mu2_trk_dxy = mu2.trk_dxy.compute()
mu1_trk_dz = mu1.trk_dz.compute()
mu2_trk_dz = mu2.trk_dz.compute()
mu1_trackIso = mu1.trackIso.compute()
mu2_trackIso = mu2.trackIso.compute()
mu1_ecalIso = mu1.ecalIso.compute()
mu2_ecalIso = mu2.ecalIso.compute()
mu1_hcalIso = mu1.hcalIso.compute()
mu2_hcalIso = mu2.hcalIso.compute()
mu1_pt = mu1.pt.compute()
mu2_pt = mu2.pt.compute()

# Tight selection mask for each muon
def tight_mask(normchi2, trk_dxy, trk_dz, trackIso, ecalIso, hcalIso, pt):
    return (
        (normchi2 < 10)
        & (np.abs(trk_dxy) < 0.2)
        & (np.abs(trk_dz) < 0.5)
        & ((trackIso + ecalIso + hcalIso) / pt < 0.15)
    )

#testing to see if the muons pass might tight selection
mu1_tight = tight_mask(mu1_normchi2, mu1_trk_dxy, mu1_trk_dz, mu1_trackIso, mu1_ecalIso, mu1_hcalIso, mu1_pt)
mu2_tight = tight_mask(mu2_normchi2, mu2_trk_dxy, mu2_trk_dz, mu2_trackIso, mu2_ecalIso, mu2_hcalIso, mu2_pt)


# Apply eta, charge, and mass window cuts
eta_cut = (np.abs(mu1_eta) < 2.5) & (np.abs(mu2_eta) < 2.5)
charge_cut = (mu1_charge * mu2_charge) < 0
pt_cut = (mu1_pt > 25) & (mu2_pt > 25)

# Calculate Z candidate mass and apply mass window cut
z_cand = mu1 + mu2
z_mass = z_cand.mass.compute()
mass_cut = (z_mass > 80) & (z_mass < 100)

final_mask = eta_cut & charge_cut & mass_cut & pt_cut
mu1 = mu1.compute()
mu2 = mu2.compute()

# Apply mask to everything
mu1 = mu1[final_mask]
mu2 = mu2[final_mask]
mu1_tight = mu1_tight[final_mask]
mu2_tight = mu2_tight[final_mask]
z_mass = z_mass[final_mask]

# Tag and probe: randomly assign tag/probe for each event
np.random.seed(42)
rand = np.random.rand(len(mu1))
tag_is_mu1 = rand < 0.5

tag = ak.where(tag_is_mu1, mu1, mu2)
probe = ak.where(tag_is_mu1, mu2, mu1)
tag_tight = ak.where(tag_is_mu1, mu1_tight, mu2_tight)
probe_tight = ak.where(tag_is_mu1, mu2_tight, mu1_tight)

# Only keep events where tag passes tight selection
tag_probe_mask = tag_tight
probe = probe[tag_probe_mask]
probe_tight = probe_tight[tag_probe_mask]

# Efficiency: denominator = all probes, numerator = probes passing tight
probe_pt = probe.pt
bins = np.linspace(25, 100, 20)
tot, _ = np.histogram(probe_pt, bins=bins)
eff, _ = np.histogram(probe_pt[probe_tight], bins=bins)
efficiency = eff / np.maximum(tot, 1)
bin_centers = 0.5 * (bins[1:] + bins[:-1])

#quick error calculation based on statistical uncertainty
eff_err = np.sqrt(efficiency * (1 - efficiency) / np.maximum(tot, 1))
bin_width = bins[1] - bins[0]

#then plotting the efficiency
plt.figure(figsize=(8,6))
hep.style.use("CMS")
plt.errorbar(
    bin_centers, efficiency, yerr=eff_err, xerr=bin_width/2,
    fmt='o', color='crimson', label="Tight efficiency", capsize=2
)
plt.xlabel(r"Probe $p_T$ [GeV]")
plt.ylabel("Efficiency")
plt.title("Tag-and-Probe Tight Muon Efficiency")
plt.ylim(0, 1.1)
plt.legend()
plt.tight_layout()
plt.savefig("Muon_Efficiency_Small_Window.png")
plt.show()
