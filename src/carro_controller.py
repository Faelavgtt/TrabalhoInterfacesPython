import sqlite3


class CarroController:
    def limpar_carro(self):
        self.tela.txtCarroId.clear()
        self.tela.txtCarroMarca.clear()
        self.tela.txtCarroModelo.clear()
        self.tela.txtCarroPlaca.clear()
        self.tela.spnCarroAno.setValue(2026)

    def salvar_carro(self):
        cliente_id = self.tela.cmbCarroCliente.currentData()
        marca = self.tela.txtCarroMarca.text().strip()
        modelo = self.tela.txtCarroModelo.text().strip()
        if not cliente_id:
            self.erro("Cadastre um cliente antes de cadastrar carro.")
            return
        if not marca or not modelo:
            self.erro("Digite marca e modelo do carro.")
            return
        self.db.executar(
            "INSERT INTO carros (cliente_id, marca, modelo, placa, ano) VALUES (?, ?, ?, ?, ?)",
            (
                cliente_id,
                marca,
                modelo,
                self.tela.txtCarroPlaca.text().strip(),
                self.tela.spnCarroAno.value(),
            ),
        )
        self.limpar_carro()
        self.carregar_tudo()
        self.aviso("Aviso", "Carro salvo.")

    def editar_carro(self):
        carro_id = self.tela.txtCarroId.text().strip()
        if not carro_id:
            self.erro("Selecione um carro na tabela para editar.")
            return
        self.db.executar(
            "UPDATE carros SET cliente_id=?, marca=?, modelo=?, placa=?, ano=? WHERE id=?",
            (
                self.tela.cmbCarroCliente.currentData(),
                self.tela.txtCarroMarca.text().strip(),
                self.tela.txtCarroModelo.text().strip(),
                self.tela.txtCarroPlaca.text().strip(),
                self.tela.spnCarroAno.value(),
                carro_id,
            ),
        )
        self.carregar_tudo()
        self.aviso("Aviso", "Carro alterado.")

    def excluir_carro(self):
        carro_id = self.tela.txtCarroId.text().strip()
        if not carro_id:
            self.erro("Selecione um carro na tabela para excluir.")
            return
        if self.confirmar("Excluir este carro?"):
            try:
                self.db.executar("DELETE FROM carros WHERE id=?", (carro_id,))
                self.limpar_carro()
                self.carregar_tudo()
            except sqlite3.IntegrityError:
                self.erro("Nao foi possivel excluir. Existe OS vinculada a este carro.")

    def carregar_carros(self):
        linhas = self.db.listar("""
            SELECT carros.id, clientes.nome, carros.marca, carros.modelo, carros.placa, carros.ano
            FROM carros
            JOIN clientes ON clientes.id = carros.cliente_id
            ORDER BY carros.id DESC
        """)
        self.preencher_tabela(self.tela.tblCarros, [tuple(l) for l in linhas])

    def selecionar_carro(self, row, col):
        carro_id = self.item(self.tela.tblCarros, row, 0)
        carro = self.db.um("SELECT * FROM carros WHERE id=?", (carro_id,))
        if carro:
            self.tela.txtCarroId.setText(str(carro["id"]))
            self.selecionar_combo_por_id(self.tela.cmbCarroCliente, carro["cliente_id"])
            self.tela.txtCarroMarca.setText(carro["marca"] or "")
            self.tela.txtCarroModelo.setText(carro["modelo"] or "")
            self.tela.txtCarroPlaca.setText(carro["placa"] or "")
            self.tela.spnCarroAno.setValue(carro["ano"] or 2026)
