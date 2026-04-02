import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from main.database.database import client


class PredictorOfFairSalarySv:
    def __init__(self):
        pass

    def execute(self):
        data = self._get_data()
        print("after _get_data")

        # Tratamento do CBO
        # if "cbo_2002" in data.columns:
        #     data["cbo_2002"] = pd.to_numeric(
        #         data["cbo_2002"].str.decode("utf-8").str.strip(), errors="coerce"
        #     )

        # Tratamento da UF
        if "sigla_uf" in data.columns:
            data["sigla_uf"], labels = pd.factorize(data["sigla_uf"])
            # Salva o mapeamento para usar na inferência depois
            self._export(labels, "uf_labels.pkl")

        # Garante que todas as colunas object sejam tratadas
        for col in data.columns:
            if data[col].dtype == object:
                data[col] = pd.to_numeric(data[col], errors="coerce")

        # Remove os registros NaN e nulos
        data = data.dropna()

        # Separar X (entrada) e y (o que queremos prever)
        X = data.drop("valor_remuneracao_media", axis=1)
        y = data["valor_remuneracao_media"]

        # Dividir 80% para treino e 20% para teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Criar e treinar a IA
        model = RandomForestRegressor(
            n_estimators=150,
            random_state=42,
            n_jobs=-1,
        )
        model.fit(X_train, y_train)

        # Validar a precisão
        predictions = model.predict(X_test)
        error = mean_absolute_error(y_test, predictions)

        self._export(model, "salary_model.pkl")

        print(f"Erro médio da IA: R$ {error:.2f}")

    def _export(self, model, name: str):
        joblib.dump(model, f"data/ia_models/{name}")

    def _get_data(self):
        query = """
            SELECT
                sigla_uf,
                toUInt32OrZero(cbo_2002) AS cbo_2002,
                toUInt8(idade) AS idade,
                toUInt8(sexo) AS sexo,
                toUInt8(grau_instrucao_apos_2005) AS escolaridade,
                valor_remuneracao_media
            FROM rais_vinculos
            WHERE valor_remuneracao_media > 1320
            AND valor_remuneracao_media < 50000
            AND toUInt32OrZero(cbo_2002) != 0
            ORDER BY rand()
            LIMIT 100000000
        """
        return client.query_df(query)
