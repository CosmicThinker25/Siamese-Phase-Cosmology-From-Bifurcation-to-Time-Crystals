#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_phase_portrait_emergent_time.py

Genera la figura:
  "Phase Portrait of Emergent Time via Limit Cycle"

- Integra un oscilador de Van der Pol (forma clásica) para obtener
  transitorio + ciclo límite.
- Dibuja retrato de fase (Δφ vs dΔφ/dτ) y añade anotaciones.
- Guarda en: figs/figs_phase_portrait_emergent_time.png

Uso:
  python src/make_phase_portrait_emergent_time.py
  python src/make_phase_portrait_emergent_time.py --mu 1.2 --steps 20000 --dt 0.01
"""

from __future__ import annotations

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt


def integrate_vdp(mu: float, dt: float, steps: int, x0: float, v0: float, show_progress: bool) -> tuple[np.ndarray, np.ndarray]:
    """
    Integra Van der Pol:
        x'' - mu(1 - x^2)x' + x = 0
    =>  x'' = mu(1 - x^2)x' - x
    """
    x = float(x0)
    v = float(v0)

    xs = np.empty(int(steps), dtype=float)
    vs = np.empty(int(steps), dtype=float)

    # Progreso simple sin dependencias externas (tqdm)
    # para cumplir tu preferencia de "cuanto más sencillo mejor".
    checkpoint = max(1, steps // 20)

    for i in range(steps):
        a = mu * (1.0 - x * x) * v - x
        v += a * dt
        x += v * dt
        xs[i] = x
        vs[i] = v

        if show_progress and (i % checkpoint == 0 or i == steps - 1):
            pct = int(100 * (i + 1) / steps)
            print(f"\rIntegrating: {pct:3d}% ", end="")

    if show_progress:
        print("\nDone.")

    return xs, vs


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate phase portrait figure for emergent time via limit cycle.")
    parser.add_argument("--mu", type=float, default=1.2, help="Van der Pol nonlinearity parameter (mu). Default: 1.2")
    parser.add_argument("--dt", type=float, default=0.01, help="Integration step in relational parameter τ. Default: 0.01")
    parser.add_argument("--steps", type=int, default=20000, help="Number of integration steps. Default: 20000")
    parser.add_argument("--x0", type=float, default=0.1, help="Initial Δφ. Default: 0.1")
    parser.add_argument("--v0", type=float, default=0.0, help="Initial dΔφ/dτ. Default: 0.0")
    parser.add_argument("--transient", type=int, default=12000,
                        help="Index where we consider transient finished; after this we highlight the limit cycle. Default: 12000")
    parser.add_argument("--out", type=str, default="figs/figs_phase_portrait_emergent_time.png",
                        help="Output path. Default: figs/figs_phase_portrait_emergent_time.png")
    parser.add_argument("--dpi", type=int, default=300, help="Output DPI. Default: 300")
    parser.add_argument("--no-progress", action="store_true", help="Disable progress printing.")

    args = parser.parse_args()

    # Ensure output directory exists
    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    xs, vs = integrate_vdp(
        mu=args.mu,
        dt=args.dt,
        steps=args.steps,
        x0=args.x0,
        v0=args.v0,
        show_progress=not args.no_progress,
    )

    # Split into transient + limit cycle segment
    transient = int(args.transient)
    transient = max(0, min(transient, len(xs) - 1))
    xs_tr = xs[:transient]
    vs_tr = vs[:transient]
    xs_cy = xs[transient:]
    vs_cy = vs[transient:]

    # Figure
    plt.figure(figsize=(7.5, 7.5))

    # Transient (thin)
    plt.plot(xs_tr, vs_tr, linewidth=1.2)

    # Limit cycle (thick)
    plt.plot(xs_cy, vs_cy, linewidth=4.0)

    # Axes lines
    plt.axhline(0, linewidth=1.2)
    plt.axvline(0, linewidth=1.2)

    plt.xlabel(r'$\Delta \phi$', fontsize=16)
    plt.ylabel(r'$\dot{\Delta \phi}\equiv d\Delta\phi/d\tau$', fontsize=16)
    plt.title('Phase Portrait of Emergent Time via Limit Cycle', fontsize=16, pad=14)

    # Mark origin
    plt.scatter([0], [0], s=60)

    # Annotations (matching the figure style)
    plt.annotate(
        r'$\Delta\phi=0$' + '\n(Timeless Vacuum / Platonia)',
        xy=(0, 0),
        xytext=(-2.2, -2.3),
        arrowprops=dict(arrowstyle='->', lw=1.2),
        fontsize=12,
        ha='left'
    )

    plt.annotate(
        'Vacuum Instability\n(Negative Damping)',
        xy=(0.4, 0.2),
        xytext=(-2.6, 1.8),
        arrowprops=dict(arrowstyle='->', lw=1.2),
        fontsize=12,
        ha='left'
    )

    # Choose representative points on limit cycle for arrows
    if len(xs_cy) > 10:
        idx1 = len(xs_cy) // 5
        idx2 = len(xs_cy) // 2
        pt1 = (xs_cy[idx1], vs_cy[idx1])
        pt2 = (xs_cy[idx2], vs_cy[idx2])
    else:
        pt1 = (xs[-1], vs[-1])
        pt2 = (xs[-1], vs[-1])

    plt.annotate(
        'Positive Damping Region\n(Stabilization)',
        xy=pt1,
        xytext=(1.6, 2.2),
        arrowprops=dict(arrowstyle='->', lw=1.2),
        fontsize=12,
        ha='left'
    )

    plt.annotate(
        'Time Crystal Phase\n(STTSB / Stable Limit Cycle)',
        xy=pt2,
        xytext=(1.4, -2.6),
        arrowprops=dict(arrowstyle='->', lw=1.2),
        fontsize=12,
        ha='left'
    )

    # Arrow of time: point on transient trajectory (choose a safe index)
    j = min(4000, len(xs_tr) - 1) if len(xs_tr) > 0 else 0
    plt.annotate(
        'Emergence of\nArrow of Time',
        xy=(xs[j], vs[j]),
        xytext=(-3.0, -0.2),
        arrowprops=dict(arrowstyle='->', lw=1.2),
        fontsize=12,
        ha='left'
    )

    plt.xlim(-3.5, 3.5)
    plt.ylim(-3.5, 3.5)

    plt.tight_layout()
    plt.savefig(args.out, dpi=args.dpi)
    print(f"Saved figure to: {args.out}")


if __name__ == "__main__":
    main()
