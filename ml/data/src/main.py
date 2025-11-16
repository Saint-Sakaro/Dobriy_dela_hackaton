from seeker.seeker import Seeker

def main():
    # Инициализация Seeker с ключом GigaChat
    seeker = Seeker(
        gigachat_creds="MDE5YTg2Y2ItNTg0YS03YmJkLTg1MjctZDZmNGI0MDBiZmU3OmFjMDI1NTA0LTVhOTAtNGUyOS1hNmVjLTEwMmE0ZDYyYjQxMQ=="
    )

    print("=== RAG-поиск событий ===")
    initial_query = input("Введите ваш запрос: ")
    response = seeker.ask_llm(query_text=initial_query, toa="Прошедшее")
    print("\n[Модель ответила]:")
    print(response)

    print("\nТеперь вы можете задавать уточняющие вопросы.")
    print("Чтобы начать новый диалог, введите команду 'СБРОС'.")
    print("Чтобы завершить сессию, введите 'ВЫХОД'.\n")

    while True:
        user_input = input("Ваш вопрос: ").strip()
        if not user_input:
            continue

        if user_input.upper() == "ВЫХОД":
            print("Сессия завершена.")
            break
        elif user_input.upper() == "СБРОС":
            seeker.reset()
            print("История диалога сброшена. Начинаем новый диалог.")
            initial_query = input("Введите новый запрос: ")
            response = seeker.ask_llm(query_text=initial_query)
            print("\n[Модель ответила]:")
            print(response)
            continue

        # Уточняющий вопрос в рамках текущего диалога
        answer = seeker.ask_llm(query_text=user_input)
        print("\n[Модель ответила]:")
        print(answer)


if __name__ == "__main__":
    main()
