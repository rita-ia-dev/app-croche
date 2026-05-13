import flet as ft

from receitas import receitas
from progresso import salvar_progresso, carregar_progresso

def main(page: ft.Page):

    page.title = "App de Crochê da Rita"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#FCE7D0"
    page.scroll = "auto"
    page.padding = 20 
    page.window_icon = "icon.png"
    progresso = carregar_progresso()

    etapa_atual = {"valor": 0}
    receita_atual = {"nome": ""}

    conteudo_receita = ft.Text(
        size=20,
        color="black",
        text_align="center"
    )

    titulo_receita = ft.Text(
        size=28,
        weight="bold",
        color="#FA8C0F"
    )

    lista_receitas = ft.Column(
        spacing=10
    )

    # FUNÇÕES

    def mostrar_entrada(e=None): # O 'e=None' evita erro se for chamada sem evento
        page.clean()
        page.add(
            ft.Column(
                controls=[
                    ft.Container(height=100), # Espaço no topo
                    ft.Text("CROCHÊ ACESSÍVEL", size=35, weight="bold", color="#FA8C0F", text_align="center"),
                    ft.Text("Desenvolvido por Rita", size=15, italic=True),
                    ft.Divider(height=100, color="transparent"),
                    ft.ElevatedButton(
                        "ENTRAR NO APP", 
                        on_click=lambda _: mostrar_inicio(),
                        height=100, 
                        width=320, 
                        bgcolor="#F8AD58", 
                        color="white"
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=page.width
            )
        )
        page.update()

    def mostrar_inicio():

        page.clean()

        categorias = ft.Column(

    [

        ft.Row([ft.Text("CATEGORIAS", size=30, weight="bold", color="#FA8C0F")], alignment=ft.MainAxisAlignment.CENTER),
        ft.ElevatedButton("🏫 ESCOLA DE PONTOS", width=350, height=80, bgcolor="#ffe5c6", color="white", on_click=lambda e: mostrar_categoria("🏫 ESCOLA DE PONTOS")),
        ft.ElevatedButton("🏠 SALA", width=350, height=80, bgcolor="#ffd49f", color="white", on_click=lambda e: mostrar_categoria("🏠 SALA")),
        ft.ElevatedButton("🍳 COZINHA", width=350, height=80, bgcolor="#ffb85c", color="white", on_click=lambda e: mostrar_categoria("🍳 COZINHA")),
        ft.ElevatedButton("🧸 AMIGURUMI", width=350, height=80, bgcolor="#ffa500", color="white", on_click=lambda e: mostrar_categoria("🧸 AMIGURUMI")),
        ft.ElevatedButton("🧶 AMOSTRAS", width=350, height=80, bgcolor="#c07c00", color="white", on_click=lambda e: mostrar_categoria("🧶 AMOSTRAS")),
        ft.ElevatedButton("▶️ CONTINUAR DE ONDE PAREI", width=350, height=80, bgcolor="#805300", color="white", on_click=continuar_projeto),
        ft.ElevatedButton("📂 PROJETOS EM ANDAMENTO", width=350, height=80, bgcolor="#3D2801", color="white",on_click=mostrar_projetos_em_andamento)

    ],

    horizontal_alignment="center",
    spacing=15

)

        layout = ft.Column(
            [

                ft.Container(height=40),

                categorias
            ],
            horizontal_alignment="center",
            width=page.width
        )

        page.add(layout)

        page.update()

    def mostrar_categoria(nome_categoria):

        page.clean()

        titulo = ft.Text(
            nome_categoria,
            size=30,
            weight="bold",
            color="#FA8C0F"
        )

        lista = ft.Column()

        receitas_categoria = receitas[nome_categoria]

        cores_botoes = ["#ffe5c6", "#ffd49f", "#ffb85c", "#ffa500", "#c07c00", "#805300"]

        for i, nome_receita in enumerate(receitas_categoria):

            lista.controls.append(

                ft.ElevatedButton(
                    nome_receita,
                    width=320,
                    height=55,
                    bgcolor=cores_botoes[i % len(cores_botoes)],
                    color="white",
                    on_click=lambda e, n=nome_receita, c=nome_categoria: abrir_receita(c, n)
                )

            )

        page.add(

    ft.Container(

        content=ft.Column(
            [
                titulo,

                ft.Container(height=30),

                lista,

                ft.Container(height=20),

                ft.TextButton(
                    "Voltar",
                    on_click=lambda e: mostrar_inicio()
                )
            ],

            horizontal_alignment="center",
            alignment="center"
        ),

        alignment=ft.Alignment(0, 0),
        expand=True
    )

)
    page.update()
    
    def continuar_projeto(e):

        if not progresso:

            return

        ultima_receita = list(progresso.keys())[-1]

        for categoria in receitas:

            if ultima_receita in receitas[categoria]:

                abrir_receita(categoria, ultima_receita)

                return

    def mostrar_projetos_em_andamento(e):
        page.clean()

        titulo = ft.Text(
            "Projetos em andamento",
            size=28,
            weight="bold",
            color="#FA8C0F",
            text_align="center" # Garante o texto no centro
        )

        # Adicionamos o alinhamento aqui na lista de botões
        lista = ft.Column(horizontal_alignment="center")
        cores_botoes = ["#ffe5c6", "#ffd49f", "#ffb85c", "#ffa500", "#c07c00", "#805300"]

        for i, nome_receita in enumerate(progresso):
            for categoria in receitas:
                if nome_receita in receitas[categoria]:
                    lista.controls.append(
                        ft.ElevatedButton(
    nome_receita,
    width=320,
    bgcolor=cores_botoes[i % len(cores_botoes)],
    color="white",
    on_click=lambda e, c=categoria, n=nome_receita: abrir_receita(c, n)))

        page.add(
            ft.Column(
                [
                    ft.Container(height=40),
                    titulo,
                    lista,
                    ft.Container(height=20),
                    ft.TextButton(
                        "Voltar",
                        on_click=lambda e: mostrar_inicio()
                    )
                ],
                horizontal_alignment="center", 
                width=page.width 
            )
        )

        page.update()

    def abrir_receita(categoria, nome):

        receita_atual["nome"] = nome
        receita_atual["categoria"] = categoria

        salvo = progresso.get(nome, 0)

        etapa_atual["valor"] = salvo

        mostrar_receita()

    def mostrar_receita():

        page.clean()

        nome = receita_atual["nome"]

        categoria = receita_atual["categoria"]

        dados = receitas[categoria][nome]

        imagem = dados["imagem"]

        etapas = dados["etapas"]

        indice = etapa_atual["valor"]

        titulo_receita.value = nome

        conteudo_receita.value = (
            f"Etapa {indice + 1} de {len(etapas)}\n\n"
            f"{etapas[indice]}"
        )

        if indice >= len(etapas) - 1:

            if nome in progresso:

                del progresso[nome]

        else:

            progresso[nome] = indice

            salvar_progresso(nome, indice)

        botoes = ft.Column(

            [
                ft.ElevatedButton(
                    "➡️ Próxima",
                    width=320,
                    height=55,
                    bgcolor="#ffe5c6",
                    color="white",
                    on_click=proxima_etapa
                ),

                ft.ElevatedButton(
                    "⬅️ Voltar",
                    width=320,
                    height=55,
                    bgcolor="#ffd49f",
                    color="white",
                    on_click=etapa_anterior
                ),

                ft.ElevatedButton(
                    "🔄 Reiniciar",
                    width=320,
                    height=55,
                    bgcolor="#ffcb8a",
                    color="white",
                    on_click=reiniciar_receita
                ),
            ],

            horizontal_alignment="center"

        )

        page.add(

            ft.Column(
                [
                    ft.Container(height=20),

                    titulo_receita,

                    ft.Container(

                        content=ft.Image(
                            src=imagem,
                            width=250,
                            fit=ft.ImageFit.CONTAIN
                        ),

                        border_radius=15,

                        border=ft.Border(
                            left=ft.BorderSide(4, "#FA8C0F"),
                            top=ft.BorderSide(4, "#FA8C0F"),
                            right=ft.BorderSide(4, "#FA8C0F"),
                            bottom=ft.BorderSide(4, "#FA8C0F")
                        ),

                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=8,
                            color="black12",
                            offset=ft.Offset(0, 4)
                        ),

                        padding=0
                    ),

                    ft.Container(
                        content=conteudo_receita,
                        padding=20
                    ),

                    botoes,

                    ft.TextButton(
                        "Voltar",
                        on_click=lambda e: mostrar_categoria(
                            receita_atual["categoria"]
                        )
                    )

                ],

                horizontal_alignment="center"
            )

        )

        page.update()

    def proxima_etapa(e):

        nome = receita_atual["nome"]
        categoria = receita_atual["categoria"]

        etapas = receitas[categoria][nome]["etapas"]

        if etapa_atual["valor"] < len(etapas) - 1:

            etapa_atual["valor"] += 1

            mostrar_receita()

    def etapa_anterior(e):

        if etapa_atual["valor"] > 0:

            etapa_atual["valor"] -= 1

            mostrar_receita()

    def reiniciar_receita(e):

        nome = receita_atual["nome"]

        etapa_atual["valor"] = 0

        if nome in progresso:

            del progresso[nome]

        mostrar_receita()

    # INÍCIO

    mostrar_entrada()

if __name__ == "__main__":
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        host="0.0.0.0",
        port=10000,
        assets_dir="assets"
    )