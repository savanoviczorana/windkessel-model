# Windkessel model — matematičko modelovanje arterijskog pritiska

Seminarski rad iz predmeta *Modeliranje dinamičkih sistema*.
Modelovanje dinamike arterijskog pritiska pomoću dvoelementnog i
troelementnog Windkessel modela, sa numeričkim simulacijama u Pythonu.

## Sadržaj

- `doc/` — seminarski rad (LaTeX izvor i PDF)
- `notebook/` — Jupyter notebook sa svim simulacijama
- `figures/` — slike korišćene u radu

## Modeli

- **Dvoelementni (RC):** periferni otpor R i arterijska elastičnost C
- **Troelementni:** dodaje karakterističnu impedansu R1 u seriji sa RC granom

## Pokretanje simulacija

Notebook sadrži sve simulacije (oba modela, validaciju, poređenje i analizu osetljivosti).

```bash
pip install numpy matplotlib jupyter
jupyter notebook notebook/windkessel_simulacije.ipynb
```

## Kompajliranje rada

```bash
cd doc
pdflatex windkessel.tex
pdflatex windkessel.tex
```

## Autor

Zorana Savanović
