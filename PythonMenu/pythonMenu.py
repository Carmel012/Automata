import pandas as pd

# Ruta del archivo CSV original
file_path = '/Users/carmelorodriguezchab/Downloads/automata.csv'

# Función para cargar el archivo CSV y construir el DFA
def cargar_dfa(file_path):
    try:
        # Cargar el archivo CSV
        df = pd.read_csv(file_path).drop(columns=['Unnamed: 4'], errors='ignore')
        print("Archivo cargado correctamente.\n")
        print("Contenido del archivo cargado:")
        print(df.head())  # Mostrar las primeras filas del archivo CSV cargado
    except FileNotFoundError:
        print(f"Archivo no encontrado en la ruta: {file_path}")
        return None, None, None
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None, None, None

    # Procesar el archivo CSV para definir el DFA
    dfa = {}
    initial_state = None
    final_states = set()

    for _, row in df.iterrows():
        state = row['Entidades']
        
        # Determinar el estado inicial y final
        if row['Unnamed: 0'] == 'Inicio':
            initial_state = state
        if row['Unnamed: 0'] == 'Final':
            final_states.add(state)
        
        # Agregar las transiciones para los símbolos 0 y 1
        dfa[state] = {0: row.iloc[2], 1: row.iloc[3]}
    
    return dfa, initial_state, final_states, df

# Función para verificar una cadena en el DFA
def verificar_cadena(dfa, initial_state, final_states, cadena):
    current_state = initial_state
    for simbolo in cadena:
        simbolo = int(simbolo)
        if simbolo not in dfa[current_state]:
            return False
        current_state = dfa[current_state][simbolo]
    return current_state in final_states

# Función para mostrar el menú y ejecutar la opción seleccionada
def menu():
    global file_path  # Hacer que file_path sea global para poder modificarla desde el menú
    dfa, initial_state, final_states, df = cargar_dfa(file_path)
    if dfa is None:
        return

    while True:
        print("\n--- Menú ---")
        print("1. Verificar una cadena")
        print("2. Modificar el autómata (archivo CSV)")
        print("3. Salir")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == '1':
            cadena = input("Introduce la cadena de 0s y 1s a verificar: ")
            es_valida = verificar_cadena(dfa, initial_state, final_states, cadena)
            print(f"La cadena '{cadena}' es {'válida' if es_valida else 'inválida'}.")
        
        elif opcion == '2':
            print("\n--- Modificar el autómata ---")
            print("1. Agregar nueva transición")
            print("2. Agregar nuevo estado final")
            print("3. Salir")
            
            sub_opcion = input("Selecciona una opción: ")

            if sub_opcion == '1':
                # Agregar nueva transición
                estado_origen = input("Introduce el estado de origen: ")
                simbolo = input("Introduce el símbolo (0 o 1): ")
                estado_destino = input("Introduce el estado de destino: ")

                # Actualizar el DataFrame y el DFA
                if estado_origen in df['Entidades'].values:
                    df.loc[df['Entidades'] == estado_origen, simbolo] = estado_destino
                    print(f"Transición agregada: {estado_origen} -> {simbolo} -> {estado_destino}")
                else:
                    print("El estado de origen no existe en el autómata.")

            elif sub_opcion == '2':
                # Agregar nuevo estado final
                nuevo_estado = input("Introduce el nuevo estado final: ")
                if nuevo_estado not in final_states:
                    final_states.add(nuevo_estado)
                    print(f"Nuevo estado final agregado: {nuevo_estado}")
                else:
                    print("Este estado ya es final.")

            elif sub_opcion == '3':
                print("Volviendo al menú principal.")
                continue
            
            # Guardar el archivo modificado
            df.to_csv(file_path, index=False)
            print(f"Archivo actualizado guardado en: {file_path}")

            # Recargar el DFA con los cambios realizados
            dfa, initial_state, final_states, df = cargar_dfa(file_path)
        
        elif opcion == '3':
            print("Saliendo del programa.")
            break
        
        else:
            print("Opción no válida. Por favor, elige una opción del menú.")

# Ejecutar el menú
if __name__ == '__main__':
    menu()
