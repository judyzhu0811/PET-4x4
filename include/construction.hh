#ifndef CONSTRUCTION_HH
#define CONSTRUCTION_HH

#include "G4VUserDetectorConstruction.hh"
#include "G4VPhysicalVolume.hh"
#include "G4LogicalVolume.hh"
#include "G4Box.hh"
#include "G4PVPlacement.hh"
#include "G4NistManager.hh"
#include "G4SystemOfUnits.hh"
#include "G4OpticalSurface.hh"
#include "G4LogicalSkinSurface.hh"

// Forward declare your sensitive detector class if needed
// class Detector;

class MyDetectorConstruction : public G4VUserDetectorConstruction
{
public:
    // Constructor
    MyDetectorConstruction();

    // Destructor
    ~MyDetectorConstruction() override;

    // Build the geometry and return the physical world
    G4VPhysicalVolume* Construct() override;


private:
    // You can add pointers to important logical volumes here if needed
    // G4LogicalVolume* fLogicWorld;
    // G4LogicalVolume* fLogicTeflonShell;
    // G4LogicalVolume* fLogicLiquidXenon;
};

#endif // CONSTRUCTION_HH
