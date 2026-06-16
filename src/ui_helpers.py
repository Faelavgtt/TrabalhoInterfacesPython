from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView


class UiHelpers:
    def configurar_tabelas(self):
        tabelas = [
            self.tela.tblClientes,
            self.tela.tblCarros,
            self.tela.tblServicos,
            self.tela.tblOrdensServico,
            self.tela.tblListarOrdens,
        ]
        for tabela in tabelas:
            tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def aviso(self, titulo, texto):
        QMessageBox.information(self.tela, titulo, texto)

    def erro(self, texto):
        QMessageBox.warning(self.tela, "Aviso", texto)

    def confirmar(self, texto):
        return QMessageBox.question(
            self.tela,
            "Confirmar",
            texto,
            QMessageBox.Yes | QMessageBox.No,
        ) == QMessageBox.Yes

    def item(self, tabela, row, col):
        it = tabela.item(row, col)
        return it.text() if it else ""

    def preencher_tabela(self, tabela, linhas):
        tabela.setRowCount(0)
        for row_num, linha in enumerate(linhas):
            tabela.insertRow(row_num)
            for col_num, valor in enumerate(linha):
                texto = str(valor if valor is not None else "")
                tabela.setItem(row_num, col_num, QTableWidgetItem(texto))

    def selecionar_combo_por_id(self, combo, valor_id):
        for i in range(combo.count()):
            if combo.itemData(i) == valor_id:
                combo.setCurrentIndex(i)
                return
