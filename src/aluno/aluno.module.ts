import { Module } from '@nestjs/common';
import { AlunoService } from './aluno.service';
import { AlunoController } from './aluno.controller';

@Module({
  providers: [AlunoService],
  controllers: [AlunoController]
})
export class AlunoModule {}
