#include <memory>

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "PhysicsTools/TensorFlow/interface/TensorFlow.h"
#include <vector>
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Scouting/interface/Run3ScoutingPFJet.h"
#include "DataFormats/PatCandidates/interface/Jet.h" // Include for pat::Jet
#include "DataFormats/BTauReco/interface/DeepBoostedJetTagInfo.h"
//#include "FWCore/Framework/interface/EDGetToken.h"

// put a tensorflow::SessionCache into the global cache structure
// the session cache wraps both a tf graph and a tf session instance and also handles their deletion
class MyPlugin : public edm::stream::EDProducer<edm::GlobalCache<tensorflow::SessionCache>> {
public:
  explicit MyPlugin(const edm::ParameterSet&, const tensorflow::SessionCache*);
  ~MyPlugin(){};

  static void fillDescriptions(edm::ConfigurationDescriptions&);

  // additional static methods for initializing and closing the global cache
  static std::unique_ptr<tensorflow::SessionCache> initializeGlobalCache(const edm::ParameterSet&);
  static void globalEndJob(const tensorflow::SessionCache*);

private:
  void beginJob();
  void produce(edm::Event&, const edm::EventSetup&);  // Change this from analyze to produce
  void endJob();

  std::string inputTensorName_;
  std::string outputTensorName_;


  // a pointer to the session created by the global session cache
  typedef std::vector<reco::DeepBoostedJetTagInfo> TagInfoCollection;
  const tensorflow::Session* session_; 
  edm::EDGetTokenT<edm::View<reco::Jet>> jet_token_;
  const edm::EDGetTokenT<TagInfoCollection> src_;

  // Add output variable
  std::vector<float> bTagScore_;  // Or whichever type is appropriate
};

std::unique_ptr<tensorflow::SessionCache> MyPlugin::initializeGlobalCache(const edm::ParameterSet& params) {
  // this method is supposed to create, initialize and return a SessionCache instance
  std::string graphPath = edm::FileInPath(params.getParameter<std::string>("graphPath")).fullPath();
  
  // Declare options outside the if/else block
  tensorflow::Options options;

  // Setup the TF backend by configuration
  if (params.getParameter<std::string>("tf_backend") == "cuda") {
    options = tensorflow::Options{tensorflow::Backend::cuda};
  } else {
    options = tensorflow::Options{tensorflow::Backend::cpu};
  }

  return std::make_unique<tensorflow::SessionCache>(graphPath, options);
}

void MyPlugin::globalEndJob(const tensorflow::SessionCache* cache) {}

void MyPlugin::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  // defining this function will lead to a *_cfi file being generated when compiling
  edm::ParameterSetDescription desc;
  desc.add<std::string>("graphPath", "path/to/your/model")->setComment("Path to the saved TensorFlow model");
  desc.add<std::string>("inputTensorName", "input")->setComment("Name of the input tensor");
  desc.add<std::string>("outputTensorName", "output")->setComment("Name of the output tensor");
  desc.add<std::string>("outputTag", "bTagScore")->setComment("Name of the output branch");
  desc.add<std::string>("tf_backend", "cpu")->setComment("TensorFlow backend: 'cpu' or 'cuda'.");
  desc.add<edm::InputTag>("src", edm::InputTag("pfDeepBoostedJetTagInfos"));
  desc.add<edm::InputTag>("jets", edm::InputTag(""));

  
  
  descriptions.addWithDefaultLabel(desc);
}

MyPlugin::MyPlugin(const edm::ParameterSet& config,  const tensorflow::SessionCache* cache)
    : inputTensorName_(config.getParameter<std::string>("inputTensorName")),
      outputTensorName_(config.getParameter<std::string>("outputTensorName")),
      session_(cache->getSession()),
      jet_token_ (consumes<edm::View<reco::Jet>>(config.getParameter<edm::InputTag>("jets"))),
      src_(consumes<TagInfoCollection>(config.getParameter<edm::InputTag>("src"))){

  // Declare the product that this module will produce
  produces<edm::ValueMap<float>>("bTagScore");
}

void MyPlugin::beginJob() {}

void MyPlugin::endJob() {
  // close the session
  tensorflow::closeSession(session_);
}

