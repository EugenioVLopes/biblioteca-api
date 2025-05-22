import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateAlunoDto } from './dto/create-aluno/create-aluno';
import { UpdateAlunoDto } from './dto/update-aluno/update-aluno';

@Injectable()
export class AlunoService {
  constructor(private prisma: PrismaService) {}

  async create(data: CreateAlunoDto) {
    return this.prisma.aluno.create({ data });
  }

  async findAll() {
    return this.prisma.aluno.findMany();
  }

  async findOne(mat: number) {
    return this.prisma.aluno.findUnique({ where: { mat } });
  }

  async update(mat: number, data: UpdateAlunoDto) {
    return this.prisma.aluno.update({
      where: { mat },
      data,
    });
  }

  async remove(mat: number) {
    return this.prisma.aluno.delete({ where: { mat } });
  }
}
