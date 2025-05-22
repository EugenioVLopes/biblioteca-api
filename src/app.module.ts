import { Module } from '@nestjs/common';
import { AlunoModule } from './aluno/aluno.module';
import { PrismaModule } from './prisma/prisma.module';

@Module({
  imports: [AlunoModule, PrismaModule],
})
export class AppModule {}
