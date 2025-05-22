import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { AlunoModule } from './aluno/aluno.module';
import { PrismaModule } from './prisma/prisma.module';

@Module({
  imports: [AlunoModule, PrismaModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
