from flask import Blueprint, render_template, request, jsonify
from main.helpers.mappings import MAP_INSTRUCAO, MAP_SEXO, MAP_TAMANHO
from main.database.database import client

bp = Blueprint(
    "pages",
    __name__,
    url_prefix="/",
    template_folder="templates",
)


class PagesCtrl:
    @staticmethod
    @bp.route("/", methods=["GET"])
    def search_index():
        return render_template("search.html")

    @bp.route("/api/cargos")
    def api_jobs():
        query = (
            "SELECT trim(cbo_2002), trim(descricao) FROM cbo_nomes ORDER BY descricao"
        )
        result = client.query(query)

        jobs = []
        for row in result.result_rows:
            jobs.append({"codigo": row[0], "nome": row[1]})

        return jsonify(jobs)

    @bp.route("/buscar", methods=["POST"])
    def search_request():
        cbo = request.form.get("cbo_codigo")
        name = request.form.get("cbo_nome")

        query = f"""
            SELECT 
                sexo, sigla_uf,
                grau_instrucao_apos_2005 as instrucao,
                tamanho_estabelecimento as tamanho,
                ROUND(AVG(valor_remuneracao_media), 2) as media,
                MIN(valor_remuneracao_media) as minimo,
                MAX(valor_remuneracao_media) as maximo,
                COUNT(*) as total
            FROM rais_vinculos 
            WHERE cbo_2002 = '{cbo}'
            AND valor_remuneracao_media > 400 
            GROUP BY sexo, sigla_uf, instrucao, tamanho
            ORDER BY total DESC
            LIMIT 50
        """

        result = client.query(query)

        formatted_data = []
        for row in result.result_rows:
            formatted_data.append(
                {
                    "sexo": MAP_SEXO.get(str(row[0]), "Outro"),
                    "uf": row[1],
                    "escolaridade": MAP_INSTRUCAO.get(str(row[2]), "Outros"),
                    "empresa": MAP_TAMANHO.get(str(row[3]), "Não informado"),
                    "media": row[4],
                    "minimo": row[5],
                    "maximo": row[6],
                    "vagas": row[7],
                }
            )

        return render_template(
            "results.html",
            cbo=cbo,
            name=name,
            data=formatted_data,
        )

    @bp.route("/profissoes-topo")
    def higher_salaries():
        query = """
            SELECT 
                T2.descricao AS cargo,
                ROUND(AVG(T1.valor_remuneracao_media), 2) AS media_salarial,
                COUNT(*) AS total_vagas,
                MAX(T1.valor_remuneracao_media) AS teto_salarial
            FROM rais_vinculos AS T1
            LEFT JOIN cbo_nomes AS T2 ON T1.cbo_2002 = T2.cbo_2002
            GROUP BY cargo
            HAVING total_vagas > 5
            ORDER BY media_salarial DESC
            LIMIT 50
        """

        result = client.query(query)

        dados_topo = []
        for row in result.result_rows:
            dados_topo.append(
                {
                    "cargo": row[0] or "Cargo não identificado",
                    "media": row[1],
                    "vagas": row[2],
                    "teto": row[3],
                }
            )

        return render_template("higher_salaries.html", dados=dados_topo)

    @bp.route("/quantidade-profissionais")
    def larger_number_workers():
        query = """
            SELECT 
                T2.descricao AS cargo,
                COUNT(*) AS total_funcionarios,
                ROUND(AVG(T1.valor_remuneracao_media), 2) AS media_salarial,
                sigla_uf
            FROM rais_vinculos AS T1
            LEFT JOIN cbo_nomes AS T2 ON T1.cbo_2002 = T2.cbo_2002
            GROUP BY cargo, sigla_uf
            ORDER BY total_funcionarios DESC
            LIMIT 50
        """

        result = client.query(query)

        date = []
        for row in result.result_rows:
            date.append(
                {
                    "cargo": row[0] or "Cargo não identificado",
                    "total_funcionarios": row[1],
                    "media_salarial": row[2],
                    "sigla_uf": row[3],
                }
            )

        return render_template(
            "larger_number_workers.html",
            date=date,
        )

    @bp.route("/mapa-salarial")
    def by_state():
        query = """
            SELECT 
                sigla_uf,
                ROUND(AVG(valor_remuneracao_media), 2) AS media_estado,
                COUNT(*) AS total_vinculos
            FROM rais_vinculos
            WHERE valor_remuneracao_media > 200 
            AND valor_remuneracao_media < 250000
            AND idade BETWEEN 14 AND 100
            GROUP BY sigla_uf
        """
        result = client.query(query)

        data_map = {}
        for row in result.result_rows:
            data_map[row[0]] = {
                "media": row[1],
                "vagas": row[2],
            }

        return render_template(
            "by_state.html",
            data_map=data_map,
        )
