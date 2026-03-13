#include "action.hh"
#include "run.hh"
#include "generator.hh" 
#include "EventAction.hh"
#include "SteppingAction.hh"

MyActionInitialization::MyActionInitialization()
{}

MyActionInitialization::~MyActionInitialization()
{}

void MyActionInitialization::Build() const
{
    MyPrimaryGenerator *generator = new MyPrimaryGenerator();
    SetUserAction(generator);

    MyRunAction *runAction = new MyRunAction();
    SetUserAction(runAction);

    MyEventAction* eventAction = new MyEventAction(runAction);
    SetUserAction(eventAction);

    SetUserAction(new MySteppingAction(eventAction));
}
