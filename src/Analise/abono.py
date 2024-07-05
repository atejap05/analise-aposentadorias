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

    def qtd_servidores_abono_permanencia_por_ano_mes(self, ano: int, mes: int) -> dict:

        # qtd servidor
        qtd_serv_mes_atual = self.abono_df.loc[(self.abono_df['Ano'] == ano) & (
                self.abono_df['Mes'] == mes)].shape[0]

        # labels
        label_mes_atual = f"Servidores com abono permanência em {str(mes).zfill(2)}/{ano}"

        primeiro_ano, primeiro_mes = self.get_primeiro_ano_mes()
        ultimo_ano, ultimo_mes = self.get_ultimo_ano_mes()

        if ano == primeiro_ano and mes == primeiro_mes:
            qtd_serv_mes_anterior = 0
            label_mes_anterior = "Sem dados"

        else:

            if mes == 1:
                qtd_serv_mes_anterior = self.abono_df.loc[(
                                                                  self.abono_df['Ano'] == ano - 1) & (
                                                                  self.abono_df['Mes'] == 12)].shape[0]

                label_mes_anterior = f"Servidores com abono permanência em 12/{ano - 1}"

            else:
                qtd_serv_mes_anterior = self.abono_df.loc[(self.abono_df['Ano'] == ano) & (
                        self.abono_df['Mes'] == mes - 1)].shape[0]

                label_mes_anterior = (f"Servidores com abono permanência em " +
                                      "{str(mes - 1).zfill(2)}/{ano if mes != 1 else ano - 1}")

        if ano == ultimo_ano and mes == ultimo_mes:
            qtd_serv_proximo_mes = 0
            label_proximo_mes = "Sem dados"

        else:

            if mes == 12:
                qtd_serv_proximo_mes = self.abono_df.loc[(
                                                                 self.abono_df['Ano'] == ano + 1) & (
                                                                 self.abono_df['Mes'] == 1)].shape[0]

                label_proximo_mes = f"Servidores com abono permanência em 01/{ano + 1}"

            else:
                qtd_serv_proximo_mes = self.abono_df.loc[(
                                                                 self.abono_df['Ano'] == ano) & (
                                                                 self.abono_df['Mes'] == mes + 1)].shape[0]

                label_proximo_mes = f"Servidores com abono permanência em {str(mes + 1).zfill(2)}/{ano + 1}"

        return {
                "mes_anterior": {"label": label_mes_anterior, "value": qtd_serv_mes_anterior},
                "mes_atual": {"label": label_mes_atual, "value": qtd_serv_mes_atual},
                "mes_proximo": {"label": label_proximo_mes, "value": qtd_serv_proximo_mes}
                }

    def montante_pago_abono_permanencia(self) -> pd.Series:
        return self.abono_df.groupby("Ano")["Valor"].sum()

    def qtd_servidores_abono_permanencia_por_uf_residencia_por_ano_mes(self, ano: str, mes: str) -> pd.Series:
        return self.abono_df.loc[
            (self.abono_df['Ano'] == ano) & (self.abono_df['Mes'] == mes), "UF Residência"].value_counts()

    @staticmethod
    def rename_descricao_unidade(text):
        text = text.upper().strip()
        mapping = {
            "SRRF/10RF/SUPERINTENDENCIA REG RFB 10A R": "10RF",
            "SRRF/9RF/SUPERINTENDENCIA REG RFB 9A RF": "9RF",
            "SRRF/8RF/SUPERINTENDENCIA REG RFB 8A RF": "8RF",
            "SRRF/7RF/SUPERINTENDENCIA REG RFB 7A RF": "7RF",
            "SRRF/6RF/SUPERINTENDENCIA REG RFB 6A RF": "6RF",
            "SRRF/5RF/SUPERINTENDENCIA REG RFB 5A RF": "5RF",
            "SRRF/4RF/SUPERINTENDENCIA REG RFB 4A RF": "4RF",
            "SRRF/3RF/SUPERINTENDENCIA REG RFB 3A RF": "3RF",
            "SRRF/2RF/SUPERINTENDENCIA REG RFB 2A RF": "2RF",
            "SRRF/1RF/SUPERINTENDENCIA REG RFB 1A RF": "1RF",
            "SEC ESP RECEITA FEDERAL DO BRASIL": "SERFB",
            "COORDENACAO-GERAL DE GESTAO DE PESSOAS": "COGEP"
        }
        return mapping.get(text, text)

    def qtd_servidores_abono_permanencia_por_unidade_por_ano_mes(self, ano: str, mes: str) -> pd.Series:
        qtd_serv_por_unidade = self.abono_df.loc[(self.abono_df['Ano'] == ano) & (
                self.abono_df['Mes'] == mes), "Denominação unidade"].value_counts()
        qtd_serv_por_unidade.rename(
            self.rename_descricao_unidade, inplace=True)
        return qtd_serv_por_unidade

    def get_df_servidor(self, servidor, cpf) -> pd.DataFrame:

        cpf = str(cpf).replace(".", "").replace("-", "")
        cpf = cpf[3:9]

        # find all rows with the same cpf and name
        return self.abono_df[
            self.abono_df["Nome"].astype(str).str.contains(servidor, case=False) &
            self.abono_df["CPF"].astype(str).str.contains(cpf, case=False)
            ]

    def montante_pago_abono_permanencia_por_servidor_ano_ano(self, servidor, cpf) -> pd.Series:

        df_servidor = self.get_df_servidor(servidor, cpf)
        return df_servidor.groupby("Ano")["Valor"].sum()
