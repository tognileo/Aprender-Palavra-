"""
Importa as expressões do CSV para o banco.

Pode ser executado várias vezes: o que já existe é pulado, só o que é novo entra.
Como rodar (na raiz do projeto, com o (venv) ativo):
    python -m banco.importar_expressoes
(ou o botão Play do VS Code neste arquivo)
"""
import csv
from pathlib import Path

import sys
from pathlib import Path

# Põe a pasta raiz do projeto no caminho do Python. Assim o "from backend..." funciona
# em qualquer jeito de rodar (botão Play do VS Code, de dentro da pasta, ou com -m).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.banco_de_dados import SessionLocal
from backend.modelos import Nicho, Grupo, Expressao

CAMINHO_CSV = Path(__file__).resolve().parent / "expressoes.csv"


def importar(db, caminho_csv=CAMINHO_CSV):
    # 1) Lê o CSV (utf-8-sig remove o BOM do começo do arquivo)
    with open(caminho_csv, encoding="utf-8-sig", newline="") as arquivo:
        linhas = list(csv.DictReader(arquivo))

    # 2) Busca os nichos que já existem no banco, pelo nome
    nichos = {n.nome: n.id for n in db.query(Nicho).all()}

    grupos_criados = 0
    expressoes_novas = 0
    expressoes_puladas = 0

    # Cache: (nicho_id, nome do grupo) -> id do grupo
    grupos_ids = {}
    # Contador da ordem dos grupos de cada nicho (o Básico é sempre 0)
    proxima_ordem = {}

    for linha in linhas:
        nome_nicho = linha["nicho"].strip()
        nome_grupo = linha["grupo"].strip()

        # Básico: nicho vazio no CSV = nicho_id vazio (None) no banco
        if nome_nicho == "":
            nicho_id = None
        else:
            if nome_nicho not in nichos:
                raise RuntimeError(
                    f'O nicho "{nome_nicho}" não existe na tabela nichos. '
                    "Confira o nome no CSV e no banco."
                )
            nicho_id = nichos[nome_nicho]

        # 3) Acha o grupo (ou cria, se ainda não existir)
        chave = (nicho_id, nome_grupo)
        if chave not in grupos_ids:
            filtro = Grupo.nicho_id.is_(None) if nicho_id is None else Grupo.nicho_id == nicho_id
            grupo = db.query(Grupo).filter(filtro, Grupo.nome == nome_grupo).first()
            if grupo is None:
                if nicho_id is None:
                    ordem_grupo = 0
                else:
                    ordem_grupo = proxima_ordem.get(nicho_id)
                    if ordem_grupo is None:
                        # Continua depois da maior ordem que já existe nesse nicho
                        maior = (
                            db.query(Grupo.ordem)
                            .filter(Grupo.nicho_id == nicho_id)
                            .order_by(Grupo.ordem.desc())
                            .first()
                        )
                        ordem_grupo = (maior[0] + 1) if maior else 1
                    proxima_ordem[nicho_id] = ordem_grupo + 1
                grupo = Grupo(nicho_id=nicho_id, nome=nome_grupo, ordem=ordem_grupo)
                db.add(grupo)
                db.flush()  # gera o id do grupo sem finalizar a gravação
                grupos_criados += 1
            grupos_ids[chave] = grupo.id

        grupo_id = grupos_ids[chave]

        # 4) Expressão: se (grupo, inglês) já existe, pula
        ingles = linha["ingles"].strip()
        ja_existe = (
            db.query(Expressao.id)
            .filter(Expressao.grupo_id == grupo_id, Expressao.ingles == ingles)
            .first()
        )
        if ja_existe:
            expressoes_puladas += 1
            continue

        db.add(
            Expressao(
                grupo_id=grupo_id,
                ingles=ingles,
                portugues=linha["portugues"].strip(),
                pronuncia=linha["pronuncia"].strip(),
                ordem=int(linha["ordem"]),
                audio=None,
            )
        )
        expressoes_novas += 1

    return grupos_criados, expressoes_novas, expressoes_puladas


if __name__ == "__main__":
    db = SessionLocal()
    try:
        g, novas, puladas = importar(db)
        db.commit()  # só grava de verdade se não houve erro
        print(f"Grupos criados: {g}")
        print(f"Expressões inseridas: {novas}")
        print(f"Expressões que já existiam (puladas): {puladas}")
    except Exception as erro:
        db.rollback()  # desfaz tudo se algo deu errado
        print("Erro na importação. Nada foi gravado.")
        print(erro)
    finally:
        db.close()