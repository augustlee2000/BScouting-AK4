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
  //desc.add<edm::InputTag>("jetInputTag")->setComment("Input tag for jets.");
  desc.add<edm::InputTag>("src", edm::InputTag("pfDeepBoostedJetTagInfos"));

  
  
  descriptions.addWithDefaultLabel(desc);
}

MyPlugin::MyPlugin(const edm::ParameterSet& config,  const tensorflow::SessionCache* cache)
    : inputTensorName_(config.getParameter<std::string>("inputTensorName")),
      outputTensorName_(config.getParameter<std::string>("outputTensorName")),
      session_(cache->getSession()),
      //jetToken_(consumes<std::vector<Run3ScoutingPFJet>>(config.getParameter<edm::InputTag>("jetInputTag"))) { // Assume "jetInputTag" is defined in your configuration
      src_(consumes<TagInfoCollection>(config.getParameter<edm::InputTag>("src"))){

  // Declare the product that this module will produce
  produces<edm::ValueMap<int>>("bTagScore");
}

void MyPlugin::beginJob() {}

void MyPlugin::endJob() {
  // close the session
  tensorflow::closeSession(session_);
}

void MyPlugin::produce(edm::Event& event, const edm::EventSetup& setup) {
  std::cout << "starting"<< std::endl;
  // define a tensor and fill it with range(10)
  //edm::Handle<std::vector<Run3ScoutingPFJet>> jetsHandle;
  //event.getByToken(jetToken_, jetsHandle);
  edm::Handle<TagInfoCollection> tag_infos;
  event.getByToken(src_, tag_infos);

  auto new_tag_infos = std::make_unique<TagInfoCollection>();

  for (const auto& info : *tag_infos) {
    // Process or modify `info` as needed
    new_tag_infos->push_back(info); // Or add modified info
}

  edm::OrphanHandle<TagInfoCollection> oh = event.put(std::move(new_tag_infos));

  //tensorflow::Tensor input(tensorflow::DT_FLOAT, {1, static_cast<int64_t>(jetsHandle->size())});  // Adjust the shape
  tensorflow::Tensor input(tensorflow::DT_FLOAT, {1, static_cast<int64_t>(tag_infos->size())});  // Adjust the shape
  for (size_t i = 0; i < tag_infos->size(); i++) {
    //const auto& jet = (*tag_infos)[i];
    input.matrix<float>()(0, i) = float(i);
  }

  std::vector<tensorflow::Tensor> outputs;
  
  tensorflow::Status status = const_cast<tensorflow::Session*>(session_)->Run({{inputTensorName_, input}}, {outputTensorName_}, {}, &outputs);

  const tensorflow::Tensor& output = outputs[0];

  std::vector<float> bTagScores(tag_infos->size(), 0.0f);

 

  // Create a ValueMap for bTagScores and store it in the event
  std::unique_ptr<edm::ValueMap<float>> bTagScore_table(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler filler_BTagScore_table(*bTagScore_table);
  filler_BTagScore_table.insert(oh, bTagScores.begin(), bTagScores.end());
  filler_BTagScore_table.fill();
  
  event.put(std::move(bTagScore_table), "bTagScore");
}

DEFINE_FWK_MODULE(MyPlugin);
