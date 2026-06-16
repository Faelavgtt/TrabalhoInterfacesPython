import sqlite3


class ClienteController:
    def limpar_cliente(self):
        self.tela.txtClienteId.clear()
        self.tela.txtClienteNome.clear()
        self.tela.txtClienteCpf.clear()
        self.tela.txtClienteTelefone.clear()
        self.tela.txtClienteEmail.clear()
        self.tela.txtClienteEndereco.clear()

    def salvar_cliente(self):
        nome = self.tela.txtClienteNome.text().strip()
        if not nome:
            self.erro("Digite o nome do cliente.")
            return
        self.db.executar(
            "INSERT INTO clientes (nome, cpf, telefone, email, endereco) VALUES (?, ?, ?, ?, ?)",
            (
                nome,
                self.tela.txtClienteCpf.text().strip(),
                self.tela.txtClienteTelefone.text().strip(),
                self.tela.txtClienteEmail.text().strip(),
                self.tela.txtClienteEndereco.text().strip(),
            ),
        )
        self.limpar_cliente()
        self.carregar_tudo()
        self.aviso("Aviso", "Cliente salvo.")

    def editar_cliente(self):
        cliente_id = self.tela.txtClienteId.text().strip()
        if not cliente_id:
            self.erro("Selecione um cliente na tabela para editar.")
            return
        self.db.executar(
            "UPDATE clientes SET nome=?, cpf=?, telefone=?, email=?, endereco=? WHERE id=?",
            (
                self.tela.txtClienteNome.text().strip(),
                self.tela.txtClienteCpf.text().strip(),
                self.tela.txtClienteTelefone.text().strip(),
                self.tela.txtClienteEmail.text().strip(),
                self.tela.txtClienteEndereco.text().strip(),
                cliente_id,
            ),
        )
        self.carregar_tudo()
        self.aviso("Aviso", "Cliente alterado.")

    def excluir_cliente(self):
        cliente_id = self.tela.txtClienteId.text().strip()
        if not cliente_id:
            self.erro("Selecione um cliente na tabela para excluir.")
            return
        mensagem = "Excluir este cliente? Carros e OS vinculados podem impedir a exclusao."
        if self.confirmar(mensagem):
            try:
                self.db.executar("DELETE FROM clientes WHERE id=?", (cliente_id,))
                self.limpar_cliente()
                self.carregar_tudo()
            except sqlite3.IntegrityError:
                self.erro("Nao foi possivel excluir. Existe carro ou OS vinculada a este cliente.")

    def carregar_clientes(self):
        linhas = self.db.listar("SELECT id, nome, cpf, telefone, email FROM clientes ORDER BY id DESC")
        self.preencher_tabela(self.tela.tblClientes, [tuple(l) for l in linhas])

    def selecionar_cliente(self, row, col):
        cliente_id = self.item(self.tela.tblClientes, row, 0)
        cliente = self.db.um("SELECT * FROM clientes WHERE id=?", (cliente_id,))
        if cliente:
            self.tela.txtClienteId.setText(str(cliente["id"]))
            self.tela.txtClienteNome.setText(cliente["nome"] or "")
            self.tela.txtClienteCpf.setText(cliente["cpf"] or "")
            self.tela.txtClienteTelefone.setText(cliente["telefone"] or "")
            self.tela.txtClienteEmail.setText(cliente["email"] or "")
            self.tela.txtClienteEndereco.setText(cliente["endereco"] or "")