void MyPlugin::produce(edm::Event& event, const edm::EventSetup& setup) {
  // define a tensor and fill it with range(10)
  //edm::Handle<std::vector<Run3ScoutingPFJet>> jetsHandle;
  //event.getByToken(jetToken_, jetsHandle);
  edm::Handle<TagInfoCollection> tag_infos;
  event.getByToken(src_, tag_infos);
  edm::Handle<edm::View<reco::Jet>> jets;
  jets = event.getHandle(jet_token_);

  /* int64_t jet_size = 1; // or jets->size() if it’s dynamically determined

  // Define tensors with TensorFlow C++ API
  tensorflow::Tensor input(tensorflow::DT_FLOAT, {jet_size, 50, 10});
  tensorflow::Tensor mask(tensorflow::DT_FLOAT, {jet_size, 50, 1});
  tensorflow::Tensor points(tensorflow::DT_FLOAT, {jet_size, 50, 2});

  // Populate 'points' tensor with specified values
  auto points_flat = points.tensor<float, 3>();
  points_flat(0, 0, 0) = 0.39855543f; points_flat(0, 0, 1) = -0.25659508f;
  points_flat(0, 1, 0) = 0.24621168f; points_flat(0, 1, 1) = 0.00219398f;
  points_flat(0, 2, 0) = 0.16418043f; points_flat(0, 2, 1) = -0.25659508f;
  points_flat(0, 3, 0) = 0.01476637f; points_flat(0, 3, 1) = -0.25659508f;
  points_flat(0, 4, 0) = 0.11144606f; points_flat(0, 4, 1) = -0.15112634f;
  points_flat(0, 5, 0) = 0.1104695f; points_flat(0, 5, 1) = 0.27758461f;
  points_flat(0, 6, 0) = -0.05749926f; points_flat(0, 6, 1) = 0.30688149f;
  points_flat(0, 7, 0) = 0.13293043f; points_flat(0, 7, 1) = 0.04223304f;
  points_flat(0, 8, 0) = 0.10070387f; points_flat(0, 8, 1) = 0.15844397f;
  points_flat(0, 9, 0) = 0.03820387f; points_flat(0, 9, 1) = 0.11547522f;
  points_flat(0, 10, 0) = -0.01160082f; points_flat(0, 10, 1) = -0.15796228f;
  points_flat(0, 11, 0) = -0.16785082f; points_flat(0, 11, 1) = -0.16675134f;
  points_flat(0, 12, 0) = -0.18054613f; points_flat(0, 12, 1) = -0.18042322f;
  points_flat(0, 13, 0) = -0.10535081f; points_flat(0, 13, 1) = 0.1994596f;
  points_flat(0, 14, 0) = -0.19812426f; points_flat(0, 14, 1) = -0.10229822f;
  points_flat(0, 15, 0) = -0.15515551f; points_flat(0, 15, 1) = 0.1447721f;
  points_flat(0, 16, 0) = -0.21765551f; points_flat(0, 16, 1) = 0.02953773f;
  

  // Populate 'input' tensor with specified values
  auto input_flat = input.tensor<float, 3>();
  float input_values[17][10] = {
        { 3.98555428e-01, -2.56595075e-01,  4.74012107e-01, -3.70441139e-01,
          1.16016829e+00,  1.00000000e+00,  0.00000000e+00,  0.00000000e+00,
          0.00000000e+00,  0.00000000e+00 },
        { 2.46211678e-01,  2.19397573e-03,  2.46221453e-01,  1.97397256e+00,
          3.34439349e+00,  1.00000000e+00,  0.00000000e+00,  0.00000000e+00,
          0.00000000e+00,  0.00000000e+00 },
        { 1.64180428e-01, -2.56595075e-01,  3.04624766e-01, -3.57093573e-01,
          9.52827692e-01,  1.00000000e+00,  0.00000000e+00,  0.00000000e+00,
          0.00000000e+00,  0.00000000e+00 },
        { 1.47663690e-02, -2.56595075e-01,  2.57019609e-01,  1.78063011e+00,
          2.92941475e+00,  1.00000000e+00,  0.00000000e+00,  0.00000000e+00,
          0.00000000e+00,  0.00000000e+00 },
        { 1.11446060e-01, -1.51126340e-01,  1.87774852e-01,  2.27726722e+00,
          3.51783872e+00,  1.00000000e+00,  0.00000000e+00, -1.00000000e+00,
          6.16455078e-03, -1.00097656e-01 },
        { 1.10469498e-01,  2.77584612e-01,  2.98758626e-01,  3.76400977e-01,
          1.61602890e+00,  0.00000000e+00,  1.00000000e+00,  0.00000000e+00,
          0.00000000e+00,  0.00000000e+00 },
        { -5.74992560e-02,  3.06881487e-01,  3.12221736e-01,  1.98261654e+00,
          3.06280851e+00,  1.00000000e+00,  0.00000000e+00, -1.00000000e+00,
          -3.25202942e-03, -1.17248535e-01 },
        { 1.32930428e-01,  4.22330387e-02,  1.39478058e-01,  2.20013663e-01,
          1.48116159e+00,  0.00000000e+00,  1.00000000e+00,  0.00000000e+00,
          0.00000000e+00,  0.00000000e+00 },
        { 1.00703873e-01,  1.58443972e-01,  1.87738553e-01,  1.76772341e-01,
          1.40764046e+00,  1.00000000e+00,  0.00000000e+00,  1.00000000e+00,
          -2.34985352e-02, -1.42333984e-01 },
        { 3.82038690e-02,  1.15475222e-01,  1.21630847e-01,  1.55154395e+00,
          2.72227192e+00,  1.00000000e+00,  0.00000000e+00,  1.00000000e+00,
          4.02450562e-03, -1.68457031e-01 },
        { -1.16008185e-02, -1.57962278e-01,  1.58387691e-01, -2.98811495e-01,
          8.26517224e-01,  1.00000000e+00,  0.00000000e+00,  1.00000000e+00,
          -1.48849487e-02, -1.43432617e-01 },
        { -1.67850822e-01, -1.66751340e-01,  2.36600727e-01, -2.78608769e-01,
          7.00922132e-01,  1.00000000e+00,  0.00000000e+00,  1.00000000e+00,
          -1.97601318e-02, -9.11254883e-02 },
        { -1.80546135e-01, -1.80423215e-01,  2.55243897e-01,  1.57040465e+00,
          2.53655839e+00,  1.00000000e+00,  0.00000000e+00,  0.00000000e+00,
          0.00000000e+00,  0.00000000e+00 },
        { -1.05350815e-01,  1.99459597e-01,  2.25572437e-01,  3.31857800e-01,
          1.36778784e+00,  1.00000000e+00,  0.00000000e+00, -1.00000000e+00,
          1.55715942e-02, -1.61254883e-01 },
        { -1.98124260e-01, -1.02298215e-01,  2.22975656e-01,  6.49738014e-01,
          1.59888482e+00,  0.00000000e+00,  1.00000000e+00,  0.00000000e+00,
          0.00000000e+00,  0.00000000e+00 },
        { -1.55155510e-01,  1.44772097e-01,  2.12207898e-01,  1.27756441e+00,
          2.26657009e+00,  1.00000000e+00,  0.00000000e+00,  1.00000000e+00,
          -3.22163105e-05, -1.12304688e-01 },
        { -2.17655510e-01,  2.95377262e-02,  2.19650626e-01,  2.70178056e+00,
          3.63294768e+00,  0.00000000e+00,  1.00000000e+00,  0.00000000e+00,
          0.00000000e+00,  0.00000000e+00 }
    };

  for (int i = 0; i < 17; ++i) {
    for (int j = 0; j < 10; ++j) {
        input_flat(0, i, j) = input_values[i][j];
    }
  }

    // Populate 'mask' tensor with specified values
  auto mask_flat = mask.tensor<float, 3>();
  mask_flat(0, 0, 0) = 1.16016829f;
  mask_flat(0, 1, 0) = 3.34439349f;
  mask_flat(0, 2, 0) = 0.95282769f;
  mask_flat(0, 3, 0) = 2.92941475f;
  mask_flat(0, 4, 0) = 3.51783872f;
  mask_flat(0, 5, 0) = 1.6160289f;
  mask_flat(0, 6, 0) = 3.06280851f;
  mask_flat(0, 7, 0) = 1.48116159f;
  mask_flat(0, 8, 0) = 1.40764046f;
  mask_flat(0, 9, 0) = 2.72227192f;
  mask_flat(0, 10, 0) = 0.82651722f;
  mask_flat(0, 11, 0) = 0.70092213f;
  mask_flat(0, 12, 0) = 2.53655839f;
  mask_flat(0, 13, 0) = 1.36778784f;
  mask_flat(0, 14, 0) = 1.59888482f;
  mask_flat(0, 15, 0) = 2.26657009f;
  mask_flat(0, 16, 0) = 3.63294768f;

  

  std::vector<tensorflow::Tensor> outputs;
  tensorflow::run(session_, {{inputTensorName_, input}, {"mask", mask}, {"points", points}}, {outputTensorName_}, &outputs);
  std::vector<float> bTagScores(1);
  bTagScores[0] = outputs[0].matrix<float>()(0, 1);
  std::cout << "output: " << outputs[0].matrix<float>()(0, 0) << std::endl;
  std::cout << "output: " << outputs[0].matrix<float>()(0, 1) << std::endl; */


  //tensorflow::Tensor input(tensorflow::DT_FLOAT, {1, static_cast<int64_t>(jetsHandle->size())});  // Adjust the shape
  tensorflow::Tensor input(tensorflow::DT_FLOAT, {static_cast<int64_t>(jets->size()), 50, 10});
  tensorflow::Tensor mask(tensorflow::DT_FLOAT, {static_cast<int64_t>(jets->size()), 50, 1});
  tensorflow::Tensor points(tensorflow::DT_FLOAT, {static_cast<int64_t>(jets->size()), 50, 2});  // Adjust the shape
  for (size_t i = 0; i < jets->size(); i++) {
    const auto& tag_info = (*tag_infos)[i];  // Access the tag info for this jet
  
    // Loop over the candidates (max 50)
    for (size_t j = 0; j < 50; j++) {
        if (j < tag_info.features().get("pfcand_etarel").size()) {  // Check if there are enough candidates
            

            // Fill the tensor with the 10 variables for each candidate
          //mask.tensor<float, 3>()(i, j, 0) = 0.0;  // Set mask value to 1 for valid candidates
          mask.tensor<float, 3>()(i, j, 0) = tag_info.features().get("pfcand_pt_log_nopuppi")[j];
          points.tensor<float, 3>()(i, j, 0) = tag_info.features().get("pfcand_etarel")[j];  // pt
          points.tensor<float, 3>()(i, j, 1) = tag_info.features().get("pfcand_phirel")[j]; // eta
          input.tensor<float, 3>()(i, j, 0) = tag_info.features().get("pfcand_etarel")[j];              // deta
          input.tensor<float, 3>()(i, j, 1) = tag_info.features().get("pfcand_phirel")[j];              // dphi
          input.tensor<float, 3>()(i, j, 2) = tag_info.features().get("pfcand_deltaR")[j];                // dR
          input.tensor<float, 3>()(i, j, 3) = tag_info.features().get("pfcand_pt_log_nopuppi")[j];    // pt_log_nopuppi
          input.tensor<float, 3>()(i, j, 4) = tag_info.features().get("pfcand_e_log_nopuppi")[j];     // e_log_nopuppi
          if (tag_info.features().get("pfcand_isNeutralHad")[j] == 1 || tag_info.features().get("pfcand_isChargedHad")[j] == 1) {
            input.tensor<float, 3>()(i, j, 5) = 1;
            }
          else {
            input.tensor<float, 3>()(i, j, 5) = 0;
          }
          //input.tensor<float, 3>()(i, j, 5) = tag_info.features().get("pfcand_isNeutralHad")[j];             // isHad and to figured it NeutralHad and charged Hadrong
          if (tag_info.features().get("pfcand_isEl")[j] == 1 || tag_info.features().get("pfcand_isGamma")[j] == 1) {
            input.tensor<float, 3>()(i, j, 6) = 1;
            }
          else {
            input.tensor<float, 3>()(i, j, 6) = 0;
          }
          //input.tensor<float, 3>()(i, j, 6) = tag_info.features().get("pfcand_isEl")[j];              // isEG
          input.tensor<float, 3>()(i, j, 7) = tag_info.features().get("pfcand_charge")[j];            // charge
          input.tensor<float, 3>()(i, j, 8) = tag_info.features().get("pfcand_dxy")[j];               // dxy
          input.tensor<float, 3>()(i, j, 9) = tag_info.features().get("pfcand_dz")[j];                // dz
        } else {
            // Fill remaining slots with zeros if there are fewer than 50 candidates
            for (int k = 0; k < 10; k++) {
                input.tensor<float, 3>()(i, j, k) = 0.0;
                //points.tensor<float, 3>()(i, j, k) = 0.0;
                //mask.tensor<float, 3>()(i, j, k) = 0.0;
            }
            for (int l = 0; l < 2; l++) {
                points.tensor<float, 3>()(i, j, l) = 0.0;
            }
            for (int m = 0; m < 1; m++) {
                mask.tensor<float, 3>()(i, j, m) = 0.0;
            }
    }
  }
 }
  std::vector<tensorflow::Tensor> outputs;
  
  //tensorflow::Status status = const_cast<tensorflow::Session*>(session_)->Run({{inputTensorName_, input}}, {outputTensorName_}, {}, &outputs);
  std::vector<float> bTagScores(jets->size());
  if (jets->size() > 0) {
    tensorflow::run(session_, {{inputTensorName_, input}, {"mask", mask}, {"points", points}}, {outputTensorName_}, &outputs);
    for (size_t a = 0; a < jets->size(); a++) {
      const auto& tag_info = (*tag_infos)[a];
      if (tag_info.features().get("pfcand_pt_log_nopuppi").size() > 0) {
        bTagScores[a] = outputs[0].matrix<float>()(a, 1);
        
      }
      else {
        bTagScores[a] = -1.0;
      }
    }
  }


  

  // Create a ValueMap for bTagScores and store it in the event
  std::unique_ptr<edm::ValueMap<float>> bTagScore_table(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler filler_BTagScore_table(*bTagScore_table);
  filler_BTagScore_table.insert(jets, bTagScores.begin(), bTagScores.end());
  filler_BTagScore_table.fill();
  
  event.put(std::move(bTagScore_table), "bTagScore");
}

DEFINE_FWK_MODULE(MyPlugin);
