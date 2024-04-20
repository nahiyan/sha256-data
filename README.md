# SHA-256 Collisions

This repository contains files related to the step-reduced SHA-256 collision
attack, specifically the SAT solver log files, encodings, and lists of
collisions.

The `sfs` directory houses the files related to SFS collisions. Inside, the
`encodings` directory contains the SAT encodings for the versions of
step-reduced SHA-256 ranging from 20 to 38 steps. The `logs` directories contain
the SAT solver log files&mdash;each named with the format,
`{steps}-{seed}-sfs-{solver}`. The collisions lists are in the `collisions.md`
files.
