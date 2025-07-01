from .. import db


class Aluno(db.Model):
    __tablename__ = "ALUNO"
    MAT_ALUNO = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NOME = db.Column(db.String(100), nullable=False)
    EMAIL = db.Column(db.String(100))
    CURSO = db.Column(db.String(100))

    def to_dict(self):
        return {
            "MAT_ALUNO": self.MAT_ALUNO,
            "NOME": self.NOME,
            "EMAIL": self.EMAIL,
            "CURSO": self.CURSO,
        }
