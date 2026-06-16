class AuthController:
    def login(self):
        usuario = self.tela.txtUsuario.text().strip()
        senha = self.tela.txtSenha.text().strip()
        user = self.db.um(
            "SELECT * FROM usuarios WHERE usuario=? AND senha=?",
            (usuario, senha),
        )
        if user:
            self.tela.stackedWidget.setCurrentIndex(1)
            self.tela.tabWidget.setCurrentIndex(0)
            self.tela.txtSenha.clear()
        else:
            self.erro("Usuario ou senha errado.")
