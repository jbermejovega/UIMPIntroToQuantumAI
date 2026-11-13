# Introduction to Quantum Artificial Intelligence

**Jara Juana Bermejo Vega**

[2026] JJBV. Todos los derechos reservados.
Uso para estudiantes y autoaprendizaje: Se autoriza la consulta, descarga y ejecución de estos materiales exclusivamente para el estudio personal y el aprendizaje individual. Uso docente e institucional: Queda prohibida la reproducción, distribución, comunicación pública, proyección sistemática en aula o incorporación sustancial de estos materiales (textos, figuras, presentaciones o notebooks) en asignaturas, cursos o programas impartidos por terceros sin licencia o autorización expresa por escrito del autor, fuera de los límites legales del derecho de cita. Contacto para licencias docentes: [jbermejovega@go.ugr.es].

## Tutorials · 2026–2027

The student-facing practical notebooks are in **[`tutorials/TUTORIAL_2026_2027/`](tutorials/TUTORIAL_2026_2027/)**.

- **[Quimb: DMRG, matrix product states and transverse-field Ising](tutorials/TUTORIAL_2026_2027/Quimb_DMRG_MPS_TFIM.ipynb)**
- **[Variational Quantum Eigensolver: transverse-field Ising](tutorials/TUTORIAL_2026_2027/VQE_TFIM.ipynb)**

The notebook cells contain the scientific implementations, figures and numerical results. Read their explanations and imports before running them. Hardware requirements depend on the experiment; GPU acceleration is optional and must be checked for the installed backend.

## Run locally

```bash
git clone https://github.com/jbermejovega/Quantum-AI-for-Queens.git
cd Quantum-AI-for-Queens
python -m pip install jupyterlab
jupyter lab tutorials/TUTORIAL_2026_2027
```

Use a dedicated Python environment and install the scientific packages needed by the chosen notebook. The command above starts JupyterLab; **it does not certify that the scientific dependencies are installed or all notebook cells have been executed successfully**.

Record your Python version, CPU/GPU, operating system, installed packages, parameters, elapsed time, figures and errors when reporting results.

## References for the practical

- [Recursive QAOA · arXiv:2211.15832v2](tutorials/TUTORIAL_2026_2027/bibliography/2211.15832v2.pdf)
- [Renormalization group and Monte Carlo · arXiv:2401.04811v1](tutorials/TUTORIAL_2026_2027/bibliography/2401.04811v1.pdf)
- [Modified recursive QAOA · arXiv:2408.13207v2](tutorials/TUTORIAL_2026_2027/bibliography/2408.13207v2.pdf)
- [Ising model notes](tutorials/TUTORIAL_2026_2027/notes_ising.pdf)

## Other course tutorials

[Browse the tutorial index](tutorials/README.md) for the existing Ising, HHL and quantum data-fitting examples. Their authorship and existing licence notices remain applicable.
