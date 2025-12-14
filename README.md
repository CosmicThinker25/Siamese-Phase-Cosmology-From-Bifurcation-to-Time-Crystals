# Time-Crystalline Emergence of Relational Time at a CPT-Symmetric Boundary

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17927003.svg)](https://doi.org/10.5281/zenodo.17927003)

## Overview

This repository contains the complete, reproducible implementation of the theoretical framework presented in the paper  
**“Time-Crystalline Emergence of Relational Time at a CPT-Symmetric Boundary.”**

The work proposes a minimal dynamical mechanism by which physical time emerges from an atemporal, CPT-invariant vacuum. Time is not assumed as a fundamental parameter, but arises as an ordered phase of a relational degree of freedom via spontaneous time-translation symmetry breaking (STTSB), analogous to a time-crystal phase.

---

## Scientific Motivation

Timeless formulations of quantum gravity suggest that the universe may originate from a static, atemporal state. In this work, we show that:

- An atemporal CPT-symmetric vacuum can be dynamically unstable.
- A nonlinear phase equation naturally develops a **stable limit cycle**.
- This limit cycle defines a **robust relational clock**, without introducing external time.
- The resulting phase exhibits properties directly analogous to **classical time crystals**.

Time therefore emerges as a **non-equilibrium dynamical phase**, not as a background structure.

---

## Repository Structure


---

## Reproducibility

This project is fully reproducible.

- All figures appearing in the paper are generated directly from the scripts provided in `src/`.
- No proprietary software or hidden steps are required.
- The numerical integration uses a minimal, transparent implementation of a nonlinear oscillator admitting a stable limit cycle.
- The LaTeX manuscript compiles without external bibliography files.

To reproduce the main phase-portrait figure:

```bash
python src/make_phase_portrait_emergent_time.py
