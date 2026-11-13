# PACA DOCENCIA · Codebooks y notas de clase · 13-11-2026

**Quantum AI for Queens** · proyecto docente de Jara Juana Bermejo Vega (JJBV).

Esta edición contiene **cuatro notebooks docentes nuevos** y **cuatro notas de clase asociadas**, con ejecución local de sus celdas Python y verificaciones numéricas. No sustituye los tutoriales históricos ni reproduce los notebooks originales del ZIP docente de PACA.

| Código | Codebook | Lecture note | Control |
|---|---|---|---|
| 01 | [QAOA / MaxCut](codebooks/01_qaoa_maxcut_baseline.ipynb) | [Nota 01](lecture_notes/01_qaoa_maxcut_baseline.md) | Óptimo clásico y normalización |
| 02 | [TFIM 1D](codebooks/02_tfim_exact_reference.ipynb) | [Nota 02](lecture_notes/02_tfim_exact_reference.md) | Límites J=0 y h=0 |
| 03 | [MPS / SVD](codebooks/03_mps_svd_compression.ipynb) | [Nota 03](lecture_notes/03_mps_svd_compression.md) | Error de truncación |
| 04 | [HHL: control clásico](codebooks/04_hhl_classical_control.ipynb) | [Nota 04](lecture_notes/04_hhl_classical_control.md) | Residual y condición |

## Entorno

Python 3, NumPy y Jupyter. No se necesita hardware cuántico. La evaluación de estos notebooks no implica que se hayan ejecutado los notebooks de terceros ni los algoritmos VQE/DMRG/HHL completos.

## CI nativa

```bash
python paca_docencia/codebooks_20261113/check_codebooks_native.py
```

Este ejecutor local verifica exclusivamente los cuatro codebooks nuevos y falla ante celdas con salidas guardadas, dependencias ausentes o errores de ejecución. No depende de GitHub Actions como prueba de admisión.

## Relación con PACA PROYECTO DOCENTE

Los codebooks se corresponden con cuatro proyecciones pedagógicas: QAOA MaxCut; TFIM como referencia VQE/DMRG; redes tensoriales MPS/SVD; y sistemas lineales como control clásico para HHL. La rúbrica común es **código + resultados + traza + interpretación**.

Los nueve notebooks originales del paquete `PACA_PPL_DOCENCIA_INVESTIGA_2026-11-13.zip` permanecen **HOLD_SOURCE_IMPORT / HOLD_RIGHTS_REVIEW**. Tampoco se copian los 44 notebooks de SIGILBOOK ni datos de estudiantes, expedientes, CV o proyectos privados.

## Autoría, derechos y atribuciones

**Dirección editorial del proyecto:** Jara Juana Bermejo Vega (JJBV), SIGILBOOK · PACA DOCENCIA. Material de apoyo nuevo preparado bajo instrucciones autorales y sujeto a revisión editorial. Se reservan los derechos que correspondan a las contribuciones originales de JJBV, sin atribuirle automáticamente obras de terceros.

Los tutoriales HHL históricos del repositorio proceden en parte de Qiskit Textbook y de trabajos de Tyler Benson; conservan sus propias licencias y atribuciones. Este release no altera esos archivos ni aplica una licencia global al futuro libro académico `SIGILBOOK · PACA Lecture Notes & Codebooks`.

La publicación abierta permite consultar el material, pero no constituye por sí sola una licencia adicional de redistribución, traducción o explotación comercial. Los permisos se resuelven por archivo y titularidad.

**PIORNALEGO ES CANON · SOURCE_BOUND.**
