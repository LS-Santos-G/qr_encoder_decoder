import numpy as np
import matplotlib.pyplot as plt
from encoder import Encoder
from decoder import decode_matrix, read_format
import channel as C

MENSAJE = "abc"
INTENTOS = 200
DANOS = np.arange(0, 0.121, 0.01)
rng = np.random.default_rng(0)


def crear(mensaje, nivel):
    e = Encoder(mensaje, nivel)
    e.encode_string_text()
    return e.final_matrix_output().astype(int)


print("PRUEBA 1: sin daño")
for nivel in "LMQH":
    m = crear(MENSAJE, nivel)
    print(" ", nivel, read_format(m), decode_matrix(m), "OK" if decode_matrix(m) == MENSAJE else "MAL")

for nombre, dañar in [("módulos al azar", C.flip_exact), ("mancha", C.burst)]:
    print(f"\nPRUEBA 2: daño {nombre}  (% de lecturas correctas)")
    plt.figure(nombre)
    print("  daño " + "".join(f"{d:>5.0%}" for d in DANOS))
    for nivel in "LMQH":
        m = crear(MENSAJE, nivel)
        tasa = [np.mean([decode_matrix(dañar(m, d, rng)) == MENSAJE for _ in range(INTENTOS)]) for d in DANOS]
        limite = max([d for d, t in zip(DANOS, tasa) if t >= 0.95], default=0)
        print(f"  {nivel}    " + "".join(f"{t*100:>5.0f}" for t in tasa) + f"   límite 95%: {limite:.0%}")
        plt.plot(DANOS * 100, np.array(tasa) * 100, label=nivel)
    plt.legend(); plt.xlabel("% dañado"); plt.ylabel("% lecturas correctas"); plt.grid(alpha=.3)

m = crear("Grupo 1", "H")
fig, ax = plt.subplots(1, 2)
for a, img, t in zip(ax, [m, C.flip_exact(m, 0.03, rng)], ["original", "dañado 3%"]):
    a.imshow(img, cmap="gray_r"); a.set_title(t); a.axis("off")
plt.show()
