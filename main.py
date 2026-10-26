from core import (
    buscar_por_matricula,
    calcular_frequencia,
    calcular_media,
    cadastrar_estudante,
    classificar_situacao,
    listar_nomes_em_turmas_diferentes,
    listar_ordenado_por_media,
    listar_por_nome,
    listar_por_turma,
    registrar_avaliacoes,
    registrar_frequencia,
    remover_estudante,
    estudantes,
    atualizar_estudante,
)
from ui import cabecalho, limpar_tela, menu, mensagem


def consultar_estudante():
    cabecalho("CONSULTAR ESTUDANTE")
    print("1. Por matrícula")
    print("2. Por nome")
    print("3. Por turma")

    opcao = input("Escolha: ").strip()
    encontrados = []

    if opcao == "1":
        matricula = input("Digite a matrícula: ").strip()
        est = buscar_por_matricula(matricula)
        if est:
            encontrados.append(est)
    elif opcao == "2":
        nome = input("Digite o nome (ou parte do nome): ").strip()
        encontrados = listar_por_nome(nome)
    elif opcao == "3":
        turma = input("Digite a turma: ").strip()
        encontrados = listar_por_turma(turma)
    else:
        mensagem("erro", "Opção inválida!")
        return

    if not encontrados:
        mensagem("info", "Nenhum estudante encontrado.")
        return

    for est in encontrados:
        media = calcular_media(est["avaliacoes"])
        situacao = classificar_situacao(media)
        freq = calcular_frequencia(est["aulas_previstas"], est["presencas"])

        print(f"\nMatrícula: {est['matricula']}")
        print(f"Nome: {est['nome']}")
        print(f"Turma: {est['turma']}")
        print(f"Avaliações: {est['avaliacoes']}")
        print(f"Média: {media:.2f} | Situação: {situacao}")
        print(f"Frequência: {freq:.1f}%")


def cadastrar_estudante_no_sistema():
    cabecalho("CADASTRAR ESTUDANTE")
    matricula = input("Matrícula: ").strip()

    if buscar_por_matricula(matricula):
        mensagem("erro", "Já existe um estudante com essa matrícula!")
        return

    nome = input("Nome completo: ").strip()
    turma = input("Turma: ").strip()

    if cadastrar_estudante(matricula, nome, turma):
        mensagem("sucesso", "Estudante cadastrado com sucesso!")


def atualizar_estudante_no_sistema():
    cabecalho("ATUALIZAR ESTUDANTE")
    matricula = input("Matrícula do estudante: ").strip()

    est = buscar_por_matricula(matricula)
    if not est:
        mensagem("erro", "Estudante não encontrado!")
        return

    print(f"Estudante atual: {est['nome']} - Turma: {est['turma']}")

    novo_nome = input("Novo nome (deixe em branco para manter): ").strip()
    nova_turma = input("Nova turma (deixe em branco para manter): ").strip()

    if atualizar_estudante(matricula, novo_nome, nova_turma):
        mensagem("sucesso", "Dados atualizados com sucesso!")


def remover_estudante_no_sistema():
    cabecalho("REMOVER ESTUDANTE")
    matricula = input("Matrícula do estudante: ").strip()

    est = buscar_por_matricula(matricula)
    if not est:
        mensagem("erro", "Estudante não encontrado!")
        return

    confirmacao = input(f"Tem certeza que deseja remover {est['nome']}? (s/n): ").strip().lower()
    if confirmacao == "s":
        if remover_estudante(matricula):
            mensagem("sucesso", "Estudante removido com sucesso!")
    else:
        mensagem("info", "Remoção cancelada.")


def registrar_avaliacoes_no_sistema():
    cabecalho("REGISTRAR AVALIAÇÕES")
    matricula = input("Matrícula do estudante: ").strip()

    if not buscar_por_matricula(matricula):
        mensagem("erro", "Estudante não encontrado!")
        return

    try:
        quantidade = int(input("Quantas notas deseja adicionar? "))
        notas = []
        for i in range(quantidade):
            nota = float(input(f"Nota {i + 1}: "))
            if 0 <= nota <= 10:
                notas.append(nota)
            else:
                print("Nota inválida (deve ser entre 0 e 10). Ignorada.")

        if registrar_avaliacoes(matricula, notas):
            mensagem("sucesso", "Avaliações registradas com sucesso!")
    except ValueError:
        mensagem("erro", "Entrada inválida! Digite números.")


def registrar_frequencia_no_sistema():
    cabecalho("REGISTRAR FREQUÊNCIA")
    matricula = input("Matrícula do estudante: ").strip()

    if not buscar_por_matricula(matricula):
        mensagem("erro", "Estudante não encontrado!")
        return

    try:
        aulas = int(input("Total de aulas previstas: "))
        presencas = int(input("Total de presenças: "))

        if registrar_frequencia(matricula, aulas, presencas):
            mensagem("sucesso", "Frequência registrada com sucesso!")
        else:
            mensagem("erro", "Valores inválidos!")
    except ValueError:
        mensagem("erro", "Entrada inválida! Digite números inteiros.")


