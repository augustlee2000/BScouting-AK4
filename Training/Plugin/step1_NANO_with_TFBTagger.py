# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 -s NANO:@Scout --process NANO --data --eventcontent NANOAOD,DQM --datatier NANOAOD,DQMIO -n 10000 --customise Configuration/DataProcessing/Utils.addMonitoring --era Run3_2024 --conditions auto:run3_data_prompt --filein filelist:step1_dasquery.log --lumiToProcess step1_lumiRanges.log --fileout file:step2.root
import os
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_2024_cff import Run3_2024

process = cms.Process('NANO',Run3_2024)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.custom_run3scouting_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

#Input source for crab
# process.source = cms.Source("PoolSource",
#     fileNames = cms.untracked.vstring(()))


# # Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/005ca4b8-1e10-4fc2-adec-9a31b5d28fc7.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/0090e21c-bc2d-431c-be65-115764b2d87d.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/01b4b794-4191-43b6-b35b-85cae26eb36b.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/0281f5e2-d452-451b-a51d-3c39278eb958.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/041bb9f7-7974-4a22-8a13-a974313c555f.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/06c7e979-4101-43a2-8e90-9e2782dc4d06.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/070ab341-f4cf-4353-82db-795916bab049.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/07805857-5a69-44c7-a306-1db5a6f83508.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/08753861-21f7-4099-97f2-2b55d4aa7f00.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/0b6db7aa-d04f-46d1-a486-85473d1933a1.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/0c1476d5-501f-4ce9-a5c6-55ecb9e86c8b.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/0c40be78-12fd-47a8-a027-224ce8e8467d.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/0eea6229-25a1-41c8-8a30-5f69f8947bf6.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/116166d9-726f-493d-9e12-9a3f8a94154e.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/143dc3ec-c590-4e89-82f5-88279768a520.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/14e85356-6096-4053-a566-6fe3bb4d6595.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/161ff4d9-9f84-404c-accb-62491a71ec1f.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/17f31a55-79a2-4f7e-9ffd-5de62f847298.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/1838c1bc-4288-4dea-bc76-a63d53b4c7c0.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/18cf3a26-da59-4e74-999f-28b84bfefcba.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/1974c423-ce6c-49a7-bc4e-630c71cce646.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/1ba145c4-b79c-4551-bb1d-840e0846253d.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/1d174aba-c837-454c-b04d-1e4c13bb92ea.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/1deb4dee-a0bb-4808-8f39-f4a6c722dee7.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/1fc1f79a-87d1-4f13-99a2-c56140af4dcd.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/2238e9ae-9c94-4d5b-bb87-93ba5a43112d.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/229a60af-04ac-480f-a34d-ffdf3037d580.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/23f7e6fb-220e-4bef-b466-60cb5a534e87.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/25fbaaec-1deb-4ecf-9b16-d0ba628af04a.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/263df5f1-bc7a-440c-84e6-4ebc5217fa62.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/2c30e049-3092-4516-adb3-c6f43bf493a5.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/2c7087a6-8681-4aa0-a729-c3b9a63bf71d.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/2d377756-1719-4a6f-9b07-089f7d73cbc2.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/2eac8dad-ea36-4350-92ad-561f0281b53e.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/30893ea5-ba63-4eb8-813c-058fca8de958.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/320dc06a-e9ff-4e6f-bfcf-8b541aa94419.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/35d6af9d-6110-4d70-8a3c-ab34a826c135.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/37817c9a-cc90-4e40-ac41-f6a7b3fc0646.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/38582eee-906f-43d4-ae05-7db648cf16c4.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/3a1e229e-8f6d-4aee-a64d-8b7940e88b8c.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/3aa0ba1e-7041-476e-8f1b-4864a73b6a07.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/3bcae58a-8ab6-42a0-bc0d-c3ec4b5bb2f9.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/3daa2f83-df6a-45d4-b88f-e7405bc2e146.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/3e39aeed-faa6-4996-8c26-c634059b1d34.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/3e6d48f9-7bee-4aed-86c3-614292bc91c0.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/4094974e-99e3-4656-b411-521a81f4966c.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/4108b7a4-d067-47f4-8282-c5427ef42ac6.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/420937c6-ab95-42d0-843a-60b6e72e74ca.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/4237b495-3dd2-42a4-95c8-800ccd366adb.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/429311b1-7fc3-49f4-9318-a055d3db36b1.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/43cd617d-6384-4354-bf59-01ae47542c06.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/451c8006-dadc-406d-84bb-5c2e6b63fb4d.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/48208ff3-35a7-4036-8441-06ca6cb05b1b.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/485428d7-510a-43e7-ba36-f33e14db00e0.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/49c541df-d422-4b86-a135-22a8de4dbbf5.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/4a85f7c7-e028-481a-844c-69db60ff1b09.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/4af7d38b-28fd-4177-ac96-01803c3fe98c.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/4b52f778-d441-4fc9-9f6e-5fffa7ea2a6e.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/4e4388c8-80de-4903-9e03-5e9ee99ed902.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/4f0e3fb9-160a-4876-8a34-80bdfd3e7557.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/51841b61-b168-4a70-8630-52f5d1603f32.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/54054354-3ed7-466c-8f34-b3c58e3e6cea.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/540b1f37-a2ec-4965-a61c-1bbdf540654b.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/5424e372-6113-4edb-ae39-3f3c86372bff.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/54a10919-e2b8-44e9-a28b-19dfeed3460d.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/5516aa7b-fa9d-4713-ba23-3447a3ea7203.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/584c0a89-5786-4660-b07f-fc832959eb2d.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/5918d3a3-c2bf-4fda-a819-1feaddef7d31.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/5cf95596-307c-4dee-a472-6869de7d96be.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/5e0c3d2c-f518-4c67-97b4-48e0d5d9122f.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/5e9f0838-1632-4dde-86e7-1cff89bee754.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/619f3978-d549-4d74-8591-4ebb50444d16.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/622d34b5-a5c1-4d37-9c17-c8053c1bbcf2.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/626168cb-b0ec-41f1-a133-db0c37fb9798.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/62d6e186-676d-4c00-9606-28d80a85ba6b.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/62e80b88-e559-4a2f-888e-e673274d21f0.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/64c3d21c-b324-4c1b-92cc-e4ee7b66e120.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/6525e10d-f406-4aa2-a425-6baa67271927.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/66c49379-1ac6-4411-9bec-dccd3a0eac6a.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/67c79ec0-b575-4cea-94a9-2272cce98485.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/680e3134-abc4-4c48-b2f4-c512a6c1b2de.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/6a9aed5b-24c7-4a72-83bd-3dc8ff303499.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/6b4b2006-5537-4b01-8df1-9547fc677a5a.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/6bd16d2f-9209-408a-89b9-29904c56d7c3.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/6c38b48c-bc8f-49dc-b044-1208902a81de.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/6c7530eb-2d06-4d3f-9050-a2678d1093da.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/6cb03559-4add-4f16-a054-9f2d64a5659e.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/6d4b2916-19a4-44cb-a8db-d253735b4443.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/6de3b3d9-a00a-4304-b2e3-e2eda9c6bf11.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/70c644f1-3e74-4afe-abb8-31bdefb3001f.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/71674679-bafa-485f-a6c4-4b2e67085c2a.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/742ab962-1667-4068-82ad-c858c865f163.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/74acfbd2-b197-43c3-ab63-8fa45f5d7a4f.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/74d10d06-a89f-423b-a6b0-8c1f50610c58.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/75877f4e-d91e-4b1f-84ef-c4236b07cfd6.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/76abfebe-1a7f-48f2-8d1b-bdbcfb42ae3f.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/7778e800-0099-4863-b70e-4dfa3cb85875.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/77ce46c8-f566-403b-9961-57d0fba29443.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/789a51d7-dbfe-4589-88aa-866f533edae4.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/79692749-6041-44cd-b599-999bb5abf9fc.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/7a60aa43-7734-4785-be70-f6384450adc1.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/7c24ed90-e50d-46b9-827f-1d55ab425c40.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/7d05c8e2-d9a0-4897-8026-fb9fe534504d.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/7eb183df-023e-41f8-8dee-ee03827bc8cc.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/80d59698-9954-4fd0-beb1-e12bdaee24f8.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/81e558ff-5cdb-447b-9900-b0affab79603.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/8214a455-d8f0-4dc8-bec0-4146635e8291.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/8525f4d6-6905-4c9f-bb8a-edccd3cea889.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/86a6f50d-8a44-4ae0-a70c-892dcfb78c1e.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/87a0f201-ea35-4e9e-8139-85cd3f3dbe36.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/89493252-d44e-470b-a8db-457de121d9fa.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/8a7041d6-cddd-4e41-a150-95c4ef213cda.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/8bf38f1a-3402-47bc-8630-cc8c62f895a4.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/8c2f56a7-6424-4b7c-bdb5-e999827da087.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/8cdde3a7-2b65-4704-aa45-25ea4d59c85f.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/8d7fa031-1c02-4a76-9aa4-9aaa82045c95.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/90075f21-0837-4cb3-a988-5d6eb00a5a9d.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/920281ab-5998-4c14-a43e-76807a5bfea3.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/92aaadbf-2604-4884-a5bf-16298af8f6f8.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/932be3b2-3735-4b62-a5f3-940280873e9a.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/93bbb652-3099-49c7-93d6-98d1a40e2831.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/9483ee9c-efdb-4cf8-8e83-9adf3645edaf.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/94b88232-0381-43ee-a831-5a59e5289b8c.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/952255bb-25e8-48c5-a8bc-9aeb73f32ce3.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/977ae62e-3c90-400f-a9c2-cbff98dae771.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/99df4853-51f2-41ab-a001-b8f90f4f3ef1.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/99ea4360-9268-4344-80a4-55c6013770e8.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/9b437d70-5c77-49fe-accb-8a0180b2f63e.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/9be8dd16-cec7-4300-bb75-2236e00df0ba.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/9c6811c7-1665-46c0-9dae-2b769df964f8.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/9d38698e-522e-4fc1-b580-b92294f86e26.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/9f363bcc-0141-4d44-8ca6-54cb1cff7ff0.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/9fb2d56d-6d0a-49fb-a3b1-b69984169740.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/a218f83d-1bcc-43ac-9cb0-7e342287f00f.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/a440da5d-1a5e-4d44-9ce7-679596d5e94b.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/a457bc9c-e7e6-46e4-9d70-090b89c3bf62.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/a4b24654-c703-406e-9099-05500b6dc4e5.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/a62b551f-b99b-45d5-bb1a-33fbd9a8f01e.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/a75f9e36-c008-40bd-9a49-eaff81c9fe2f.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/a95bd8e4-a693-4af6-8773-cfa27051f626.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/a9c90d7f-6b9f-444d-85cf-80b2267ab1b8.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/a9d79120-bfde-44ac-961e-73c332ba9f78.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/ab2d4704-e2ef-434b-a0fd-98a9ac7eb202.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/ad580103-b522-4b40-bd54-164f061720a9.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/adb0cf69-414b-4bd6-a69f-b96d3dd04d33.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/af54047f-f0b5-4bc3-a1d3-b790b8255acf.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/b26ee84d-6bf1-4677-83fa-be79842e13ce.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/b336ddd0-431c-4e82-8d95-892ea043d546.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/b3d85d83-88a4-480f-8541-cf4312eadf1f.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/b74a4a03-d902-4f00-a051-7d23a9ae674b.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/b9332565-6051-4717-8836-8be2e3beaa71.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/b9394ba6-1bab-4305-ac60-9715b9496cf2.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/bafddaee-7dc4-4326-9ed0-144072e60047.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/bc30672b-636d-4fba-bcd3-edcfe057e6bb.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/bc340b16-561f-4156-b2be-fa954228c814.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/bc613c43-6e25-431f-adb1-3e416eb096d7.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/bc687abe-5917-4bf7-accb-ad44c9c6be37.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/bd08e230-9270-4f98-ab7c-7cf133798fd2.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/bd0ae564-8b55-439b-bbab-fc446f1153c7.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/bd8ecbd9-b087-457a-a5c8-c681ad2c6083.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/bd9d13e5-296d-4e35-b0a5-68ee9ecfcacd.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/bf99f89a-a7f8-477f-9a63-54f2a2811b79.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/c1b725c1-b22f-41b2-ac75-1a0493041150.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/c1f233b1-caf9-4b60-9227-9cc44bfe6e4e.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/c1f67067-12f3-4f69-a8e8-2664ad8a2e57.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/c5c62695-0713-4e77-9ec0-d56041c917e7.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/c6ab0489-e1d3-406e-94a7-531aacb4285d.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/c6d84622-0e04-4e0b-ace3-e55aced59be9.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/c7743ab6-9e74-441c-af03-533b5769fb96.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/c933fbc7-78d7-48d0-a8d2-857ecc7a520b.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/c9ef6064-a6be-4d33-a5de-2d9a1396ca91.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/cae6a3e7-3492-4fe2-b3fe-51e59913421f.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/cc91b5be-1f7c-40ca-96fb-d31771ad77a5.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/cd071c70-b65b-465a-a6c5-d24c34363cf4.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/ce72d24c-6afd-4dd3-a48c-8bf57f649088.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/d2737346-0dc2-431d-871d-6101fbe4185e.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/d29f6cd7-6a99-41bd-86eb-2966018c4c4b.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/d5f98103-3e8b-45af-8765-135de8997390.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/d7937357-7da6-4391-8c60-7437182d56fb.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/d8ae2d1e-4836-48cd-ad55-4350ae7b4f7f.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/da46bd29-a602-43e3-b950-65cd24d6f65d.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/dae7c8ce-593c-4b38-b917-884223ec8fef.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/db265fe5-22f8-43fe-b3c0-fc954bb63e30.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/dbcfa8df-3bb4-47e9-af0d-d59c3ea8d7c5.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/deed0c00-4578-4d77-a092-9abbac36f27f.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/e00c2954-61d1-43ba-9a45-9027c9d49038.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/e0cf67ed-0605-4d61-9055-c3bef534670b.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/e1149543-4d0b-4d24-8307-feee5668ab68.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/e1483f71-f33d-446c-bfe4-56d318a5d3ba.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/e22d6979-9e82-42a7-ac83-50c8b97ec96e.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/e24d5b73-d032-4353-b9c7-b68d3e2c924c.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/e4328bd4-6507-47d5-a34b-d2322fec2813.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/e4e34058-35ea-4f59-9774-868f0d514725.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/e4e8880d-2cd0-46e8-99ce-bc9a1f107629.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/e89e0ada-f683-4a80-9092-9431c3fee950.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/e9870e66-f8c4-4ecd-9f11-6fa3c6abb7c5.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/ea3c92e1-6927-4899-8f42-67bce67bdf9f.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/ea96bcfe-41bc-470d-a1c1-f03bf0f43c8e.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/eb04c606-bce3-4e7f-b3ea-c07c1514d4e7.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/ed052ad9-03a3-4e2f-a77a-d62142129dee.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/ed3e1444-857d-46b9-8d58-eff12b24aac0.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/ee21afbe-a5f5-4fb9-bd59-e5ac5c78c569.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/ee39d7b2-c144-4783-a073-d0c9a4ad7914.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/ee5a4c34-adfe-47bd-b923-ca199a4d4ff6.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/ee5a79d4-77e3-4e3a-83f1-fa1244e1fab9.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/eef4eafc-ffad-4333-8222-0488f7b6786f.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/ef3975a6-ffbf-4c06-bfc3-44e2d9256d95.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/ef8f7bdb-7dd6-44ca-b4fa-d274b389fa18.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/f194cb4b-a988-4196-a9ed-8ae512d82dc5.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/f1f7160f-870a-4fca-84ad-6587b5022ca7.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/f2261ca0-030b-405d-8bca-fcddf7b2f345.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/f233eec1-b189-478c-b916-640653e336d5.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/f37224e7-0859-416a-95e5-8ac0deb6456b.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/f416b6dc-b3ed-4de2-9cb6-eacd57838a0f.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/f42ff34d-277c-4728-ae1a-127ac9a8879b.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/f4da1144-6066-4f91-949d-c0d6058a20ab.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/f548ecf9-3fe4-4d34-bb2f-f60ccefedcf0.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/f70d573e-216a-47a9-9f2f-7df1e529d482.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/f7838ddd-213f-454e-b1e2-82a2a77ab5a8.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/f7c94513-65f6-46ae-a949-9071d8cc73b3.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/f83373e1-44c0-4ee5-8be1-4fd19d8df5a0.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/fa971afc-f783-41a9-bd69-97ee31656afc.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/fbbdd7d6-3b25-4cbb-aaa3-31ecc43f3a64.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/fd80e621-51a7-444d-af22-99458fc23180.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/fe2555b6-e291-4fb7-a7b6-c0c405acbfb3.root',
        '/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/306/00000/fe7ea4be-fc09-43fd-a244-8313324b493e.root'
    ),
    lumisToProcess = cms.untracked.VLuminosityBlockRange("380306:28-380306:273"),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    TryToContinue = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    holdsReferencesToDeleteEarly = cms.untracked.VPSet(),
    makeTriggerResults = cms.obsolete.untracked.bool,
    modulesToCallForTryToContinue = cms.untracked.vstring(),
    modulesToIgnoreForDeleteEarly = cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:10000'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.NANOAODoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAOD'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:step2.root'),
    outputCommands = process.NANOAODEventContent.outputCommands
)



# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run3_data_prompt', '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequence)
process.NANOAODoutput_step = cms.EndPath(process.NANOAODoutput)
#process.DQMoutput_step = cms.EndPath(process.DQMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.NANOAODoutput_step) #,process.DQMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)




# process.ak4ScoutingJetParticleNetJetTagInfos = cms.EDProducer("DeepBoostedJetTagInfoProducer",
#     jet_radius = cms.double(0.4),
#     min_jet_pt = cms.double(5.0),
#     max_jet_eta = cms.double(2.5),
#     min_pt_for_track_properties = cms.double(0.95),
#     min_pt_for_pfcandidates = cms.double(0.1),
#     use_puppiP4 = cms.bool(False),
#     include_neutrals = cms.bool(True),
#     sort_by_sip2dsig = cms.bool(False),
#     min_puppi_wgt = cms.double(-1.0),
#     flip_ip_sign = cms.bool(False),
#     sip3dSigMax = cms.double(-1.0),
#     use_hlt_features = cms.bool(False),
#     pf_candidates = cms.InputTag("scoutingPFCands"),
#     jets = cms.InputTag("ak4ScoutingJets"),
#     puppi_value_map = cms.InputTag(""),
#     use_scouting_features = cms.bool(True),
#     normchi2_value_map = cms.InputTag("scoutingPFCands", "normchi2"),
#     dz_value_map = cms.InputTag("scoutingPFCands", "dz"),
#     dxy_value_map = cms.InputTag("scoutingPFCands", "dxy"),
#     dzsig_value_map = cms.InputTag("scoutingPFCands", "dzsig"),
#     dxysig_value_map = cms.InputTag("scoutingPFCands", "dxysig"),
#     lostInnerHits_value_map = cms.InputTag("scoutingPFCands", "lostInnerHits"),
#     quality_value_map = cms.InputTag("scoutingPFCands", "quality"),
#     trkPt_value_map = cms.InputTag("scoutingPFCands", "trkPt"),
#     trkEta_value_map = cms.InputTag("scoutingPFCands", "trkEta"),
#     trkPhi_value_map = cms.InputTag("scoutingPFCands", "trkPhi"),
# )


# # Load the TensorFlow B-Tagger plugin
# thisdir = os.path.dirname(os.path.abspath(__file__))
# datadir = os.path.join(thisdir, "src", "data")

# process.load("PhysicsTools.NanoAOD.myPlugin_cfi")
# process.myPlugin.graphPath = cms.string(os.path.join(datadir, "graph.pb"))
# process.myPlugin.inputTensorName = cms.string("input")
# process.myPlugin.outputTensorName = cms.string("output")
# process.myPlugin.src = cms.InputTag("ak4ScoutingJetParticleNetJetTagInfos")




# # Include b-tagging sequence in the process path
# process.p = cms.Path(
#     process.nanoSequence +
#     process.myPlugin # Keep the existing NanoAOD sequence
# )

# process.schedule.extend([process.p])

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

