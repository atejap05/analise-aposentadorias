import pandas as pd


class Abono:
    def __init__(self, file_path):
        self.file_path = file_path
        self.abono_df = None

    def load_data(self):
        self.abono_df = pd.read_csv(self.file_path, sep=";", encoding='latin1')

    def get_anos(self):
        return self.abono_df["Ano"].unique()

    def get_meses(self, ano):
        return self.abono_df.loc[self.abono_df["Ano"] == ano, "Mes"].unique()

    def qtd_servidores_abono_permanencia_por_ano_mes(self, ano: str, mes: str) -> int:
        return self.abono_df.loc[(self.abono_df['Ano'] == ano) & (self.abono_df['Mes'] == mes)].shape[0]

    def qtd_servidores_abono_permanencia_por_uf_residencia(self):
        return self.abono_df.groupby("UF Residência").size()

    def qtd_servidores_abono_permanencia_por_situacao_servidor(self):
        return self.abono_df.groupby("Situação servidor").size()

    def qtd_servidores_abono_permanencia_por_uf_upag_vinculacao(self):
        return self.abono_df.groupby("UF da UPAG de vinculação").size()

    def qtd_servidores_abono_permanencia_por_denominacao_unidade_organizacional(self):
        return self.abono_df.groupby("Denominação unidade").size()

    def qtd_servidores_abono_permanencia_por_cidade_residencia(self):
        return self.abono_df.groupby("Cidade residência").size()
