from PyQt5.QtCore import QDate


class OrdemServicoController:
    def carregar_carros_os(self):
        cliente_id = self.tela.cmbOSCliente.currentData()
        self.tela.cmbOSCarro.clear()
        if not cliente_id:
            return
        carros = self.db.listar(
            "SELECT id, marca, modelo, placa FROM carros WHERE cliente_id=? ORDER BY marca, modelo",
            (cliente_id,),
        )
        for carro in carros:
            texto = f"{carro['marca']} {carro['modelo']} - {carro['placa']}"
            self.tela.cmbOSCarro.addItem(texto, carro["id"])

    def preencher_valor_servico(self):
        servico_id = self.tela.cmbOSServico.currentData()
        if servico_id:
            servico = self.db.um("SELECT valor FROM servicos WHERE id=?", (servico_id,))
            if servico:
                self.tela.spnOSValor.setValue(float(servico["valor"] or 0))

    def limpar_os(self):
        self.tela.txtOSId.clear()
        self.tela.dateOS.setDate(QDate.currentDate())
        self.tela.cmbOSStatus.setCurrentIndex(0)
        self.tela.spnOSValor.setValue(0)
        self.tela.txtOSObs.clear()
        self.preencher_valor_servico()

    def salvar_os(self):
        cliente_id = self.tela.cmbOSCliente.currentData()
        carro_id = self.tela.cmbOSCarro.currentData()
        servico_id = self.tela.cmbOSServico.currentData()
        if not cliente_id or not carro_id or not servico_id:
            self.erro("Cadastre cliente, carro e servico antes de criar uma OS.")
            return
        self.db.executar(
            """
            INSERT INTO ordens_servico
            (cliente_id, carro_id, servico_id, data, status, valor, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                cliente_id,
                carro_id,
                servico_id,
                self.tela.dateOS.date().toString("yyyy-MM-dd"),
                self.tela.cmbOSStatus.currentText(),
                self.tela.spnOSValor.value(),
                self.tela.txtOSObs.toPlainText().strip(),
            ),
        )
        self.limpar_os()
        self.carregar_tudo()
        self.aviso("Aviso", "Ordem salva.")

    def editar_os(self):
        os_id = self.tela.txtOSId.text().strip()
        if not os_id:
            self.erro("Selecione uma OS na tabela para editar.")
            return
        self.db.executar(
            """
            UPDATE ordens_servico
            SET cliente_id=?, carro_id=?, servico_id=?, data=?, status=?, valor=?, observacoes=?
            WHERE id=?
            """,
            (
                self.tela.cmbOSCliente.currentData(),
                self.tela.cmbOSCarro.currentData(),
                self.tela.cmbOSServico.currentData(),
                self.tela.dateOS.date().toString("yyyy-MM-dd"),
                self.tela.cmbOSStatus.currentText(),
                self.tela.spnOSValor.value(),
                self.tela.txtOSObs.toPlainText().strip(),
                os_id,
            ),
        )
        self.carregar_tudo()
        self.aviso("Aviso", "OS alterada.")

    def excluir_os(self):
        os_id = self.tela.txtOSId.text().strip()
        if not os_id:
            self.erro("Selecione uma OS na tabela para excluir.")
            return
        if self.confirmar("Excluir esta ordem de servico?"):
            self.db.executar("DELETE FROM ordens_servico WHERE id=?", (os_id,))
            self.limpar_os()
            self.carregar_tudo()

    def carregar_ordens(self):
        linhas = self.db.listar("""
            SELECT os.id, cl.nome, ca.marca || ' ' || ca.modelo, se.nome, os.data, os.status, printf('%.2f', os.valor)
            FROM ordens_servico os
            JOIN clientes cl ON cl.id = os.cliente_id
            JOIN carros ca ON ca.id = os.carro_id
            JOIN servicos se ON se.id = os.servico_id
            ORDER BY os.id DESC
        """)
        self.preencher_tabela(self.tela.tblOrdensServico, [tuple(l) for l in linhas])

    def selecionar_os(self, row, col):
        os_id = self.item(self.tela.tblOrdensServico, row, 0)
        ordem = self.db.um("SELECT * FROM ordens_servico WHERE id=?", (os_id,))
        if ordem:
            self.tela.txtOSId.setText(str(ordem["id"]))
            self.selecionar_combo_por_id(self.tela.cmbOSCliente, ordem["cliente_id"])
            self.carregar_carros_os()
            self.selecionar_combo_por_id(self.tela.cmbOSCarro, ordem["carro_id"])
            self.selecionar_combo_por_id(self.tela.cmbOSServico, ordem["servico_id"])
            self.tela.dateOS.setDate(QDate.fromString(ordem["data"], "yyyy-MM-dd"))
            self.tela.cmbOSStatus.setCurrentText(ordem["status"])
            self.tela.spnOSValor.setValue(float(ordem["valor"] or 0))
            self.tela.txtOSObs.setPlainText(ordem["observacoes"] or "")

    def carregar_listagem_os(self):
        busca = self.tela.txtPesquisarOS.text().strip()
        status = self.tela.cmbFiltroStatus.currentText()
        params = []
        where = []

        if busca:
            where.append("""
                (CAST(os.id AS TEXT) LIKE ? OR cl.nome LIKE ? OR ca.placa LIKE ? OR se.nome LIKE ?)
            """)
            termo = f"%{busca}%"
            params.extend([termo, termo, termo, termo])

        if status != "Todos os status":
            where.append("os.status = ?")
            params.append(status)

        sql = """
            SELECT os.id, cl.nome, cl.telefone,
                   ca.marca || ' ' || ca.modelo, ca.placa,
                   se.nome, os.data, os.status, printf('%.2f', os.valor)
            FROM ordens_servico os
            JOIN clientes cl ON cl.id = os.cliente_id
            JOIN carros ca ON ca.id = os.carro_id
            JOIN servicos se ON se.id = os.servico_id
        """
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY os.id DESC"

        linhas = self.db.listar(sql, params)
        self.preencher_tabela(self.tela.tblListarOrdens, [tuple(l) for l in linhas])
