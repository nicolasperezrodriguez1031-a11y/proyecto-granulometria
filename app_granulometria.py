import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Análisis Granulométrico", layout="wide")

st.title("Análisis Granulométrico")

# Diccionario estándar de mallas (ASTM/Tyler) en micrones
MALLAS_STD = {
    "6": 3350.0, "10": 2000.0, "12": 1700.0, "14": 1400.0,
    "18": 1000.0, "20": 850.0, "30": 600.0, "40": 425.0,
    "50": 300.0, "70": 212.0, "100": 150.0, "140": 106.0,
    "200": 75.0, "270": 53.0, "Fondo": 0.0
}

# Inicializar datos por defecto
if 'df_gran' not in st.session_state:
    st.session_state.df_gran = pd.DataFrame({
        "Malla": ["6", "10", "12", "14", "18", "30", "Fondo"],
        "Peso tamiz [g]": [387.7, 378.2, 365.3, 328.0, 303.1, 291.3, 296.4],
        "Peso tamiz + mineral [g]": [387.7, 378.4, 365.3, 328.1, 303.3, 308.5, 296.4]
    })

st.write("### 1. Ingreso de Datos")
st.info("Puedes agregar, borrar o modificar filas haciendo doble clic en las celdas. Presiona el botón de 'Basurero' o '+' a la derecha de la tabla.")

# Tabla editable con formato estricto de 2 decimales para sus columnas
df_editado = st.data_editor(
    st.session_state.df_gran, 
    num_rows="dynamic", 
    use_container_width=True,
    column_config={
        "Peso tamiz [g]": st.column_config.NumberColumn(format="%.2f"),
        "Peso tamiz + mineral [g]": st.column_config.NumberColumn(format="%.2f")
    }
)

# Cálculos Automáticos
if not df_editado.empty:
    try:
        # Asignar abertura
        df_editado['Abertura [µm]'] = df_editado['Malla'].map(MALLAS_STD)
        
        # Calcular pesos
        df_editado['Peso mineral [g]'] = df_editado['Peso tamiz + mineral [g]'] - df_editado['Peso tamiz [g]']
        df_editado['Peso mineral [g]'] = df_editado['Peso mineral [g]'].clip(lower=0)
        
        peso_total = df_editado['Peso mineral [g]'].sum()
        
        if peso_total > 0:
            df_editado['Retenido parcial [%]'] = (df_editado['Peso mineral [g]'] / peso_total) * 100
            df_editado['Retenido acumulado [%]'] = df_editado['Retenido parcial [%]'].cumsum()
            df_editado['Pasante acumulado [%]'] = 100 - df_editado['Retenido acumulado [%]']
            
            st.write("### 2. Tabla Granulométrica Calculada")
            
            # Seleccionamos todas las columnas que tengan números
            columnas_numericas = df_editado.select_dtypes(include='number').columns
            # Le aplicamos un "estilo visual" que obliga a mostrar siempre formato ".00"
            tabla_formateada = df_editado.style.format(subset=columnas_numericas, formatter="{:.2f}")
            
            st.dataframe(tabla_formateada, use_container_width=True)

            # Cálculo del T80 y Gráfico
            df_calc = df_editado[df_editado['Malla'] != 'Fondo'].dropna(subset=['Abertura [µm]', 'Pasante acumulado [%]'])
            
            if not df_calc.empty:
                df_calc = df_calc.sort_values(by='Abertura [µm]', ascending=True)
                
                # Interpolar T80
                t80 = np.interp(80.0, df_calc['Pasante acumulado [%]'], df_calc['Abertura [µm]'])
                
                st.write("### 3. Resultados y Gráfico")
                st.success(f"**El $T_{{80}}$ estimado es: {t80:.2f} µm**")
                
                # Gráfico
                fig = px.line(df_calc, x='Abertura [µm]', y='Pasante acumulado [%]', 
                              log_x=True, markers=True, 
                              title="Curva Granulométrica")
                fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="80% Pasante")
                fig.add_vline(x=t80, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error en los cálculos. Asegúrate de ingresar mallas válidas. Detalle: {e}")

# --- NUEVA SECCIÓN: CONEXIÓN CON POWER BI ---
st.write("### 4. Exportar a Power BI")
st.info("Guarda los datos actuales para que Power BI pueda leerlos y graficarlos.")

if st.button("💾 Actualizar datos para Power BI"):
    df_editado.to_csv("datos_granulometria.csv", index=False, decimal=",", sep=";")
    st.success("¡Datos guardados exitosamente como 'datos_granulometria.csv'!")
# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #a6a8ab;'>Creado por grupo DiRoPS</p>", unsafe_allow_html=True)
