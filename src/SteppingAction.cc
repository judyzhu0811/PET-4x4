#include "SteppingAction.hh"
#include "EventAction.hh"

#include "G4Step.hh"
#include "G4Track.hh"
#include "G4OpticalPhoton.hh"
#include "G4OpBoundaryProcess.hh"
#include "G4ProcessManager.hh"
#include "G4TouchableHandle.hh"

MySteppingAction::MySteppingAction(MyEventAction* eventAction)
: fEventAction(eventAction) {}

void MySteppingAction::UserSteppingAction(const G4Step* step)
{
    auto track = step->GetTrack();
    if (track->GetDefinition() != G4OpticalPhoton::Definition())
        return;

    auto post = step->GetPostStepPoint();
    if (post->GetStepStatus() != fGeomBoundary)
        return;

    static G4OpBoundaryProcess* boundary = nullptr;
    if (!boundary) {
        auto pm = track->GetDefinition()->GetProcessManager();
        for (int i = 0; i < pm->GetProcessListLength(); i++) {
            auto p = (*pm->GetProcessList())[i];
            if (p->GetProcessName() == "OpBoundary") {
                boundary = static_cast<G4OpBoundaryProcess*>(p);
                break;
            }
        }
    }
    if (!boundary) return;

    if (boundary->GetStatus() == Detection) {

       
        auto touch = post->GetTouchableHandle();
        int sipm_id = touch->GetCopyNumber(1); // depth=1 → physDetector

        fEventAction->AddHit(sipm_id);


    }
}
