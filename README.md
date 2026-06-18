# Windkessel model — matematičko modelovanje arterijskog pritiska

> Seminarski rad iz predmeta *Modeliranje dinamičkih sistema*.
> Modelovanje dinamike arterijskog pritiska pomoću dvoelementnog i troelementnog Windkessel modela, sa numeričkim simulacijama u Pythonu (Eulerova i Runge–Kutta metoda).

## Pregled rezultata

### Dvoelementni model
Pritisak prati pulsni ulazni protok; tokom dijastole opada eksponencijalno.

![Dvoelementni model](figures/plots/skrin1.jpeg)

### Troelementni model
Dodatni otpor R1 daje oštrije sistoličke vrhove, bliže stvarnim merenjima.

![Troelementni model](figures/plots/skrin2.jpeg)

### Validacija
Numeričko rešenje (Euler) poklapa se sa analitičkim za konstantan protok.

![Validacija](figures/plots/skrin3.jpeg)

### Poređenje modela
![Poređenje](figures/plots/skrin4.jpeg)

### Analiza osetljivosti parametara
Uticaj elastičnosti C i perifernog otpora R na krivu pritiska.

![Osetljivost](figures/plots/skrin5.jpeg)

## O modelu

Windkessel model koristi analogiju između krvotoka i električnog kola:

| Fiziološka veličina | Električni analog | Simbol |
|---|---|---|
| Elastičnost arterija | Kondenzator | C |
| Periferni otpor | Otpornik | R |
| Karakteristična impedansa aorte | Serijski otpornik | R1 |
| Ulazni protok iz srca | Izvor struje | Qin(t) |

Osnovna jednačina (dvoelementni model):

$$C \frac{dP}{dt} + \frac{P}{R} = Q_{in}(t)$$

## Sadržaj

- `doc/` — seminarski rad (LaTeX izvor i PDF)
- `notebook/` — Jupyter notebook sa svim simulacijama
- `figures/` — slike korišćene u radu

## Pokretanje

    pip install numpy matplotlib jupyter
    jupyter notebook notebook/windkessel_simulacije.ipynb

## Kompajliranje rada

    cd doc
    pdflatex windkessel.tex
    pdflatex windkessel.tex

## Autor

Zorana Savanović — Prirodno-matematički fakultet, Univerzitet u Novom Sadu