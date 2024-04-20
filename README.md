# SHA-256 Collisions

This repository contains files related to the step-reduced SHA-256 collision
attack, specifically the SAT solver log files, encodings, and summaries of
collisions.

The `sfs` directory houses the files related to SFS collisions. Inside, the
`encodings` directory contains the SAT encodings for the versions of
step-reduced SHA-256 ranging from 20 to 38 steps. The `logs` directories contain
the SAT solver log files &mdash; each log file is named in the format:
`{steps}-{seed}-sfs-{solver}`. The collisions summary is in the `collisions.md`
files.
