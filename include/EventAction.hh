#include "G4UserEventAction.hh"
#include "globals.hh"



class MyRunAction;

class MyEventAction : public G4UserEventAction
{
  public:
    MyEventAction(MyRunAction*);
    ~MyEventAction() override = default;

    void BeginOfEventAction(const G4Event* event) override;
    void EndOfEventAction(const G4Event* event) override;


  public:
    void AddHit(int sipm_id);
  private:
    std::array<int,17> fSipmCounts;
    MyRunAction* fRunAction = nullptr;

};





