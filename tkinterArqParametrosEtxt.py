import json
import tkinter as tk
from tkinter import filedialog, messagebox, Text

'''


FUNCIONALIDADES:

--Manipula arquivo de texto podendo abrir, editar, salvar no arquivo existente ou salvar como novo arquivo
nao alterando os dados do original.

--le arquivo parametros.json(deve estar incluido no mesmo diretorio do progama), e possui opcoes para alteracao de
data inicial, data final e nome.

BOTOES:

--Abrir arquivo-- abre o arquivo .txt para ser manipulado
--Salvar Alteracoes-- salva o arquivo .txt com as mudancas feitas
--Salvar como novo arquivo-- salva um novo arquivo .txt sem alterar o arquivo original
--leer dados .json-- ao clicar ele apaga as alteracoes nao salvas e retorna os valores iniciais 
--salvar dados .json-- salva as alteracoes feitas no arquivo .json
--sair-- finaliza o progama


'''
class Editor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.selected_file_path = None

        self.init_ui()

    def init_ui(self):
        # Botoes do arquivo de texto
        btn_abrir = tk.Button(self, text="Abrir arquivo", command=self.abrir_arquivo)
        btn_abrir.place(x=10, y=10, width=100, height=30)

        btn_salvar = tk.Button(self, text="Salvar Alterações", command=self.salvar_arquivo)
        btn_salvar.place(x=120, y=10, width=150, height=30)

        btn_salvar_como = tk.Button(self, text="Salvar como Novo Arquivo", command=self.salvar_como_novo_arquivo)
        btn_salvar_como.place(x=280, y=10, width=180, height=30)

        # Rótulo para exibir o nome do arquivo selecionado
        self.label_arquivo = tk.Label(self, text="Nenhum arquivo selecionado")
        self.label_arquivo.place(x=10, y=50, width=450, height=20)

        # Widget de texto para exibir/editar o conteúdo do arquivo
        self.text_widget = Text(self)
        self.text_widget.place(x=10, y=80, width=480, height=200)

        # Configurações da data inicial
        self.label_data_inicial = tk.Label(self, text="Data Inicial")
        self.label_data_inicial.place(x=10, y=290, width=80, height=20)

        self.data_inicial = tk.Entry(self)
        self.data_inicial.place(x=100, y=290, width=120, height=20)

        # Configurações da data final
        self.label_data_final = tk.Label(self, text="Data Final")
        self.label_data_final.place(x=10, y=320, width=80, height=20)

        self.data_final = tk.Entry(self)
        self.data_final.place(x=100, y=320, width=120, height=20)

        # Configurações da aba Nome
        self.label_nome = tk.Label(self, text="Nome")
        self.label_nome.place(x=10, y=350, width=80, height=20)

        self.nome_tela = tk.Entry(self)
        self.nome_tela.place(x=100, y=350, width=120, height=20)

        # Botão para ler json
        btn_ler_json = tk.Button(self, text="Ler Dados .json", command=self.ler_json)
        btn_ler_json.place(x=10, y=380, width=150, height=30)

        # Botão para Salvar Alterações
        btn_salvar_json = tk.Button(self, text="Salvar Dados .json", command=self.salvar_alteracoes_json)
        btn_salvar_json.place(x=170, y=380, width=150, height=30)

        # Botão de sair
        btn_sair = tk.Button(self, text="Sair", command=self.sair)
        btn_sair.place(x=330, y=380, width=150, height=30)

        # Preenche campos da tela
        dados = self.ler_arquivo_json("parametros.json")

        if dados is not None:
            nome_var = dados.get("nome", "")
            data_inicial_var = dados.get("data_inicial", "")
            data_final_var = dados.get("data_final", "")

            self.nome_tela.insert(0, nome_var)
            self.data_inicial.insert(0, data_inicial_var)
            self.data_final.insert(0, data_final_var)

        self.geometry("500x420")
        self.title("Aplicação para manipular arquivos")
        self.mainloop()

    def sair(self):
        reply = messagebox.askquestion('Sair', 'Deseja realmente sair?')
        if reply == 'yes':
            self.destroy()

    def abrir_arquivo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()

            self.selected_file_path = file_path
            self.label_arquivo.config(text=f"Arquivo selecionado: {self.selected_file_path}")
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, content)

    def salvar_arquivo(self):
        content = self.text_widget.get(1.0, tk.END)
        if content and self.selected_file_path:
            with open(self.selected_file_path, 'w') as file:
                file.write(content)
            messagebox.showinfo("Salvo com sucesso", f"Alterações salvas em: {self.selected_file_path}")

    def salvar_como_novo_arquivo(self):
        content = self.text_widget.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(content)
            messagebox.showinfo("Salvo com sucesso", f"Arquivo salvo em: {file_path}")

    def ler_arquivo_json(self, caminho):
        try:
            with open(caminho, 'r') as arquivo:
                dados = json.load(arquivo)
            return dados
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo JSON não encontrado!")
            return None
        except json.JSONDecodeError:
            messagebox.showerror("Erro", "Erro ao decodificar o arquivo JSON!")
            return None

    def salvar_alteracoes_json(self):
        new_nome = self.nome_tela.get()
        new_data_inicial = self.data_inicial.get()
        new_data_final = self.data_final.get()

        with open("parametros.json", "r+") as json_file:
            data = json.load(json_file)

            data["nome"] = new_nome
            data["data_inicial"] = new_data_inicial
            data["data_final"] = new_data_final

            json_file.seek(0)  # rewind
            json.dump(data, json_file)
            json_file.truncate()

    def ler_json(self):
        dados = self.ler_arquivo_json("parametros.json")

        if dados is not None:
            self.nome_tela.delete(0, tk.END)
            self.nome_tela.insert(0, dados.get("nome", ""))
            self.data_inicial.delete(0, tk.END)
            self.data_inicial.insert(0, dados.get("data_inicial", ""))
            self.data_final.delete(0, tk.END)
            self.data_final.insert(0, dados.get("data_final", ""))

if __name__ == '__main__':
    editor = Editor()