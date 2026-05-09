# 🔊 Sonido Digital — Intelligence Dashboard

**Autor:** Byron Barrientos Pérez  
**Stack:** Python · Streamlit · Plotly · Anthropic Claude API  
**Contexto:** Proyecto de portafolio desarrollado para demostrar capacidades de analítica de datos e IA aplicada a un negocio real de distribución de audio profesional en Guatemala.

---

## 🎯 Problema de Negocio

Sonido Digital Guatemala distribuye marcas premium de car audio (Memphis, Rockford Fosgate, JBL, Pioneer, entre otras). Como empresa en crecimiento, enfrenta desafíos típicos de retail especializado:

- **Stockouts** de productos de alta rotación que generan pérdida de ventas
- **Sobrestock** en categorías de menor demanda que inmoviliza capital
- **Decisiones reactivas** en lugar de basadas en datos
- **Sin visibilidad unificada** de KPIs de ventas, inventario y canales

Este dashboard transforma datos operativos en decisiones estratégicas y tácticas.

---

## 🧩 Módulos del Sistema

### 📊 Módulo 1 — KPIs & Ventas
- Ingresos, ganancia bruta y margen en tiempo real
- Tendencia mensual por categoría y marca
- Top productos por ingreso
- Análisis de consultas por canal y tasa de conversión

### 📦 Módulo 2 — Gestión de Inventario
- Alertas automáticas de stock crítico y bajo
- Visualización de estado de inventario por SKU
- Valor de inventario por marca
- Tabla de control operativo completa

### 📈 Módulo 3 — Pronóstico de Demanda
- Pronóstico de 90 días por categoría con bandas de confianza
- Basado en media móvil ponderada + ajuste estacional
- Comparativa estacional histórica por categoría

### 🤖 Módulo 4 — Asistente IA
- Chat en lenguaje natural sobre datos del negocio
- Alimentado con contexto de datos reales en cada consulta
- Arquitectura RAG simplificada (contexto estructurado + LLM)
- Recomendaciones accionables orientadas a decisiones

---

## 🚀 Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/sonido-digital-dashboard.git
cd sonido-digital-dashboard

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar API key de Anthropic (para el asistente IA)
export ANTHROPIC_API_KEY="tu-api-key-aquí"

# 4. Generar datos sintéticos
python data/generate_data.py

# 5. Ejecutar el dashboard
streamlit run app.py
```

---

## 🔄 Usar con Datos Reales

Para conectar datos reales de Sonido Digital, reemplaza los archivos CSV en `/data/` con exportaciones de tu sistema actual. El esquema esperado está documentado en `data/generate_data.py`.

Columnas requeridas:
- `sales.csv`: `date, product_id, brand, category, quantity, revenue_gtq, profit_gtq`
- `inventory.csv`: `product_id, current_stock, reorder_point, max_stock, last_restock, status`
- `products.csv`: `product_id, product_name, brand, category, cost_gtq, price_gtq`

---

## 🏗️ Arquitectura

```
sonido_digital/
├── app.py                  # Dashboard principal (Streamlit)
├── requirements.txt
├── data/
│   ├── generate_data.py    # Generador de datos sintéticos
│   ├── products.csv
│   ├── inventory.csv
│   ├── sales.csv
│   └── inquiries.csv
└── README.md
```

---

## 📌 Relevancia para ImProgress

Este proyecto demuestra aplicación directa de los servicios de ImProgress:

| Módulo del Dashboard | Servicio ImProgress |
|---|---|
| KPIs & Ventas | Digital Data Transformation |
| Inventario & Alertas | Smart Flow |
| Pronóstico de Demanda | Stream Sales |
| Asistente IA (RAG) | IA aplicada — metodología Simbiotika |

---

## 👤 Autor

**Byron Barrientos Pérez** — Ingeniero Electrónico, Summa Cum Laude  
Universidad del Valle de Guatemala  
[linkedin.com/in/byron-barrientos-07a17b286](https://www.linkedin.com/in/byron-barrientos-07a17b286)
