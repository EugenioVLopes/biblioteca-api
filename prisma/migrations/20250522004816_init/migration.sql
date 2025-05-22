-- CreateTable
CREATE TABLE "Aluno" (
    "mat" INTEGER NOT NULL,
    "nome" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "curso" TEXT NOT NULL,

    CONSTRAINT "Aluno_pkey" PRIMARY KEY ("mat")
);

-- CreateTable
CREATE TABLE "Livro" (
    "cod" INTEGER NOT NULL,
    "titulo" TEXT NOT NULL,
    "autor" TEXT NOT NULL,
    "editora" TEXT NOT NULL,
    "ano" INTEGER NOT NULL,

    CONSTRAINT "Livro_pkey" PRIMARY KEY ("cod")
);

-- CreateTable
CREATE TABLE "Exemplar" (
    "tombo" INTEGER NOT NULL,
    "codLivro" INTEGER NOT NULL,

    CONSTRAINT "Exemplar_pkey" PRIMARY KEY ("tombo")
);

-- CreateTable
CREATE TABLE "Emprestimo" (
    "cod" INTEGER NOT NULL,
    "matAluno" INTEGER NOT NULL,
    "dataEmp" TIMESTAMP(3) NOT NULL,
    "dataPrev" TIMESTAMP(3) NOT NULL,
    "dataDev" TIMESTAMP(3),
    "atraso" BOOLEAN NOT NULL,

    CONSTRAINT "Emprestimo_pkey" PRIMARY KEY ("cod")
);

-- CreateTable
CREATE TABLE "EmpExemplar" (
    "codEmp" INTEGER NOT NULL,
    "tomboExemplar" INTEGER NOT NULL,

    CONSTRAINT "EmpExemplar_pkey" PRIMARY KEY ("codEmp","tomboExemplar")
);

-- CreateIndex
CREATE UNIQUE INDEX "Aluno_email_key" ON "Aluno"("email");

-- AddForeignKey
ALTER TABLE "Exemplar" ADD CONSTRAINT "Exemplar_codLivro_fkey" FOREIGN KEY ("codLivro") REFERENCES "Livro"("cod") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Emprestimo" ADD CONSTRAINT "Emprestimo_matAluno_fkey" FOREIGN KEY ("matAluno") REFERENCES "Aluno"("mat") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "EmpExemplar" ADD CONSTRAINT "EmpExemplar_codEmp_fkey" FOREIGN KEY ("codEmp") REFERENCES "Emprestimo"("cod") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "EmpExemplar" ADD CONSTRAINT "EmpExemplar_tomboExemplar_fkey" FOREIGN KEY ("tomboExemplar") REFERENCES "Exemplar"("tombo") ON DELETE RESTRICT ON UPDATE CASCADE;
