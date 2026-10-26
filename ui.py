import os


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def cabecalho(titulo):
    print("\n" + "=" * 26)
    print(f"   {titulo}")
    print("=" * 26)


def mensagem(tipo, texto):
    icones = {
        "sucesso": "✓",
        "erro": "✕",
        "info": "ℹ",
    }
    print(f"{icones.get(tipo, '•')} {texto}")


def menu():
    cabecalho("CONTROLE ACADÊMICO")
    print("1.  Cadastrar estudante")
    print("2.  Consultar estudante")
    print("3.  Atualizar estudante")
    print("4.  Remover estudante")
    print("5.  Registrar avaliações")
    print("6.  Registrar frequência")
    print("7.  Relatório individual")
    print("8.  Relatório geral")
    print("9.  Estudantes em acompanhamento")
    print("10. Ordenar por média")
    print("11. Nomes em turmas diferentes")
    print("0.  Sair do sistema")
    print("=" * 52)
