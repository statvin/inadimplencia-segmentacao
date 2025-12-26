import pandas as pd
import os

def load_raw_data(filepath):
    """
    Carrega o dataset UCI Credit Card Default.
    Estratégia: Prioriza leitura como Excel Real (.xls), com fallback para CSV.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

    print(f"Tentando carregar: {filepath}")

    # Tenta ler como EXCEL primeiro (devido ao erro 0xd0)
    try:
        # header=1 é essencial para pular a linha 'X1, X2...'
        df = pd.read_excel(filepath, header=1)
        print("✅ Arquivo detectado como Excel (.xls) e carregado com sucesso.")
    except Exception as e_excel:
        print(f"⚠️ Falha ao ler como Excel: {e_excel}")
        print("Tentando ler como CSV/Texto...")
        
        try:
            # Se falhar, tenta CSV (pode ser separador ; ou ,)
            df = pd.read_csv(filepath, header=1, encoding='utf-8')
        except Exception as e_csv:
             # Última tentativa: encoding latin-1 (comum em arquivos antigos)
            try:
                df = pd.read_csv(filepath, header=1, encoding='latin-1')
            except:
                raise ValueError(f"CRÍTICO: Não foi possível ler o arquivo nem como Excel nem como CSV.\nErro Excel: {e_excel}\nErro CSV: {e_csv}")

    # --- LIMPEZA E PADRONIZAÇÃO ---
    
    # Renomeação (Mapeamento de Negócio)
    rename_map = {
        'PAY_0': 'status_pag_set',
        'PAY_2': 'status_pag_ago',
        'PAY_3': 'status_pag_jul',
        'PAY_4': 'status_pag_jun',
        'PAY_5': 'status_pag_mai',
        'PAY_6': 'status_pag_abr',
        'default payment next month': 'is_inadimplente',
        'LIMIT_BAL': 'limite_credito',
        'SEX': 'genero',
        'EDUCATION': 'escolaridade',
        'MARRIAGE': 'estado_civil',
        'AGE': 'idade',
        'BILL_AMT1': 'bill_amt1',
        'PAY_AMT1': 'pay_amt1'
    }
    
    # Normaliza colunas do DF para minúsculo para garantir o match
    df.columns = [str(c).lower() for c in df.columns]
    
    # Cria mapa de renomeação em minúsculo
    rename_map_lower = {k.lower(): v for k, v in rename_map.items()}
    
    df.rename(columns=rename_map_lower, inplace=True)

    # Sanity Check das colunas críticas
    if 'status_pag_set' not in df.columns:
        # Caso o header=1 não tenha funcionado como esperado, tentamos depurar
        print(f"⚠️ AVISO: Colunas encontradas: {df.columns.tolist()[:10]}")
        raise ValueError("A coluna 'PAY_0' (status_pag_set) não foi encontrada. Verifique o parâmetro header.")

    return df

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ajuste o nome do arquivo se necessário. 
    # DICA: Verifique se o nome na pasta é 'credit_card_clients.xls' ou 'default of credit card clients.xls'
    file_name = 'credit_card_clients.xls' 
    file_path = os.path.join(current_dir, '..', 'data', 'raw', file_name)
    
    try:
        df = load_raw_data(file_path)
        print(f"🚀 SUCESSO FINAL! Dataset pronto.")
        print(f"Shape: {df.shape}")
        print(f"Colunas de Pagamento: {[c for c in df.columns if 'status_pag' in c]}")
    except Exception as e:
        print(f"❌ Erro: {e}")