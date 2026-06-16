import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate

from auth_controller import AuthController
from carro_controller import CarroController
from cliente_controller import ClienteController
from config import UI_FILE
from database import Banco
from ordem_servico_controller import OrdemServicoController
from servico_controller import ServicoController
from ui_helpers import UiHelpers


class SistemaOS(
    UiHelpers,
    AuthController,
    ClienteController,
    CarroController,
    ServicoController,
    OrdemServicoController,
):
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.tela = uic.loadUi(str(UI_FILE))
        self.db = Banco()

        self.configurar_tabelas()
        self.conectar_eventos()
        self.carregar_tudo()

        self.tela.stackedWidget.setCurrentIndex(0)
        self.tela.dateOS.setDate(QDate.currentDate())

    def conectar_eventos(self):
        self.conectar_eventos_login_e_navegacao()
        self.conectar_eventos_cliente()
        self.conectar_eventos_carro()
        self.conectar_eventos_servico()
        self.conectar_eventos_ordem_servico()
        self.conectar_eventos_listagem()

    def conectar_eventos_login_e_navegacao(self):
        self.tela.btnEntrar.clicked.connect(self.login)
        self.tela.btnSair.clicked.connect(lambda: self.tela.stackedWidget.setCurrentIndex(0))
        self.tela.btnCardCliente.clicked.connect(lambda: self.tela.tabWidget.setCurrentIndex(1))
        self.tela.btnCardCarro.clicked.connect(lambda: self.tela.tabWidget.setCurrentIndex(2))
        self.tela.btnCardServico.clicked.connect(lambda: self.tela.tabWidget.setCurrentIndex(3))
        self.tela.btnCardOS.clicked.connect(lambda: self.tela.tabWidget.setCurrentIndex(4))
        self.tela.btnCardListarOS.clicked.connect(lambda: self.tela.tabWidget.setCurrentIndex(5))

    def conectar_eventos_cliente(self):
        self.tela.btnNovoCliente.clicked.connect(self.limpar_cliente)
        self.tela.btnLimparCliente.clicked.connect(self.limpar_cliente)
        self.tela.btnSalvarCliente.clicked.connect(self.salvar_cliente)
        self.tela.btnEditarCliente.clicked.connect(self.editar_cliente)
        self.tela.btnExcluirCliente.clicked.connect(self.excluir_cliente)
        self.tela.tblClientes.cellClicked.connect(self.selecionar_cliente)

    def conectar_eventos_carro(self):
        self.tela.btnNovoCarro.clicked.connect(self.limpar_carro)
        self.tela.btnLimparCarro.clicked.connect(self.limpar_carro)
        self.tela.btnSalvarCarro.clicked.connect(self.salvar_carro)
        self.tela.btnEditarCarro.clicked.connect(self.editar_carro)
        self.tela.btnExcluirCarro.clicked.connect(self.excluir_carro)
        self.tela.tblCarros.cellClicked.connect(self.selecionar_carro)

    def conectar_eventos_servico(self):
        self.tela.btnNovoServico.clicked.connect(self.limpar_servico)
        self.tela.btnLimparServico.clicked.connect(self.limpar_servico)
        self.tela.btnSalvarServico.clicked.connect(self.salvar_servico)
        self.tela.btnEditarServico.clicked.connect(self.editar_servico)
        self.tela.btnExcluirServico.clicked.connect(self.excluir_servico)
        self.tela.tblServicos.cellClicked.connect(self.selecionar_servico)

    def conectar_eventos_ordem_servico(self):
        self.tela.btnNovaOS.clicked.connect(self.limpar_os)
        self.tela.btnLimparOS.clicked.connect(self.limpar_os)
        self.tela.btnSalvarOS.clicked.connect(self.salvar_os)
        self.tela.btnEditarOS.clicked.connect(self.editar_os)
        self.tela.btnExcluirOS.clicked.connect(self.excluir_os)
        self.tela.tblOrdensServico.cellClicked.connect(self.selecionar_os)
        self.tela.cmbOSCliente.currentIndexChanged.connect(self.carregar_carros_os)
        self.tela.cmbOSServico.currentIndexChanged.connect(self.preencher_valor_servico)

    def conectar_eventos_listagem(self):
        self.tela.btnPesquisarOS.clicked.connect(self.carregar_listagem_os)
        self.tela.btnAtualizarOS.clicked.connect(self.carregar_listagem_os)

    def carregar_tudo(self):
        self.carregar_clientes()
        self.carregar_combos()
        self.carregar_carros()
        self.carregar_servicos()
        self.carregar_ordens()
        self.carregar_listagem_os()

    def carregar_combos(self):
        clientes = self.db.listar("SELECT id, nome FROM clientes ORDER BY nome")
        self.tela.cmbCarroCliente.clear()
        self.tela.cmbOSCliente.clear()
        for cliente in clientes:
            self.tela.cmbCarroCliente.addItem(cliente["nome"], cliente["id"])
            self.tela.cmbOSCliente.addItem(cliente["nome"], cliente["id"])

        servicos = self.db.listar("SELECT id, nome, valor FROM servicos ORDER BY nome")
        self.tela.cmbOSServico.clear()
        for servico in servicos:
            self.tela.cmbOSServico.addItem(servico["nome"], servico["id"])

        self.carregar_carros_os()

    def executar(self):
        self.tela.show()
        sys.exit(self.app.exec_())
