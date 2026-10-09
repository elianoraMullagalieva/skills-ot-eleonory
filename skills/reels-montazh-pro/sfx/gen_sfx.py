#!/usr/bin/env python3
"""Синтез мягких звуков интерфейса (без чужих сэмплов → без проблем с лицензией).

  python3 gen_sfx.py [папка=рядом со скриптом]
→ click, copy, paste, send, pop, whoosh, ding, type (.wav, 48 кГц, стерео, пик −6 дБ).
Звуки нарочно тихие и короткие: «звук на действии», а не музыка. Детерминированы (seed) — каждый раз одинаковые."""
import os, sys, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(7)


def t(d):
    return np.arange(int(SR * d)) / SR


def env(n, a=0.002, r=None, k=30):
    """Атака a с, экспоненциальный спад со скоростью k."""
    x = np.arange(n) / SR
    e = np.exp(-k * x)
    na = max(1, int(a * SR))
    e[:na] *= np.linspace(0, 1, na)
    return e


def svf(x, f, q=0.7, mode='bp'):
    """Фильтр с переменной частотой f (массив или число) — state variable."""
    f = np.broadcast_to(np.asarray(f, float), x.shape)
    lp = bp = 0.0
    out = np.empty_like(x)
    for i in range(len(x)):
        g = 2 * np.sin(np.pi * min(f[i], SR / 6) / SR)
        hp = x[i] - lp - bp / q
        bp += g * hp
        lp += g * bp
        out[i] = bp if mode == 'bp' else (lp if mode == 'lp' else hp)
    return out


def tick(freq=2200, d=0.04, k=120, noise=0.4):
    n = int(SR * d)
    s = np.sin(2 * np.pi * freq * t(d)) * 0.6 + svf(rng.standard_normal(n) * noise, freq * 1.5, 1.2)
    return s * env(n, 0.0008, k=k)


def click():
    return tick(2400, 0.06, 140, 0.5) + 0.3 * tick(1200, 0.06, 90, 0.1)


def pop():
    d = 0.08
    x = t(d)
    f = 820 * np.exp(-x * 18) + 260
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(len(x), 0.003, k=45)


def copy_():
    s = np.zeros(int(SR * 0.16))
    a, b = tick(1900, 0.06, 110, 0.3), tick(2600, 0.06, 120, 0.3)
    s[:len(a)] += a
    o = int(SR * 0.055)
    s[o:o + len(b)] += 0.8 * b
    return s


def paste():
    d = 0.12
    x = t(d)
    thump = np.sin(2 * np.pi * (170 + 60 * np.exp(-x * 40)) * x) * env(len(x), 0.002, k=38)
    s = 0.9 * thump
    tk = tick(1700, 0.05, 130, 0.35)
    s[:len(tk)] += 0.45 * tk
    return s


def send():
    d = 0.38
    n = int(SR * d)
    x = t(d)
    f = 500 + 2600 * (x / d) ** 1.5
    air = svf(rng.standard_normal(n), f, 2.5)
    e = np.sin(np.pi * np.clip(x / d, 0, 1)) ** 1.6
    blip = np.zeros(n)
    b = pop()[: int(SR * 0.06)]
    o = n - len(b) - int(SR * 0.02)
    blip[o:o + len(b)] = 0.35 * b
    return 0.5 * air * e + blip


def whoosh():
    d = 0.55
    n = int(SR * d)
    x = t(d)
    f = 2400 * np.exp(-x * 4) + 350
    air = svf(rng.standard_normal(n), f, 1.6)
    return air * np.sin(np.pi * x / d) ** 2


def ding():
    d = 0.9
    x = t(d)
    s = sum(a * np.sin(2 * np.pi * f * x) * np.exp(-x * k) for f, a, k in
            [(1318.5, 1, 4.5), (2637, .35, 7), (3637, .12, 10), (5274, .05, 14)])
    return s * env(len(x), 0.004, k=0)


def type_():
    s = np.zeros(int(SR * 0.42))
    pos = 0.0
    for i in range(6):
        k = tick(1800 + rng.integers(-300, 300), 0.035, 150, 0.6) * (0.6 + 0.4 * rng.random())
        o = int(pos * SR)
        s[o:o + len(k)] += k[: len(s) - o]
        pos += 0.055 + 0.03 * rng.random()
    return s


SOUNDS = {'click': click, 'copy': copy_, 'paste': paste, 'send': send, 'pop': pop,
          'whoosh': whoosh, 'ding': ding, 'type': type_}


def write(path, mono):
    mono = mono / (np.abs(mono).max() + 1e-9) * 0.5         # пик −6 дБ
    fade = min(len(mono), int(SR * 0.004))
    mono[-fade:] *= np.linspace(1, 0, fade)
    st = np.stack([mono, mono], 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype('<i2').tobytes())


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out, exist_ok=True)
    for name, fn in SOUNDS.items():
        write(os.path.join(out, f'{name}.wav'), fn())
        print('✓', name)
