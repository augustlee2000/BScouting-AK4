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
          mask.tensor<float, 3>()(i, j, 0) = 1.0;  // Set mask value to 1 for valid candidates
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
            }
        }
    }
 }
  std::vector<tensorflow::Tensor> outputs;

  
  // tensorflow::Status status = const_cast<tensorflow::Session*>(session_)->Run({{inputTensorName_, input}}, {outputTensorName_}, {}, &outputs);
  std::vector<float> bTagScores(jets->size());
  if (jets->size() > 0) {
    tensorflow::run(session_, {{inputTensorName_, input}, {"mask", mask}, {"points", points}}, {outputTensorName_}, &outputs);
    for (size_t a = 0; a < jets->size(); a++) {
      bTagScores[a] = outputs[0].matrix<float>()(a, 1);

    }
  }


  /* tensorflow::run(session_, {{inputTensorName_, input}, {"mask", mask}, {"points", points}}, {outputTensorName_}, &outputs);
  //tensorflow::run(session_, {{inputTensorName_, input}}, {outputTensorName_}, &outputs);
  for (size_t a = 0; a < jets->size(); a++) {
    std::cout << "output: " << outputs[0].matrix<float>()(a, 0) << std::endl;

  }
  // print the output
  std::cout << jets->size() << " -> " << outputs[0].matrix<float>()(0, 0) << std::endl << std::endl;

  const tensorflow::Tensor& output = outputs[0]; 

  std::vector<float> bTagScores(tag_infos->size()); */
  

  // Create a ValueMap for bTagScores and store it in the event
  std::unique_ptr<edm::ValueMap<float>> bTagScore_table(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler filler_BTagScore_table(*bTagScore_table);
  filler_BTagScore_table.insert(jets, bTagScores.begin(), bTagScores.end());
  filler_BTagScore_table.fill();
  
  event.put(std::move(bTagScore_table), "bTagScore");
}

DEFINE_FWK_MODULE(MyPlugin);
