#include "detector.hh"
#include "run.hh"

MySensitiveDetector::MySensitiveDetector(G4String name) : G4VSensitiveDetector(name)
{}

MySensitiveDetector::~MySensitiveDetector()
{}

G4bool MySensitiveDetector::ProcessHits(G4Step *aStep, G4TouchableHistory *ROhist)
{
    G4Track *track = aStep->GetTrack();

    track->SetTrackStatus(fStopAndKill);

    G4StepPoint *preStepPoint = aStep->GetPreStepPoint();
    G4StepPoint *postStepPoint = aStep->GetPostStepPoint();

    G4ThreeVector posPhoton = preStepPoint->GetPosition();

    //G4cout << "Photon position: " << posPhoton << G4endl;

    const G4VTouchable *touchable = aStep->GetPreStepPoint()->GetTouchable();

    G4int copyNo = touchable->GetCopyNumber();

    //G4cout << "Copy number: " << copyNo << G4endl;

    G4VPhysicalVolume *physVol = touchable->GetVolume();
    G4ThreeVector posDetector = physVol->GetTranslation();

    //G4cout << "Detector position: " << posDetector << G4endl;

    if (posDetector[0] == -16.25) {
        if (posDetector[1] == -16.25) {
            det7++;
        } else if (posDetector[1] == 0) {
            det4++;
        } else {
            det1++;
        }
    } else if (posDetector[0] == 0) {
       if (posDetector[1] == -16.25) {
            det8++;
        } else if (posDetector[1] == 0) {
            det5++;
        } else {
            det2++;
        }
    } else {
       if (posDetector[1] == -16.25) {
            det9++;
        } else if (posDetector[1] == 0) {
            det6++;
        } else {
            det3++;
        }
    }

    // G4cout << "det1: " << det1 << "\n";
    // G4cout << "det2: " << det2 << "\n";
    // G4cout << "det3: " << det3 << "\n";
    // G4cout << "det4: " << det4 << "\n";
    // G4cout << "det5: " << det5 << "\n";
    // G4cout << "det6: " << det6 << "\n";
    // G4cout << "det7: " << det7 << "\n";
    // G4cout << "det8: " << det8 << "\n";
    // G4cout << "det9: " << det9 << "\n";

    G4int evt = G4RunManager::GetRunManager()->GetCurrentEvent()->GetEventID();

    // G4AnalysisManager *man = G4AnalysisManager::Instance();
    // man->FillNtupleIColumn(0, evt);
    // man->FillNtupleDColumn(1, posDetector[0]);
    // man->FillNtupleDColumn(2, posDetector[1]);
    // man->AddNtupleRow(0);

    return true;
}
