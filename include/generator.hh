#ifndef GENERATOR_HH
#define GENERATOR_HH

#include "G4VUserPrimaryGeneratorAction.hh"

#include "G4ParticleGun.hh"
#include "G4SystemOfUnits.hh"
#include "G4ParticleTable.hh"

class MyPrimaryGenerator : public G4VUserPrimaryGeneratorAction
{
public:
    MyPrimaryGenerator();
    ~MyPrimaryGenerator();
    G4ThreeVector GetEmissionPosition() const { return fEmissionPos; }
    virtual void GeneratePrimaries(G4Event*);
    G4int GetNPhotons() const { return fNPhotons; }
    

private:
    G4ParticleGun *fParticleGun;
    G4ThreeVector fEmissionPos;
    G4int fNPhotons;
};

#endif

