
=============
Line_transfer
=============

Line_transfer
=============
The way in which line transfer and scattering is dealt with
in the code. Governs whether we adopt any approximations
for radiative transfer, whether to use the indivisible packet
and macro-atom machinery, and whether to use isotropic or
anisotropic scattering.

Mode 5 is recommended for non-macro atom runs,
while mode 7 is recommended for macro-atom runs.

**Type:** Enum (Int)

**Values:**

pure_abs. *Pure absorption*
   
   The pure absortion approximation.

pure_scat. *Pure scattering*
   
   The pure scattering approximation.

sing_scat. *Single scattering*
   
   The single scattering approximation.

escape_prob. *Escape probability*
   
   Resonance scattering and electron scattering is dealt with isotropically.
   free-free, compton and bound-free opacities attenuate the weight of the photon
   wind emission produces additional photons, which have their directions chosen isotropically.
   The amount of radiation produced is attenuated by the escape probability.

thermal_trapping. *Escape probability + anisotropic scattering*
   
   as mode 4, but we use
   the 'thermal trapping method' to choose an
   anistropic direction when an r-packet deactivation
   or scatter occurs.

macro_atoms. *Macro-atoms*
   
   use macro-atom line transfer.
   Packets are indivisible and thus all opacities are dealt with by activate a macro-atom, scattering,
   or creating a k-packet.
   the new direction following electron scattering or deactivation of
   a macro atom is chosen isotropically.

macro_atoms_thermal_trapping. *Macro-atoms + anisotropic scattering*
   
   as macro_atoms, but we use the 'thermal trapping method' to choose an anistropic direction
   when an r-packet deactivation or scatter occurs.


**Parent(s):**
  parameter_: Condition e.g. greater than 0 or list e.g. [1, 2, 5]


**File:** setup_domains.c


