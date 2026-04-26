"""
Windkessel models for arterial blood pressure simulation.

Implements 2-element and 3-element Windkessel models with Euler and RK4 solvers.
"""

import numpy as np


def pulsatile_flow(t: np.ndarray, f: float = 1.0, amplitude: float = 80.0,
                   baseline: float = 20.0) -> np.ndarray:
    """Generate a pulsatile cardiac output waveform (positive half-sine).

    Parameters
    ----------
    t : array — time points (s)
    f : float — heart rate in Hz (default 1.0 = 60 bpm)
    amplitude : float — peak flow above baseline (mL/s)
    baseline : float — minimum flow (mL/s)

    Returns
    -------
    Qin : array — flow at each time point (mL/s)
    """
    return baseline + amplitude * np.maximum(0, np.sin(2 * np.pi * f * t))


def windkessel_2elem_euler(t: np.ndarray, Qin: np.ndarray,
                           R: float, C: float, P0: float) -> np.ndarray:
    """Solve 2-element Windkessel ODE using forward Euler.

    dP/dt = (1/C) * (Qin - P/R)

    Parameters
    ----------
    t : array — time points (s)
    Qin : array — input flow (mL/s)
    R : float — peripheral resistance (mmHg·s/mL)
    C : float — arterial compliance (mL/mmHg, e.g. 1.5e-3 = 1.5 mL/mmHg)
    P0 : float — initial pressure (mmHg)

    Returns
    -------
    P : array — arterial pressure (mmHg)
    """
    dt = t[1] - t[0]
    P = np.zeros_like(t)
    P[0] = P0

    for i in range(1, len(t)):
        dPdt = (1 / C) * (Qin[i - 1] - P[i - 1] / R)
        P[i] = P[i - 1] + dPdt * dt

    return P


def windkessel_2elem_analytical(t: np.ndarray, Qin_const: float,
                                 R: float, C: float, P0: float) -> np.ndarray:
    """Analytical solution for 2-element model with constant Qin.

    P(t) = Qin*R + (P0 - Qin*R) * exp(-t/(RC))

    Parameters
    ----------
    t : array — time points (s)
    Qin_const : float — constant input flow (mL/s)
    R : float — peripheral resistance (mmHg·s/mL)
    C : float — arterial compliance (mL/mmHg)
    P0 : float — initial pressure (mmHg)

    Returns
    -------
    P : array — arterial pressure (mmHg)
    """
    P_ss = Qin_const * R
    tau = R * C
    return P_ss + (P0 - P_ss) * np.exp(-t / tau)


def windkessel_3elem_rk4(t: np.ndarray, Qin: np.ndarray,
                          R1: float, R2: float, C: float,
                          P0: float) -> tuple[np.ndarray, np.ndarray]:
    """Solve 3-element Windkessel model using RK4.

    ODE:  dP/dt = (1/C) * (Qin - P/R2)
    Aortic pressure:  Pa = P + R1 * Qin

    Setting R1=0 reduces this to the 2-element model.

    Parameters
    ----------
    t : array — time points (s)
    Qin : array — input flow (mL/s)
    R1 : float — characteristic impedance (mmHg·s/mL)
    R2 : float — peripheral resistance (mmHg·s/mL)
    C : float — arterial compliance (mL/mmHg)
    P0 : float — initial distal pressure (mmHg)

    Returns
    -------
    P : array — distal pressure at RC junction (mmHg)
    Pa : array — aortic pressure (mmHg)
    """
    dt = t[1] - t[0]

    def dPdt(P_val, Qin_val):
        return (Qin_val - P_val / R2) / C

    P = np.zeros_like(t)
    P[0] = P0

    for i in range(len(t) - 1):
        Pi, qi = P[i], Qin[i]
        k1 = dPdt(Pi, qi)
        k2 = dPdt(Pi + 0.5 * dt * k1, qi)
        k3 = dPdt(Pi + 0.5 * dt * k2, qi)
        k4 = dPdt(Pi + dt * k3, qi)
        P[i + 1] = Pi + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0

    Pa = P + R1 * Qin
    return P, Pa


# ── Default physiological parameters ──
DEFAULT_PARAMS = {
    'C': 1.5e-3,     # arterial compliance (L/mmHg = 1.5 mL/mmHg)
    'R': 1.0,        # peripheral resistance (mmHg·s/mL)
    'R1': 0.05,      # characteristic impedance (mmHg·s/mL)
    'R2': 1.0,       # peripheral resistance for 3-elem (mmHg·s/mL)
    'f': 1.0,        # heart rate (Hz = 60 bpm)
    'amplitude': 80.0,  # flow amplitude (mL/s)
    'baseline': 20.0,   # baseline flow (mL/s)
    'P0': 80.0,      # initial pressure (mmHg)
    'dt': 0.001,     # time step (s)
    'tmax': 4.0,     # simulation duration (s)
}
