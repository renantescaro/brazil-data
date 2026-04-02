import joblib
import pandas as pd
from main.helpers.enums import GenderEnum, EducationEnum, UFEnum


class SalaryPredictor:
    def __init__(self):
        self.model = joblib.load("data/ia_models/salary_model.pkl")
        self.uf_labels = joblib.load("data/ia_models/uf_labels.pkl").tolist()

    def predict(self, uf_sigla, cbo, idade, sexo, escolaridade):
        print(f"UFs conhecidas pela IA: {self.uf_labels}")

        # Converte a sigla da UF no índice numérico correspondente
        uf_index = self.uf_labels.index(uf_sigla)

        # Cria o DataFrame com as mesmas colunas do treino
        input_data = pd.DataFrame(
            [[uf_index, int(cbo), int(idade), int(sexo), int(escolaridade)]],
            columns=["sigla_uf", "cbo_2002", "idade", "sexo", "escolaridade"],
        )

        prediction = self.model.predict(input_data)
        return prediction[0]


predictor = SalaryPredictor()

# Exemplo: Senior Software Developer em Santa Catarina
estimated_salary = predictor.predict(
    uf_sigla=UFEnum.SC.value,
    cbo=212405,
    idade=32,
    sexo=GenderEnum.MALE.value,
    escolaridade=EducationEnum.COLLEGE_GRADUATED.value,
)
print(f"Predicted Salary for {UFEnum.SC.name}: R$ {estimated_salary:.2f}")

# Exemplo: Doctorate Researcher em São Paulo
researcher_salary = predictor.predict(
    uf_sigla=UFEnum.SP.value,
    cbo=203105,  # Pesquisador em ciências naturais
    idade=40,
    sexo=GenderEnum.FEMALE.value,
    escolaridade=EducationEnum.DOCTORATE_DEGREE.value,
)
print(f"Predicted Salary for {UFEnum.SC.name}: R$ {researcher_salary:.2f}")
