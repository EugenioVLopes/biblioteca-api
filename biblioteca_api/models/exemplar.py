from .. import db


class Exemplar(db.Model):
    __tablename__ = "EXEMPLAR"
    TOMBO = db.Column(db.Integer, primary_key=True, autoincrement=True)
    COD_LIVRO = db.Column(db.Integer, db.ForeignKey("LIVRO.COD"), nullable=False)

    # Relacionamento com Livro
    livro = db.relationship("Livro", backref="exemplares")

    def to_dict(self):
        return {
            "TOMBO": self.TOMBO,
            "COD_LIVRO": self.COD_LIVRO,
        }
