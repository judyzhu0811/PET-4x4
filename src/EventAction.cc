
#include "EventAction.hh"
#include "run.hh"

#include "G4Event.hh"
#include "G4RunManager.hh"
#include "generator.hh"



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

MyEventAction::MyEventAction(MyRunAction* runAction):fRunAction(runAction){
    fSipmCounts.fill(0);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void MyEventAction::BeginOfEventAction(const G4Event* )
{
    fSipmCounts.fill(0);
    int EventID = (G4EventManager::GetEventManager())->GetConstCurrentEvent()->GetEventID();
    fSipmCounts[0] = EventID;
}

void MyEventAction::AddHit(int sipm_id){
    if (sipm_id >= 0 && sipm_id < 16) {
        fSipmCounts[sipm_id+1]++;
    }
}
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void MyEventAction::EndOfEventAction(const G4Event*)
{
    int N_collected = 0;
    for (int i = 1; i <= 16; i++) {
        N_collected += fSipmCounts[i];
    }

    const MyPrimaryGenerator* generator =
        static_cast<const MyPrimaryGenerator*>(
            G4RunManager::GetRunManager()->GetUserPrimaryGeneratorAction()
        );

    int nPhotons = generator->GetNPhotons();

    G4double LCE = 100.0 * static_cast<G4double>(N_collected) / nPhotons;

    G4ThreeVector pos = generator->GetEmissionPosition();

    if (fRunAction) {
        fRunAction->WriteEventRow(fSipmCounts, LCE, pos);
    }
}
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......


