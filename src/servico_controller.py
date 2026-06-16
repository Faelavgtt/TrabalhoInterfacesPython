import sqlite3


class ServicoController:
    def limpar_servico(self):
        self.tela.txtServicoId.clear()
        self.tela.txtServicoNome.clear()
        self.tela.txtServicoDescricao.clear()
        self.tela.spnServicoValor.setValue(0)

    def salvar_servico(self):
        nome = self.tela.txtServicoNome.text().strip()
        if not nome:
            self.erro("Digite o nome do servico.")
            return
        self.db.executar(
            "INSERT INTO servicos (nome, descricao, valor) VALUES (?, ?, ?)",
            (
                nome,
                self.tela.txtServicoDescricao.toPlainText().strip(),
                self.tela.spnServicoValor.value(),
            ),
        )
        self.limpar_servico()
        self.carregar_tudo()
        self.aviso("Aviso", "Servico salvo.")

    def editar_servico(self):
        servico_id = self.tela.txtServicoId.text().strip()
        if not servico_id:
            self.erro("Selecione um servico na tabela para editar.")
            return
        self.db.executar(
            "UPDATE servicos SET nome=?, descricao=?, valor=? WHERE id=?",
            (
                self.tela.txtServicoNome.text().strip(),
                self.tela.txtServicoDescricao.toPlainText().strip(),
                self.tela.spnServicoValor.value(),
                servico_id,
            ),
        )
        self.carregar_tudo()
        self.aviso("Aviso", "Servico alterado.")

    def excluir_servico(self):
        servico_id = self.tela.txtServicoId.text().strip()
        if not servico_id:
            self.erro("Selecione um servico na tabela para excluir.")
            return
        if self.confirmar("Excluir este servico?"):
            try:
                self.db.executar("DELETE FROM servicos WHERE id=?", (servico_id,))
                self.limpar_servico()
                self.carregar_tudo()
            except sqlite3.IntegrityError:
                self.erro("Nao foi possivel excluir. Existe OS vinculada a este servico.")

    def carregar_servicos(self):
        linhas = self.db.listar("SELECT id, nome, descricao, printf('%.2f', valor) FROM servicos ORDER BY id DESC")
        self.preencher_tabela(self.tela.tblServicos, [tuple(l) for l in linhas])

    def selecionar_servico(self, row, col):
        servico_id = self.item(self.tela.tblServicos, row, 0)
        servico = self.db.um("SELECT * FROM servicos WHERE id=?", (servico_id,))
        if servico:
            self.tela.txtServicoId.setText(str(servico["id"]))
            self.tela.txtServicoNome.setText(servico["nome"] or "")
            self.tela.txtServicoDescricao.setPlainText(servico["descricao"] or "")
            self.tela.spnServicoValor.setValue(float(servico["valor"] or 0))
