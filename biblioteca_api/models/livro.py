from .. import db


class Livro(db.Model):
    __tablename__ = "LIVRO"
    COD = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TITULO = db.Column(db.String(200), nullable=False)
    AUTOR = db.Column(db.String(100))
    EDITORA = db.Column(db.String(100))
    ANO = db.Column(db.Integer)

    def __init__(self, TITULO, AUTOR, EDITORA=None, ANO=None):
        self.TITULO = TITULO
        self.AUTOR = AUTOR
        self.EDITORA = EDITORA
        self.ANO = ANO

    def to_dict(self):
        return {
            "COD": self.COD,
            "TITULO": self.TITULO,
            "AUTOR": self.AUTOR,
            "EDITORA": self.EDITORA,
            "ANO": self.ANO,
        }
