"""Generate all figures for the repository."""
import sys
sys.path.insert(0, 'src')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from windkessel import (
    pulsatile_flow, windkessel_2elem_euler, windkessel_2elem_analytical,
    windkessel_3elem_rk4, DEFAULT_PARAMS
)

plt.rcParams.update({
    'figure.figsize': (12, 6), 'font.size': 12,
    'axes.grid': True, 'grid.alpha': 0.3, 'lines.linewidth': 2, 'figure.dpi': 150
})

BLUE, ORANGE, RED, GREEN, GRAY = '#2E75B6', '#E67E22', '#E74C3C', '#27AE60', '#888888'

p = DEFAULT_PARAMS
t = np.arange(0, p['tmax'], p['dt'])
Qin = pulsatile_flow(t, p['f'], p['amplitude'], p['baseline'])
half = len(t) // 2

# ── 1. 2-element simulation ──
P2 = windkessel_2elem_euler(t, Qin, p['R'], p['C'], p['P0'])
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(t, P2, color=BLUE, label='Arterial pressure P(t)')
ax.plot(t, Qin/np.max(Qin)*np.max(P2)*0.4, ':', color=GRAY, label=r'$Q_{in}$ (scaled)')
ax.set(xlabel='Time (s)', ylabel='P (mmHg)', title='2-Element Windkessel Model')
ax.legend()
plt.tight_layout()
fig.savefig('figures/sim_2elem.png', bbox_inches='tight')
plt.close()

# ── 2. 3-element simulation ──
Pd, Pa = windkessel_3elem_rk4(t, Qin, p['R1'], p['R2'], p['C'], p['P0'])
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(t, Pa, color=BLUE, label=r'Aortic pressure $P_a(t)$')
ax.plot(t, Pd, '--', color=ORANGE, label='Distal pressure P(t)')
ax.plot(t, Qin/np.max(Qin)*np.max(Pa)*0.4, ':', color=GRAY, label=r'$Q_{in}$ (scaled)')
ax.set(xlabel='Time (s)', ylabel='P (mmHg)', title='3-Element Windkessel Model (RK4)')
ax.legend()
plt.tight_layout()
fig.savefig('figures/sim_3elem.png', bbox_inches='tight')
plt.close()

# ── 3. Validation: constant Qin ──
Qc = 100.0
Qin_c = np.full_like(t, Qc)
P_an = windkessel_2elem_analytical(t, Qc, p['R'], p['C'], p['P0'])
P_nu = windkessel_2elem_euler(t, Qin_c, p['R'], p['C'], p['P0'])
err = np.abs(P_an - P_nu)

fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 7), height_ratios=[3, 1])
a1.plot(t, P_an, color=BLUE, label='Analytical')
a1.plot(t[::50], P_nu[::50], 'o', color=RED, ms=4, label='Euler')
a1.axhline(Qc*p['R'], color=GREEN, ls='--', alpha=0.5, label=f'Steady state = {Qc*p["R"]:.0f} mmHg')
a1.set(ylabel='P (mmHg)', title=f'Validation: Constant $Q_{{in}}$ = {Qc:.0f} mL/s')
a1.legend()
a2.plot(t, err, color=RED)
a2.set(xlabel='Time (s)', ylabel='|Error| (mmHg)')
plt.tight_layout()
fig.savefig('figures/validation_constant_qin.png', bbox_inches='tight')
plt.close()

# ── 4. 2 vs 3 element comparison ──
_, P2r = windkessel_3elem_rk4(t, Qin, 0, p['R'], p['C'], p['P0'])
_, P3r = windkessel_3elem_rk4(t, Qin, p['R1'], p['R2'], p['C'], p['P0'])
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(t, P2r, color=ORANGE, label='2-element: P(t)')
ax.plot(t, P3r, color=BLUE, label=r'3-element: $P_a(t)$')
ax.plot(t, Qin/np.max(Qin)*np.max(P3r)*0.35, ':', color=GRAY, alpha=0.7, label=r'$Q_{in}$ (scaled)')
ax.set(xlabel='Time (s)', ylabel='P (mmHg)', title='2-Element vs. 3-Element Windkessel Model')
ax.legend()
plt.tight_layout()
fig.savefig('figures/comparison_2v3.png', bbox_inches='tight')
plt.close()

# ── 5. Sensitivity analysis ──
fig, (a1, a2) = plt.subplots(1, 2, figsize=(16, 5))
for Cv, lb, co in [(0.5e-3,'C=0.5 (reduced)',RED),(1.5e-3,'C=1.5 (normal)',BLUE),(3e-3,'C=3.0 (high)',GREEN)]:
    _, Pa = windkessel_3elem_rk4(t, Qin, p['R1'], p['R2'], Cv, p['P0'])
    a1.plot(t, Pa, color=co, lw=1.8, label=lb)
a1.set(xlabel='Time (s)', ylabel=r'$P_a$ (mmHg)', title='Effect of Compliance (C)')
a1.legend(fontsize=9)

for Rv, lb, co in [(0.5,'R=0.5 (low)',GREEN),(1.0,'R=1.0 (normal)',BLUE),(2.0,'R=2.0 (hypertension)',RED)]:
    _, Pa = windkessel_3elem_rk4(t, Qin, p['R1'], Rv, p['C'], p['P0'])
    a2.plot(t, Pa, color=co, lw=1.8, label=lb)
a2.set(xlabel='Time (s)', ylabel=r'$P_a$ (mmHg)', title='Effect of Resistance (R)')
a2.legend(fontsize=9)
plt.tight_layout()
fig.savefig('figures/sensitivity_analysis.png', bbox_inches='tight')
plt.close()

print("All figures generated in figures/")
