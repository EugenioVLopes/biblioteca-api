import { Injectable } from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class AlunoService {
  constructor(private prisma: PrismaService) {}

  async create(data: Prisma.AlunoCreateInput) {
    return this.prisma.aluno.create({ data });
  }

  async findAll() {
    return this.prisma.aluno.findMany();
  }

  async findOne(mat: number) {
    return this.prisma.aluno.findUnique({ where: { mat } });
  }

  async update(mat: number, data: Prisma.AlunoUpdateInput) {
    return this.prisma.aluno.update({ where: { mat }, data });
  }

  async remove(mat: number) {
    return this.prisma.aluno.delete({ where: { mat } });
  }
}
