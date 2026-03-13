#include "construction.hh"
#include "G4VisAttributes.hh"   
#include "G4SDManager.hh"
#include "G4LogicalVolumeStore.hh" 
#include "G4LogicalBorderSurface.hh"
#include "G4SubtractionSolid.hh"
#include "G4VSolid.hh"


MyDetectorConstruction::MyDetectorConstruction()
{
}

MyDetectorConstruction::~MyDetectorConstruction()
{
}

G4VPhysicalVolume *MyDetectorConstruction::Construct()
{
    G4NistManager *nist = G4NistManager::Instance();
	const G4int iNbEntries = 3; 

	//================================== elements ===================================
	G4Element* Xe = new G4Element("Xenon", "Xe", 54., 131.293 * g / mole);
	G4Element* H = new G4Element("Hydrogen", "H", 1., 1.0079 * g / mole);
	G4Element* C = new G4Element("Carbon", "C", 6., 12.011 * g / mole);
	G4Element* N = new G4Element("Nitrogen", "N", 7., 14.007 * g / mole);
	G4Element* O = new G4Element("Oxygen", "O", 8., 15.999 * g / mole);
	G4Element* F = new G4Element("Fluorine", "F", 9., 18.998 * g / mole);
	G4Element* Al = new G4Element("Aluminium", "Al", 13., 26.982 * g / mole);
	G4Element* Si = new G4Element("Silicon", "Si", 14., 28.086 * g / mole);
	G4Element* Cr = new G4Element("Chromium", "Cr", 24., 51.996 * g / mole);
	G4Element* Mn = new G4Element("Manganese", "Mn", 25., 54.938 * g / mole);
	G4Element* Fe = new G4Element("Iron", "Fe", 26., 55.85 * g / mole);
	G4Element* Ni = new G4Element("Nickel", "Ni", 28., 58.693 * g / mole);
	G4Element* Cu = new G4Element("Copper", "Cu", 29., 63.546 * g / mole);
	G4Element* Pb = new G4Element("Lead", "Pb", 82., 207.2 * g / mole);
	G4Element* Sn = new G4Element("Tin", "Sn", 50., 120.0 * g / mole);
	G4Element* B = nist->FindOrBuildElement("B");
	G4Element* Gd = nist->FindOrBuildElement("Gd");

	G4Element* Ca = new G4Element("Calcium", "Ca", 20., 40.078 * g / mole);

	G4Element* Mg = new G4Element("Mg", "Mg", 12., 24.3050 * g / mole);
	G4Element* K = new G4Element("K", "K", 19., 39.0983 * g / mole);
	G4Element* Na = new G4Element("Na", "Na", 11., 22.989769 * g / mole);
	G4Element* P = new G4Element("P", "P", 15., 30.973762 * g / mole);
	G4Element* S = new G4Element("S", "S", 16., 32.065 * g / mole);
	G4Element* Ti = new G4Element("Ti", "Ti", 22., 47.867 * g / mole);

	G4Element* Au = new G4Element("Au", "Au", 79., 196.96657 * g / mole);
	//================================== materials ==================================

	//----------------------------------- air ---------------------------------------
	G4Material *Air = nist->FindOrBuildMaterial("G4_AIR");

	//----------------------------------- water -------------------------------------
	G4Material *Water = new G4Material("Water", 1. * g / cm3, 2, kStateLiquid);
	Water->AddElement(H, 2);
	Water->AddElement(O, 1);

	//----------------------------------- vacuum ------------------------------------
	G4Material *Vacuum = new G4Material("Vacuum", 1.e-20 * g / cm3, 2, kStateGas);
	Vacuum->AddElement(N, 0.755);
	Vacuum->AddElement(O, 0.245);
	
	//------------------------------------ teflon -----------------------------------
	G4Material *Teflon = new G4Material("Teflon", 2.2 * g / cm3, 2, kStateSolid);
	Teflon->AddElement(C, 0.240183);
	Teflon->AddElement(F, 0.759817);
	G4OpticalSurface *pLXeTeflonOpticalSurface =
    new G4OpticalSurface("LXeTeflonOpticalSurface",
                         unified, ground, dielectric_metal);	//changed to polished instead of ground for debugging
	
	G4double pdTeflonPhotonMomentum[iNbEntries] = {6.91 * eV, 6.98 * eV,
                                                 7.05 * eV};
	G4double pdTeflonRefractiveIndex[iNbEntries] = {1.63, 1.61, 1.58};
	G4double pdTeflonReflectivity[iNbEntries] = {0.99, 0.99, 0.99};
	G4double pdTeflonSpecularLobe[iNbEntries] = {0.01, 0.01, 0.01};
	G4double pdTeflonSpecularSpike[iNbEntries] = {0.01, 0.01, 0.01};
	G4double pdTeflonBackscatter[iNbEntries] = {0.01, 0.01, 0.01};
	G4double pdTeflonEfficiency[iNbEntries] = {0.0, 0.0, 0.0};
	G4double pdTeflonAbsorbtionLength[iNbEntries] = {10 * m, 10 * m,
													10 * m};											
G4MaterialPropertiesTable* pTeflonPropertiesTable = new G4MaterialPropertiesTable();
/*pTeflonPropertiesTable->AddProperty("RINDEX", pdTeflonPhotonMomentum, pdTeflonRefractiveIndex, iNbEntries);
pTeflonPropertiesTable->AddProperty("ABSLENGTH", pdTeflonPhotonMomentum, pdTeflonAbsorbtionLength, iNbEntries);
pTeflonPropertiesTable->AddProperty("SPECULARLOBECONSTANT", pdTeflonPhotonMomentum, pdTeflonSpecularLobe, iNbEntries);
pTeflonPropertiesTable->AddProperty("SPECULARSPIKECONSTANT", pdTeflonPhotonMomentum, pdTeflonSpecularSpike, iNbEntries);
pTeflonPropertiesTable->AddProperty("BACKSCATTERCONSTANT", pdTeflonPhotonMomentum, pdTeflonBackscatter, iNbEntries);
pTeflonPropertiesTable->AddProperty("EFFICIENCY", pdTeflonPhotonMomentum, pdTeflonEfficiency, iNbEntries); */

Teflon->SetMaterialPropertiesTable(pTeflonPropertiesTable);
G4MaterialPropertiesTable* pLXeTeflonSurfaceTable = new G4MaterialPropertiesTable();

pLXeTeflonSurfaceTable->AddProperty("REFLECTIVITY", pdTeflonPhotonMomentum, pdTeflonReflectivity, iNbEntries);
pLXeTeflonSurfaceTable->AddProperty("EFFICIENCY", pdTeflonPhotonMomentum, pdTeflonEfficiency, iNbEntries);
pLXeTeflonOpticalSurface->SetMaterialPropertiesTable(pLXeTeflonSurfaceTable);
	//----------------------------------silicon--------------------------------------------
	G4Material* Silicon = nist->FindOrBuildMaterial("G4_Si");

G4double SiPhotonEnergy[iNbEntries] = {6.91*eV, 6.98*eV, 7.05*eV};
G4double SiRefractiveIndex[iNbEntries] = {3.4, 3.4, 3.4};   
G4double SiAbsLength[iNbEntries] = {1*mm, 1*mm, 1*mm};

G4MaterialPropertiesTable* SiMPT = new G4MaterialPropertiesTable();
SiMPT->AddProperty("RINDEX", SiPhotonEnergy, SiRefractiveIndex, iNbEntries);
SiMPT->AddProperty("ABSLENGTH", SiPhotonEnergy, SiAbsLength, iNbEntries);

Silicon->SetMaterialPropertiesTable(SiMPT);

	//----------------------------------- quartz ------------------------------------
	// ref: http://www.sciner.com/Opticsland/FS.htm
	G4Material *Quartz = new G4Material("Quartz", 2.201 * g / cm3, 2, kStateSolid,
										168.15 * kelvin, 1.5 * atmosphere);
	Quartz->AddElement(Si, 1);
	Quartz->AddElement(O, 2);

	// Optical properties Quartz
	const G4int iNbEntriesMatch = 5;
	G4double pdQuartzPhotonMomentum[iNbEntriesMatch] = {
		1. * eV, 6.9 * eV, 6.91 * eV, 6.98 * eV,
		7.05 * eV};  // SERENA: changed  2.*eV to 1.*eV otherwise it gets stuck
					// "Out of Range - Attempt to retrieve information below
					// range!"
	G4double pdQuartzRefractiveIndex[iNbEntriesMatch] = {1.50, 1.50, 1.50, 1.56,
														1.60};
	G4double pdQuartzAbsorbtionLength[iNbEntriesMatch] = {30 * m, 30 * m, 30 * m,
															30 * m, 30 * m};
	G4MaterialPropertiesTable *pQuartzPropertiesTable =
		new G4MaterialPropertiesTable();

	

	pQuartzPropertiesTable->AddProperty("RINDEX", pdQuartzPhotonMomentum,
										pdQuartzRefractiveIndex, iNbEntriesMatch);
	pQuartzPropertiesTable->AddProperty("ABSLENGTH", pdQuartzPhotonMomentum,
										pdQuartzAbsorbtionLength,
										iNbEntriesMatch);
	Quartz->SetMaterialPropertiesTable(pQuartzPropertiesTable);

	//---------------------------------liquid Xenon--------------------
	
	G4Material *LXe = new G4Material("LXe", 2.85 * g / cm3, 1, kStateLiquid, 177.05 * kelvin, 1.8 * atmosphere);
	LXe->AddElement(Xe, 1);

	G4double pdLXePhotonMomentum[iNbEntries] = { 6.91 * eV, 6.98 * eV, 7.05 * eV };
	G4double pdLXeScintillation[iNbEntries] = { 0.1,     1.0,     0.1 };
	G4double pdLXeRefractiveIndex[iNbEntries] = { 1.63,    1.61,    1.58 };
	G4double pdLXeAbsorbtionLength[iNbEntries] = { 5000. * cm, 5000. * cm, 5000. * cm }; //G4double pdLXeAbsorbtionLength[iNbEntries] = { 5000. * cm, 5000. * cm, 5000. * cm };
	G4double pdLXeScatteringLength[iNbEntries] = { 100. * cm,  100. * cm,  100. * cm };
// G4double pdLXeScatteringLength[iNbEntries] = { 30. * cm,  30. * cm,  30. * cm };

	G4MaterialPropertiesTable* pLXePropertiesTable = new G4MaterialPropertiesTable();

	// pLXePropertiesTable->AddProperty("SCINTILLATIONCOMPONENT1", pdLXePhotonMomentum, pdLXeScintillation, iNbEntries);
	// pLXePropertiesTable->AddProperty("SCINTILLATIONCOMPONENT2", pdLXePhotonMomentum, pdLXeScintillation, iNbEntries);
	pLXePropertiesTable->AddProperty("RINDEX", pdLXePhotonMomentum, pdLXeRefractiveIndex, iNbEntries);
	pLXePropertiesTable->AddProperty("ABSLENGTH", pdLXePhotonMomentum, pdLXeAbsorbtionLength, iNbEntries);
	pLXePropertiesTable->AddProperty("RAYLEIGH", pdLXePhotonMomentum, pdLXeScatteringLength, iNbEntries);

	pLXePropertiesTable->AddConstProperty("SCINTILLATIONYIELD", 40. / keV);
	pLXePropertiesTable->AddConstProperty("RESOLUTIONSCALE", 1.0);
	pLXePropertiesTable->AddConstProperty("SCINTILLATIONTIMECONSTANT1", 3. * ns);
	pLXePropertiesTable->AddConstProperty("SCINTILLATIONTIMECONSTANT2", 27. * ns);
	pLXePropertiesTable->AddConstProperty("SCINTILLATIONYIELD1", 1.0);

	LXe->SetMaterialPropertiesTable(pLXePropertiesTable);
    G4Material *worldMat = Vacuum;

//---------------Detector Construction----------
    
    G4Box *solidWorld = new G4Box("solidWorld", 0.05*m, 0.05*m, 0.05*m);
	G4Box *solidDetector = new G4Box("solidDetector", 0.0075*m, 0.0075*m, 0.001*m);
	G4LogicalVolume* logicDetector = new G4LogicalVolume(solidDetector, Silicon, "logicDetector");
//----------Liquid Xenon-------------
	G4double shrinkXY = 0.1*mm;
	G4double shrinkZ  = 0.1*mm;
	G4Box *solidLiquidXenon = new G4Box(
   	 "liquidXenon",
    0.035*m - shrinkXY,
    0.035*m - shrinkXY,
    0.025*m - shrinkZ
);
	G4LogicalVolume *logicWorld = new G4LogicalVolume(solidWorld, worldMat, "logicWorld");
    G4VPhysicalVolume *physWorld = new G4PVPlacement(0, G4ThreeVector(0., 0., 0.), logicWorld, "physWorld", 0, false, 0, true);
	
//------------Teflon Shell---------------
G4Box *solidTeflonShell = new G4Box("teflonShell", 0.035*m, 0.035*m, 0.025*m);
	G4LogicalVolume *logicTeflonShell = new G4LogicalVolume(solidTeflonShell, Teflon, "logicTeflon");
	G4VPhysicalVolume *physTeflonShell = new G4PVPlacement(
    0, G4ThreeVector(0., 0., 0.), logicTeflonShell, "physTeflonShell", logicWorld, false, 0, true
);
new G4LogicalSkinSurface("TeflonSurfaceSkin", logicTeflonShell, pLXeTeflonOpticalSurface);
G4LogicalVolume *logicLiquidXenon = new G4LogicalVolume(solidLiquidXenon, LXe, "logicLiquidXenon");
G4VPhysicalVolume *physLiquidXenon = new G4PVPlacement(
    0, G4ThreeVector(0., 0., 0.), logicLiquidXenon, "physLiquidXenon", logicTeflonShell, false, 0, true
);

//new G4LogicalBorderSurface("LXeToTeflon",
                           //physLiquidXenon,
                          // physTeflonShell,
                          // pLXeTeflonOpticalSurface);
						   
// --------------------------------Cathode---------------------------------------
G4Material* metalMaterial = nist->FindOrBuildMaterial("G4_Al");
G4double metalPhotonEnergy[iNbEntries] = {6.91*eV, 6.98*eV, 7.05*eV};
G4double metalReflectivity[iNbEntries] = {0.85, 0.85, 0.85};
G4double metalEfficiency[iNbEntries] = {0.0, 0.0, 0.0};
G4MaterialPropertiesTable* metalMPT = new G4MaterialPropertiesTable();
metalMPT->AddProperty("REFLECTIVITY", metalPhotonEnergy, metalReflectivity, iNbEntries);
metalMPT->AddProperty("EFFICIENCY", metalPhotonEnergy, metalEfficiency, iNbEntries);
G4OpticalSurface* cathodeOpticalSurface = new G4OpticalSurface("CathodeSurface",
    unified, ground, dielectric_metal);
cathodeOpticalSurface->SetMaterialPropertiesTable(metalMPT);
G4double cathodeHalfXY = 35*mm;          // half-size of cathode
G4int nSquares = 10;                      // 10×10 squares
G4int nWires = nSquares + 1;              // 11 wires along X and Y
G4double wireWidth = 1*micrometer;        // wire width
G4double wireThickness = 0.01*mm;         // wire thickness along Z
G4double squareSize = 6*mm;               // size of each square
G4double gap = 0.89*mm;                   // gap between squares
G4double edgeMargin = 0.995*mm;           // distance from edge to first wire
G4double wireSpacing = squareSize + gap;
// ---- Solid cathode plate ----
G4Box* cathodePlate = new G4Box("CathodePlate", cathodeHalfXY, cathodeHalfXY, wireThickness/2.);
G4VSolid* cathodeGrid = cathodePlate;

for (int i=0; i<10; i++) {
    for (int j=0; j<10; j++) {
        G4double x = -cathodeHalfXY + edgeMargin + i*(squareSize + gap) + squareSize/2.;
        G4double y = -cathodeHalfXY + edgeMargin + j*(squareSize + gap) + squareSize/2.;
        G4Box* hole = new G4Box("Hole", squareSize/2., squareSize/2., wireThickness);
        cathodeGrid = new G4SubtractionSolid("CathodeGrid", cathodeGrid, hole, 0, G4ThreeVector(x, y, 0));
    }
}
G4LogicalVolume* logicCathodeGrid = new G4LogicalVolume(cathodeGrid, metalMaterial, "logicCathodeGrid");
G4double cathodeZ = -0.024*m - wireThickness/2.;
new G4PVPlacement(0, G4ThreeVector(0., 0., cathodeZ),
                  logicCathodeGrid, "physCathode", logicLiquidXenon, false, 0, true);
new G4LogicalSkinSurface("CathodeSurface", logicCathodeGrid, cathodeOpticalSurface);
//----------------------------------- Quartz Anode Plate --------------------------------
G4double anodeHalfXY = 34*mm;   // 68 mm / 2
G4double anodeHalfZ  = 0.25*mm; // 0.5 mm / 2

G4Box* solidAnodeQuartz = new G4Box("anodeQuartz", anodeHalfXY, anodeHalfXY, anodeHalfZ);
G4LogicalVolume* logicAnodeQuartz = new G4LogicalVolume(solidAnodeQuartz, Quartz, "logicAnodeQuartz");
G4VisAttributes* quartzVis = new G4VisAttributes(G4Colour(0.5,0.5,1.0,0.3)); // semi-transparent blue
quartzVis->SetForceSolid(true);
logicAnodeQuartz->SetVisAttributes(quartzVis);
G4double sipmBottom = 0.024*m - 0.001*m;
G4double anodeZ = sipmBottom - 5*mm - anodeHalfZ; // G4double anodeZ = sipmBottom - 5*mm - anodeHalfZ;
new G4PVPlacement(0, G4ThreeVector(0.,0.,anodeZ),
                  logicAnodeQuartz, "physAnodeQuartz",
                  logicLiquidXenon, false, 0, true);
//---------------------Wires ------------------
G4OpticalSurface* anodeOpticalSurface = new G4OpticalSurface("AnodeSurface",
    unified, polished, dielectric_metal);
anodeOpticalSurface->SetMaterialPropertiesTable(metalMPT);
G4double anodeWireWidth       = 5*micrometer;   // along Y
G4double anodeWireThickness   = 1*micrometer;   // along Z
G4double anodeTopWireSpacing  = 1*mm;           // center-to-center along Y
G4double anodeVerticalOffset  = 0.5*mm;         // top wires above bottom wires

G4int nTopWires = static_cast<G4int>(68*mm / anodeTopWireSpacing);  //68 wires
G4int nBottomWires = nTopWires;
G4Box* solidTopWire = new G4Box("topWire", anodeHalfXY, anodeWireWidth/2., anodeWireThickness/2.);
G4LogicalVolume* logicTopWire = new G4LogicalVolume(solidTopWire, metalMaterial, "logicTopWire");
new G4LogicalSkinSurface("TopWireSurface", logicTopWire, anodeOpticalSurface);

G4Box* solidBottomWire = new G4Box("bottomWire", anodeHalfXY, anodeWireWidth/2., anodeWireThickness/2.);
G4LogicalVolume* logicBottomWire = new G4LogicalVolume(solidBottomWire, metalMaterial, "logicBottomWire");
new G4LogicalSkinSurface("BottomWireSurface", logicBottomWire, anodeOpticalSurface);
// Calculate starting position once
G4double totalGridWidth = (nTopWires - 1) * anodeTopWireSpacing + anodeWireWidth;
G4double yStart = -totalGridWidth / 2. + anodeWireWidth/2.;

// Bottom wires
G4double zBottom = -anodeHalfZ + anodeWireThickness/2.;
for(G4int i = 0; i < nBottomWires; i++){
    G4double y = yStart + i*anodeTopWireSpacing;
    new G4PVPlacement(0, G4ThreeVector(0., y, zBottom), logicBottomWire,
                      "physBottomWire", logicAnodeQuartz, false, i, true);
}
// Top wires (0.5 mm above bottom wires; closer to SiPMs)
G4double zTop = anodeHalfZ - anodeWireThickness/2.;
for(G4int i = 0; i < nTopWires; i++){
    G4double y = yStart + i*anodeTopWireSpacing;  // <-- use yStart here
    new G4PVPlacement(0, G4ThreeVector(0., y, zTop), logicTopWire,
                      "physTopWire", logicAnodeQuartz, false, i, true);
}

/*
//Bottom Wires
G4double zBottom = -anodeHalfZ + anodeWireThickness/2.;
for(G4int i=0; i<nBottomWires; i++){
     G4double y = -anodeHalfXY + anodeWireWidth/2. + i*anodeTopWireSpacing;
    new G4PVPlacement(0, G4ThreeVector(0., y, zBottom), logicBottomWire,
                      "physBottomWire", logicAnodeQuartz, false, i, true);
}
					  
// Top wires (0.5 mm above bottom wires; closer to SiPMs)
G4double zTop = anodeHalfZ - anodeWireThickness/2.;

for(G4int i=0; i<nTopWires; i++){
    G4double y = -anodeHalfXY + anodeWireWidth/2. + i*anodeTopWireSpacing;
    new G4PVPlacement(0, G4ThreeVector(0., y, zTop), logicTopWire,
                      "physTopWire", logicAnodeQuartz, false, i, true);
}
					  */


//----------------------4x4 SiPM grid------------------
G4int gridSize = 4;
G4double spacing = 0.01625*m;
G4double startPos = -spacing*(gridSize-1)/2;  // start at negative offset
G4double sipmZ = (0.025*m - shrinkZ) - 0.001*m - 0.1*mm; // 24mm - 1mm - 0.1mm = 22.9mm

for (G4int i = 0; i < gridSize; i++) {
    for (G4int j = 0; j < gridSize; j++) {
        G4ThreeVector pos(
            startPos + i*spacing,  // x
            startPos + j*spacing,  // y
           	sipmZ              // z
        );
        new G4PVPlacement(
            0, pos,
            logicDetector,
            "physDetector",
            logicLiquidXenon,
            false,
            i*gridSize + j,
            true
        );
    }
}

//------------------photo cathode------------------------
G4double PC_width = 5.95*mm;
G4double PC_thick = 1*mm;
auto solidPC = new G4Box("solidPhotocathode",PC_width*0.5,PC_width*0.5,PC_thick*0.5);
auto logicPC = new G4LogicalVolume(solidPC, metalMaterial,"logicPhotocathode");
G4double dx = 0.5*(PC_width+0.5*mm);
G4double pcZ = -0.5*(2*mm-PC_thick);
int k = 0;
for (int ix : {-1, +1}) {
  for (int iy : {-1, +1}) {
    new G4PVPlacement(
      nullptr,
      G4ThreeVector(ix*dx, iy*dx, pcZ),
      logicPC,
      "physPhotocathode",
      logicDetector,   
      false,
      k++,           
      true
    );
  }
}

G4double PCPhotonEnergy[iNbEntries] = {6.91*eV, 6.98*eV, 7.05*eV};
G4double PCReflectivity[iNbEntries] = {0.2, 0.2, 0.2};
G4double PCEfficiency[iNbEntries] = {1.0, 1.0, 1.0};
G4MaterialPropertiesTable* PCMPT = new G4MaterialPropertiesTable();
PCMPT->AddProperty("REFLECTIVITY", PCPhotonEnergy, PCReflectivity, iNbEntries);
PCMPT->AddProperty("EFFICIENCY", PCPhotonEnergy, PCEfficiency, iNbEntries);

G4OpticalSurface* PCOpticalSurface = new G4OpticalSurface("PCSurface",
    unified, polished, dielectric_metal);
PCOpticalSurface->SetMaterialPropertiesTable(PCMPT);

new G4LogicalSkinSurface("PCSurface", logicPC, PCOpticalSurface);
    
return physWorld; 
} 