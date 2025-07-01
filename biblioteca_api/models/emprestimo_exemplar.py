from .. import db


class EmprestimoExemplar(db.Model):
    __tablename__ = "EMP_EXEMPLAR"
    cod_emprestimo = db.Column(
        db.Integer, db.ForeignKey("EMPRESTIMO.COD"), primary_key=True
    )
    tombo_exemplar = db.Column(
        db.Integer, db.ForeignKey("EXEMPLAR.TOMBO"), primary_key=True
    )

    emprestimo = db.relationship(
        "Emprestimo", backref=db.backref("emprestimo_exemplares", lazy=True)
    )
    exemplar = db.relationship(
        "Exemplar", backref=db.backref("emprestimo_exemplares", lazy=True)
    )

    def to_dict(self):
        return {
            "COD_EMPRESTIMO": self.cod_emprestimo,
            "TOMBO_EXEMPLAR": self.tombo_exemplar,
        }
