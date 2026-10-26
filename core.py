from collections import defaultdict

estudantes = []


def calcular_media(avaliacoes):
    if not avaliacoes:
        return 0.0
    return sum(avaliacoes) / len(avaliacoes)


def classificar_situacao(media):
    if media >= 7.0:
        return "Aprovado"
    elif media >= 5.0:
        return "Recuperação"
    return "Reprovado"


def calcular_frequencia(aulas_previstas, presencas):
    if aulas_previstas == 0:
        return 0.0
    return (presencas / aulas_previstas) * 100


def buscar_por_matricula(matricula):
    for est in estudantes:
        if est["matricula"] == matricula:
            return est
    return None


def cadastrar_estudante(matricula, nome, turma):
    if buscar_por_matricula(matricula):
        return False

    estudantes.append(
        {
            "matricula": matricula,
            "nome": nome,
            "turma": turma,
            "avaliacoes": [],
            "aulas_previstas": 0,
            "presencas": 0,
        }
    )
    return True


def atualizar_estudante(matricula, novo_nome="", nova_turma=""):
    est = buscar_por_matricula(matricula)
    if not est:
        return False

    if novo_nome:
        est["nome"] = novo_nome
    if nova_turma:
        est["turma"] = nova_turma
    return True


def remover_estudante(matricula):
    est = buscar_por_matricula(matricula)
    if not est:
        return False

    estudantes.remove(est)
    return True


def registrar_avaliacoes(matricula, notas):
    est = buscar_por_matricula(matricula)
    if not est:
        return False

    for nota in notas:
        if 0 <= nota <= 10:
            est["avaliacoes"].append(nota)
    return True


def registrar_frequencia(matricula, aulas, presencas):
    est = buscar_por_matricula(matricula)
    if not est:
        return False

    if aulas < 0 or presencas < 0 or presencas > aulas:
        return False

    est["aulas_previstas"] = aulas
    est["presencas"] = presencas
    return True


def listar_por_nome(nome):
    nome_busca = nome.lower()
    return [est for est in estudantes if nome_busca in est["nome"].lower()]


def listar_por_turma(turma):
    turma_busca = turma.lower()
    return [est for est in estudantes if est["turma"].lower() == turma_busca]


def listar_ordenado_por_media():
    return sorted(estudantes, key=lambda e: calcular_media(e["avaliacoes"]), reverse=True)


def listar_nomes_em_turmas_diferentes():
    nomes_turmas = defaultdict(set)

    for est in estudantes:
        nomes_turmas[est["nome"].lower()].add(est["turma"])

    return [
        {"nome": nome.title(), "turmas": sorted(turmas)}
        for nome, turmas in nomes_turmas.items()
        if len(turmas) > 1
    ]
