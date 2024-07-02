import pandas as pd


class Abono:
    def __init__(self, file_path):
        self.file_path = file_path
        self.abono_df = None

    def load_data(self) -> None:
        self.abono_df = pd.read_csv(self.file_path, sep=";", encoding='latin1')

    def get_anos(self) -> pd.Series:
        return self.abono_df["Ano"].unique()

    def get_meses(self, ano: str) -> pd.Series:
        return self.abono_df.loc[self.abono_df["Ano"] == ano, "Mes"].unique()

    def get_primeiro_ano_mes(self):
        ano_min = self.abono_df["Ano"].min()
        mes_min = self.abono_df.loc[self.abono_df["Ano"]
                                    == ano_min, "Mes"].min()
        return ano_min, mes_min

    def get_ultimo_ano_mes(self):
        ano_max = self.abono_df["Ano"].max()
        mes_max = self.abono_df.loc[self.abono_df["Ano"]
                                    == ano_max, "Mes"].max()
        return ano_max, mes_max

    def qtd_servidores_abono_permanencia_por_ano_mes(self, ano: str, mes: str) -> dict:

        # qtd servidor
        qtd_serv_mes_atual = self.abono_df.loc[(self.abono_df['Ano'] == ano) & (
            self.abono_df['Mes'] == mes)].shape[0]
        qtd_serv_mes_anterior = None
        qtd_serv_proximo_mes = None

        # labels
        label_mes_atual = f"Servidores com abono permanência em {str(mes).zfill(2)}/{ano}"
        label_mes_anterior = None
        label_proximo_mes = None

        primeiro_ano, primeiro_mes = self.get_primeiro_ano_mes()
        ultimo_ano, ultimo_mes = self.get_ultimo_ano_mes()

        if ano == primeiro_ano and mes == primeiro_mes:
            qtd_serv_mes_anterior = 0
            label_mes_anterior = "Sem dados"

        else:

            if mes == 1:
                qtd_serv_mes_anterior = self.abono_df.loc[(
                    self.abono_df['Ano'] == ano - 1) & (self.abono_df['Mes'] == 12)].shape[0]

                label_mes_anterior = f"Servidores com abono permanência em 12/{ano - 1}"

            else:
                qtd_serv_mes_anterior = self.abono_df.loc[(self.abono_df['Ano'] == ano) & (
                    self.abono_df['Mes'] == mes - 1)].shape[0]

                label_mes_anterior = f"Servidores com abono permanência em {str(mes - 1).zfill(2)}/{ano if mes != 1 else ano - 1}"

        if ano == ultimo_ano and mes == ultimo_mes:
            qtd_serv_proximo_mes = 0
            label_proximo_mes = "Sem dados"

        else:

            if mes == 12:
                qtd_serv_proximo_mes = self.abono_df.loc[(
                    self.abono_df['Ano'] == ano + 1) & (self.abono_df['Mes'] == 1)].shape[0]

                label_proximo_mes = f"Servidores com abono permanência em 01/{ano + 1}"

            else:
                qtd_serv_proximo_mes = self.abono_df.loc[(
                    self.abono_df['Ano'] == ano) & (self.abono_df['Mes'] == mes + 1)].shape[0]

                label_proximo_mes = f"Servidores com abono permanência em {str(mes + 1).zfill(2)}/{ano + 1 }"

        return {"mes_anterior":
                {
                    "label": label_mes_anterior,
                    "value": qtd_serv_mes_anterior
                },
                "mes_atual":
                {
                    "label": label_mes_atual,
                    "value": qtd_serv_mes_atual
                },
                "mes_proximo":
                {
                    "label": label_proximo_mes,
                    "value": qtd_serv_proximo_mes
                }
                }

    def qtd_servidores_abono_permanencia_por_uf_residencia(self) -> int:
        return self.abono_df.groupby("UF Residência").size()

    def qtd_servidores_abono_permanencia_por_situacao_servidor(self) -> int:
        return self.abono_df.groupby("Situação servidor").size()

    def qtd_servidores_abono_permanencia_por_uf_upag_vinculacao(self) -> pd.Series:
        return self.abono_df.groupby("UF da UPAG de vinculação").size()

    def qtd_servidores_abono_permanencia_por_denominacao_unidade_organizacional(self) -> pd.Series:
        return self.abono_df.groupby("Denominação unidade").size()

    def qtd_servidores_abono_permanencia_por_cidade_residencia(self):
        return self.abono_df.groupby("Cidade residência").size()
