#include "run.hh"
#include "G4AnalysisManager.hh"
#include <sstream>
#include "G4SystemOfUnits.hh"  

MyRunAction::MyRunAction() : G4UserRunAction() {}
MyRunAction::~MyRunAction() {
    if (fCsv.is_open()) fCsv.close();
}

void MyRunAction::BeginOfRunAction(const G4Run*)
{

  fCsv.open("hits_per_event.csv", std::ios::out);
  if (!fCsv.is_open()) {
    G4cerr << "ERROR: cannot open hits_per_event.csv" << G4endl;
    return;
  }

  // head
  fCsv << "event_id";
  for (int i = 0; i < 16; i++) fCsv << ",sipm" << i;
  fCsv << ",x(mm),y(mm),z(mm),LCE (%)\n";

}

void MyRunAction::EndOfRunAction(const G4Run*)
{
   if (fCsv.is_open()) fCsv.close();
}

void MyRunAction::WriteEventRow(const std::array<int, 17>& row, double LCE, G4ThreeVector pos) {
    if (!fCsv.is_open()) return;

    for (int i = 0; i < 17; i++) {
        fCsv << row[i];
        if (i != 16) fCsv << ",";
    }
    fCsv << "," << pos.x()/mm << "," << pos.y()/mm << "," << pos.z()/mm << "," << LCE << G4endl;
} 