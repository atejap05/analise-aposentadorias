import pandas as pd


class Abono():
    def __init__(self, file_path):
        self.file_path = file_path
        self.abono_df = None

    def load_data(self):
        self.abono_df = pd.read_excel(
            self.file_path, sheet_name="052024", header=0)

    def qtd_servidores_abono_permanencia(self):
        return self.abono_df.shape[0]

    def qtd_servidores_abono_permanencia_por_uf_residencia(self):
        return self.abono_df.groupby("UF da Residência").size()

    def qtd_servidores_abono_permanencia_por_nivel_escolaridade(self):
        return self.abono_df.groupby("Nível de Escolaridade").size()

    def qtd_servidores_abono_permanencia_por_situacao_servidor(self):
        return self.abono_df.groupby("Situação servidor").size()

    def qtd_servidores_abono_permanencia_por_uf_upag_vinculacao(self):
        return self.abono_df.groupby("UF da UPAG de vinculação").size()

    def qtd_servidores_abono_permanencia_por_denominacao_unidade_organizacional(self):
        return self.abono_df.groupby("Denominação unidade organizacional").size()

    def qtd_servidores_abono_permanencia_por_cidade_residencia(self):
        return self.abono_df.groupby("Cidade da residência").size()
