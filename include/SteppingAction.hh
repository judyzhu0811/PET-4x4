#include "G4UserSteppingAction.hh"

class MyEventAction;

class MySteppingAction : public G4UserSteppingAction {
public:
    explicit MySteppingAction(MyEventAction* eventAction);
    ~MySteppingAction() override = default;

    void UserSteppingAction(const G4Step*) override;

private:
    MyEventAction* fEventAction;
};
