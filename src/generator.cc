#include "generator.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4OpticalPhoton.hh"
#include "Randomize.hh"

MyPrimaryGenerator::MyPrimaryGenerator()
{
    fParticleGun = new G4ParticleGun(1);
    fNPhotons = 15000;
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

    //Randomize the emission position per event ---
    G4double x0 = (G4UniformRand() - 0.5) * 70.0*mm; // ±10 mm in x
    G4double y0 = (G4UniformRand() - 0.5) * 70.0*mm;// ±10 mm in y
    G4double z0 = 17.5*mm; //1mm
    fEmissionPos = G4ThreeVector(x0, y0, z0);
    fParticleGun->SetParticlePosition(fEmissionPos);

    for (int i = 0; i < fNPhotons; i++)
    {
        G4double costheta = 2.0*G4UniformRand() - 1.0;  
        G4double sintheta = std::sqrt(1.0 - costheta*costheta);
        G4double phi = 2.0 * CLHEP::pi * G4UniformRand();

        G4double x = sintheta * std::cos(phi);
        G4double y = sintheta * std::sin(phi);
        G4double z = costheta;

        G4ThreeVector mom(x, y, z);
        fParticleGun->SetParticleMomentumDirection(mom.unit());

        G4ThreeVector normal = mom.orthogonal();
        G4ThreeVector polarization =
            normal*std::cos(2*CLHEP::pi*G4UniformRand()) +
            mom.cross(normal)*std::sin(2*CLHEP::pi*G4UniformRand());
        fParticleGun->SetParticlePolarization(polarization);

        fParticleGun->GeneratePrimaryVertex(anEvent);
    }
}