from controller.cadastro import cadastrar_aluno
from controller.camera import iniciar_reconhecimento

def main(): # type: ignore
    print("=== SISTEMA DE RECONHECIMENTO FACIAL ===")
    print("1 - Cadastrar novo aluno")
    print("2 - Iniciar reconhecimento facial")
    print("0 - Sair")

    while True:
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Digite o nome do aluno: ").strip()
            if nome:
                cadastrar_aluno(nome)
            else:
                print("Nome inválido.")
        elif opcao == "2":
            iniciar_reconhecimento()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
from controller.cadastro import cadastrar_aluno
from controller.camera import iniciar_reconhecimento

def main():
    print("=== SISTEMA DE RECONHECIMENTO FACIAL ===")
    print("1 - Cadastrar novo aluno")
    print("2 - Iniciar reconhecimento facial")
    print("0 - Sair")

    while True:
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Digite o nome do aluno: ").strip()
            if nome:
                cadastrar_aluno(nome)
            else:
                print("Nome inválido.")
        elif opcao == "2":
            iniciar_reconhecimento()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