def relatorio_individual():
    cabecalho("RELATÓRIO INDIVIDUAL")
    matricula = input("Matrícula do estudante: ").strip()

    est = buscar_por_matricula(matricula)
    if not est:
        mensagem("erro", "Estudante não encontrado!")
        return

    media = calcular_media(est["avaliacoes"])
    situacao = classificar_situacao(media)
    freq = calcular_frequencia(est["aulas_previstas"], est["presencas"])

    print("\n========== RELATÓRIO INDIVIDUAL ==========")
    print(f"Matrícula: {est['matricula']}")
    print(f"Nome: {est['nome']}")
    print(f"Turma: {est['turma']}")
    print(f"Avaliações: {est['avaliacoes']}")
    print(f"Média: {media:.2f}")
    print(f"Situação acadêmica: {situacao}")
    print(f"Aulas previstas: {est['aulas_previstas']}")
    print(f"Presenças: {est['presencas']}")
    print(f"Frequência: {freq:.1f}%")

    if freq < 75:
        mensagem("erro", "ATENÇÃO: Frequência abaixo do mínimo de 75%!")
    print("==========================================")


def relatorio_geral():
    cabecalho("RELATÓRIO GERAL")
    if not estudantes:
        mensagem("info", "Nenhum estudante cadastrado.")
        return

    aprovados = recuperacao = reprovados = 0
    medias = []

    for est in estudantes:
        media = calcular_media(est["avaliacoes"])
        situacao = classificar_situacao(media)
        medias.append(media)

        if situacao == "Aprovado":
            aprovados += 1
        elif situacao == "Recuperação":
            recuperacao += 1
        else:
            reprovados += 1

    print("\n========== RELATÓRIO GERAL ==========")
    print(f"Total de estudantes: {len(estudantes)}")
    print(f"Aprovados: {aprovados}")
    print(f"Em recuperação: {recuperacao}")
    print(f"Reprovados: {reprovados}")

    if medias:
        print(f"Maior média: {max(medias):.2f}")
        print(f"Menor média: {min(medias):.2f}")
    print("=====================================")


def estudantes_acompanhamento():
    cabecalho("ACOMPANHAMENTO PEDAGÓGICO")
    encontrados = False

    for est in estudantes:
        media = calcular_media(est["avaliacoes"])
        freq = calcular_frequencia(est["aulas_previstas"], est["presencas"])
        situacao = classificar_situacao(media)

        if situacao != "Aprovado" or freq < 75:
            encontrados = True
            print(f"\nMatrícula: {est['matricula']} | Nome: {est['nome']}")
            print(f"Turma: {est['turma']} | Média: {media:.2f} ({situacao})")
            print(f"Frequência: {freq:.1f}%")

    if not encontrados:
        mensagem("info", "Nenhum estudante precisa de acompanhamento no momento.")


def ordenar_por_media():
    cabecalho("CLASSIFICAÇÃO POR MÉDIA")
    if not estudantes:
        mensagem("info", "Nenhum estudante cadastrado.")
        return

    ordenados = listar_ordenado_por_media()

    for i, est in enumerate(ordenados, 1):
        media = calcular_media(est["avaliacoes"])
        situacao = classificar_situacao(media)
        print(f"{i}º - {est['nome']} ({est['matricula']}) | Média: {media:.2f} | {situacao}")


def nomes_em_turmas_diferentes():
    cabecalho("NOMES EM TURMAS DIFERENTES")
    resultados = listar_nomes_em_turmas_diferentes()

    if not resultados:
        mensagem("info", "Nenhum nome aparece em turmas diferentes.")
        return

    for item in resultados:
        print(f"Nome: {item['nome']} → Turmas: {', '.join(item['turmas'])}")


def main():
    while True:
        limpar_tela()
        menu()
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_estudante_no_sistema()
        elif opcao == "2":
            consultar_estudante()
        elif opcao == "3":
            atualizar_estudante_no_sistema()
        elif opcao == "4":
            remover_estudante_no_sistema()
        elif opcao == "5":
            registrar_avaliacoes_no_sistema()
        elif opcao == "6":
            registrar_frequencia_no_sistema()
        elif opcao == "7":
            relatorio_individual()
        elif opcao == "8":
            relatorio_geral()
        elif opcao == "9":
            estudantes_acompanhamento()
        elif opcao == "10":
            ordenar_por_media()
        elif opcao == "11":
            nomes_em_turmas_diferentes()
        elif opcao == "0":
            print("\nEncerrando o sistema... Até logo!")
            break
        else:
            mensagem("erro", "Opção inválida! Tente novamente.")

        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()
