#include "generator.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4OpticalPhoton.hh"
#include "Randomize.hh"
#include "CLHEP/Units/SystemOfUnits.h"
#include "CLHEP/Units/PhysicalConstants.h"

MyPrimaryGenerator::MyPrimaryGenerator()
{
    fParticleGun = new G4ParticleGun(1);
    fNPhotons = 150000;

    G4ParticleDefinition* particle = G4OpticalPhoton::OpticalPhotonDefinition();
    fParticleGun->SetParticleDefinition(particle);
    fParticleGun->SetParticleEnergy(6.98*eV);

    fEmissionPos = G4ThreeVector(0., 0., 0.);
    fParticleGun->SetParticlePosition(fEmissionPos);
}

MyPrimaryGenerator::~MyPrimaryGenerator()
{
    delete fParticleGun;
}

void MyPrimaryGenerator::GeneratePrimaries(G4Event *anEvent)
{
    // ---------------- S2 ELECTROLUMINESCENCE REGION ----------------

    // geometry match to your anode definition in construction.cc
    G4double anodeHalfXY = 34.0*mm;
    G4double elThickness = 0.5*mm;

    // reconstruct anode Z (must match construction.cc)
    G4double anodeHalfZ  = 0.25*mm;
    G4double sipmBottom = 0.024*m - 0.001*m;
    G4double anodeZ = sipmBottom - 14*mm - anodeHalfZ;

    // XY uniform within active area
    G4double x0 = (G4UniformRand() - 0.5) * 2.0 * anodeHalfXY;
    G4double y0 = (G4UniformRand() - 0.5) * 2.0 * anodeHalfXY;

    // thin EL layer near anode wires
    G4double z0 = anodeZ + (G4UniformRand() - 0.5) * elThickness;

    fEmissionPos = G4ThreeVector(x0, y0, z0);
    fParticleGun->SetParticlePosition(fEmissionPos);

    // ---------------- photon generation ----------------

    for (int i = 0; i < fNPhotons; i++)
    {
        G4double costheta = 2.0*G4UniformRand() - 1.0;
        G4double sintheta = std::sqrt(1.0 - costheta*costheta);
        G4double phi = 2.0 * CLHEP::pi * G4UniformRand();

        G4ThreeVector mom(
            sintheta * std::cos(phi),
            sintheta * std::sin(phi),
            costheta
        );

        fParticleGun->SetParticleMomentumDirection(mom.unit());

        // polarization (unchanged)
        G4ThreeVector normal = mom.orthogonal();
        G4ThreeVector polarization =
            normal*std::cos(2*CLHEP::pi*G4UniformRand()) +
            mom.cross(normal)*std::sin(2*CLHEP::pi*G4UniformRand());

        fParticleGun->SetParticlePolarization(polarization);

        fParticleGun->GeneratePrimaryVertex(anEvent);
    }
}