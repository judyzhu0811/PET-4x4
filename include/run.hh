#ifndef RUN_HH
#define RUN_HH

#include "G4UserRunAction.hh"
#include "G4Run.hh"
#include "globals.hh"
#include <fstream>
#include "G4ThreeVector.hh"


class MyRunAction : public G4UserRunAction
{
public:
    MyRunAction();
    ~MyRunAction();

    virtual void BeginOfRunAction(const G4Run*);
    virtual void EndOfRunAction(const G4Run*);

    void WriteEventRow(const std::array<int,17> &row, double LCE, G4ThreeVector pos);
private:
  std::ofstream fCsv;
    
};

#endif
