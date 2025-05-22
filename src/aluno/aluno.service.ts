import { ConflictException, Injectable, NotFoundException } from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';
import { CreateAlunoDto } from './dto/create-aluno/create-aluno';
import { UpdateAlunoDto } from './dto/update-aluno/update-aluno';

/**
 * Serviço responsável pela lógica de negócios relacionada aos alunos
 */
@Injectable()
export class AlunoService {
  constructor(private prisma: PrismaService) {}

  /**
   * Cria um novo aluno
   * @param data Dados do aluno a ser criado
   * @throws {ConflictException} Se já existir um aluno com a mesma matrícula
   */
  async create(data: CreateAlunoDto) {
    try {
      return await this.prisma.aluno.create({ data });
    } catch (error) {
      if (error instanceof Prisma.PrismaClientKnownRequestError) {
        if (error.code === 'P2002') {
          throw new ConflictException('Já existe um aluno com esta matrícula');
        }
      }
      throw error;
    }
  }

  /**
   * Retorna todos os alunos cadastrados
   * @returns Lista de alunos
   */
  async findAll() {
    return this.prisma.aluno.findMany({
      orderBy: { nome: 'asc' },
    });
  }

  /**
   * Busca um aluno pelo número de matrícula
   * @param mat Número de matrícula do aluno
   * @throws {NotFoundException} Se o aluno não for encontrado
   */
  async findOne(mat: number) {
    const aluno = await this.prisma.aluno.findUnique({ where: { mat } });
    if (!aluno) {
      throw new NotFoundException(`Aluno com matrícula ${mat} não encontrado`);
    }
    return aluno;
  }

  /**
   * Atualiza os dados de um aluno
   * @param mat Número de matrícula do aluno
   * @param data Dados a serem atualizados
   * @throws {NotFoundException} Se o aluno não for encontrado
   */
  async update(mat: number, data: UpdateAlunoDto) {
    try {
      return await this.prisma.aluno.update({
        where: { mat },
        data,
      });
    } catch (error) {
      if (error instanceof Prisma.PrismaClientKnownRequestError) {
        if (error.code === 'P2025') {
          throw new NotFoundException(`Aluno com matrícula ${mat} não encontrado`);
        }
      }
      throw error;
    }
  }

  /**
   * Remove um aluno do sistema
   * @param mat Número de matrícula do aluno
   * @throws {NotFoundException} Se o aluno não for encontrado
   */
  async remove(mat: number) {
    try {
      await this.prisma.aluno.delete({ where: { mat } });
      return { message: 'Aluno removido com sucesso', mat };
    } catch (error) {
      if (error instanceof Prisma.PrismaClientKnownRequestError) {
        if (error.code === 'P2025') {
          throw new NotFoundException(`Aluno com matrícula ${mat} não encontrado`);
        }
      }
      throw error;
    }
  }
}
