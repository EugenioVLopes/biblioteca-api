from .. import db


class Emprestimo(db.Model):
    __tablename__ = "EMPRESTIMO"
    COD = db.Column(db.Integer, primary_key=True)
    MAT_ALUNO = db.Column(
        "MAT_ALUNO", db.Integer, db.ForeignKey("ALUNO.MAT_ALUNO"), nullable=False
    )
    DATA_EMPRESTIMO = db.Column(db.Date, nullable=False)
    DATA_PREVISTA_DEV = db.Column(db.Date, nullable=False)
    DATA_DEVOLUCAO = db.Column(db.Date)
    DATA_ATRASO = db.Column(db.Date)

    aluno = db.relationship("Aluno", backref=db.backref("emprestimos", lazy=True))

    def to_dict(self):
        """
        Retorna um dicionário com os dados do empréstimo, usando sempre 'COD' como chave do identificador.
        """
        return {
            "COD": self.COD,
            "MAT_ALUNO": int(self.MAT_ALUNO) if self.MAT_ALUNO is not None else None,
            "DATA_EMPRESTIMO": str(self.DATA_EMPRESTIMO),
            "DATA_PREVISTA_DEV": str(self.DATA_PREVISTA_DEV),
            "DATA_DEVOLUCAO": str(self.DATA_DEVOLUCAO) if self.DATA_DEVOLUCAO else None,
            "DATA_ATRASO": str(self.DATA_ATRASO) if self.DATA_ATRASO else None,
        }
