import { Module } from '@nestjs/common';
import { PrismaModule } from '../prisma/prisma.module';
import { AlunoController } from './aluno.controller';
import { AlunoService } from './aluno.service';

/**
 * Módulo responsável pela gestão de alunos
 * @description Fornece endpoints para CRUD de alunos e gerencia suas dependências
 */
@Module({
  imports: [PrismaModule],
  providers: [AlunoService],
  controllers: [AlunoController],
  exports: [AlunoService],
})
export class AlunoModule {}
