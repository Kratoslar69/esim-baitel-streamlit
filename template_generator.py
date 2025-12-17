import pandas as pd
import io

def generate_template():
    """Genera una plantilla Excel con el formato correcto para importar eSIMs"""
    
    # Datos de ejemplo
    data = {
        'iccid': ['8952140063883316310F', '8952140063883316302F'],
        'msisdn': ['2219592008', '2219592007'],
        'imsi': ['334140224894044', '334140224894036'],
        'pin': ['1234', '1234'],
        'puk': ['50863044', '50863036'],
        'serie': ['9271', '9270'],
        'asignado_a': ['', ''],  # Vacío por defecto
        'distribuidor': ['BAITEL', 'BAITEL'],
        'ip': ['CB127', 'CB127'],
        'producto': ['MOV', 'MOV'],
        'estado': ['Disponible', 'Disponible'],
        'fecha_creacion': ['2024-01-01', '2024-01-01'],
        'fecha_ultimo_cambio': ['2024-01-01', '2024-01-01']
    }
    
    df = pd.DataFrame(data)
    
    # Crear archivo Excel en memoria
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='eSIM Template')
        
        # Obtener el workbook y worksheet
        workbook = writer.book
        worksheet = writer.sheets['eSIM Template']
        
        # Ajustar ancho de columnas
        for column in worksheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
    
    output.seek(0)
    return output

def validate_import_data(df):
    """Valida que los datos importados tengan el formato correcto"""
    
    required_columns = ['iccid', 'msisdn', 'imsi', 'pin', 'puk', 'serie', 'producto', 'estado']
    
    # Verificar columnas requeridas
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"❌ Faltan columnas requeridas: {', '.join(missing_columns)}"
    
    # Verificar que no haya ICCIDs duplicados
    if df['iccid'].duplicated().any():
        return False, "❌ Hay ICCIDs duplicados en el archivo"
    
    # Verificar que los estados sean válidos
    valid_estados = ['Disponible', 'Usado']
    invalid_estados = df[~df['estado'].isin(valid_estados)]
    if not invalid_estados.empty:
        return False, f"❌ Estados inválidos encontrados. Solo se permiten: {', '.join(valid_estados)}"
    
    return True, "✅ Datos válidos"
