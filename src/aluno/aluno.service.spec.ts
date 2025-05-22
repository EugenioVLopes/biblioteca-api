import { Test, TestingModule } from '@nestjs/testing';
import { PrismaService } from '../prisma/prisma.service';
import { AlunoService } from './aluno.service';
import { CreateAlunoDto } from './dto/create-aluno/create-aluno';
import { UpdateAlunoDto } from './dto/update-aluno/update-aluno';

describe('AlunoService', () => {
  let service: AlunoService;
  let prismaService: PrismaService;

  const mockPrismaService = {
    aluno: {
      create: jest.fn(),
      findMany: jest.fn(),
      findUnique: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
    },
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        AlunoService,
        {
          provide: PrismaService,
          useValue: mockPrismaService,
        },
      ],
    }).compile();

    service = module.get<AlunoService>(AlunoService);
    prismaService = module.get<PrismaService>(PrismaService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  describe('create', () => {
    it('should create a new aluno', async () => {
      const createAlunoDto: CreateAlunoDto = {
        mat: 12345,
        nome: 'João Silva',
        email: 'joao@email.com',
        curso: 'Sistemas de Informação',
      };

      const expectedResult = { ...createAlunoDto };
      mockPrismaService.aluno.create.mockResolvedValue(expectedResult);

      const result = await service.create(createAlunoDto);

      expect(result).toEqual(expectedResult);
      expect(mockPrismaService.aluno.create).toHaveBeenCalledWith({
        data: createAlunoDto,
      });
    });
  });

  describe('findAll', () => {
    it('should return an array of alunos', async () => {
      const expectedResult = [
        { mat: 12345, nome: 'João Silva', email: 'joao@email.com', curso: 'Sistemas de Informação' },
        { mat: 67890, nome: 'Maria Santos', email: 'maria@email.com', curso: 'Engenharia da Computação' },
      ];

      mockPrismaService.aluno.findMany.mockResolvedValue(expectedResult);

      const result = await service.findAll();

      expect(result).toEqual(expectedResult);
      expect(mockPrismaService.aluno.findMany).toHaveBeenCalled();
    });
  });

  describe('findOne', () => {
    it('should return a single aluno', async () => {
      const mat = 12345;
      const expectedResult = {
        mat,
        nome: 'João Silva',
        email: 'joao@email.com',
        curso: 'Sistemas de Informação',
      };

      mockPrismaService.aluno.findUnique.mockResolvedValue(expectedResult);

      const result = await service.findOne(mat);

      expect(result).toEqual(expectedResult);
      expect(mockPrismaService.aluno.findUnique).toHaveBeenCalledWith({
        where: { mat },
      });
    });
  });

  describe('update', () => {
    it('should update an aluno', async () => {
      const mat = 12345;
      const updateAlunoDto: UpdateAlunoDto = {
        nome: 'João Silva Atualizado',
        curso: 'Engenharia da Computação',
      };

      const expectedResult = {
        mat,
        ...updateAlunoDto,
        email: 'joao@email.com',
      };

      mockPrismaService.aluno.update.mockResolvedValue(expectedResult);

      const result = await service.update(mat, updateAlunoDto);

      expect(result).toEqual(expectedResult);
      expect(mockPrismaService.aluno.update).toHaveBeenCalledWith({
        where: { mat },
        data: updateAlunoDto,
      });
    });
  });

  describe('remove', () => {
    it('should remove an aluno', async () => {
      const mat = 12345;
      const expectedResult = {
        mat,
        nome: 'João Silva',
        email: 'joao@email.com',
        curso: 'Sistemas de Informação',
      };

      mockPrismaService.aluno.delete.mockResolvedValue(expectedResult);

      const result = await service.remove(mat);

      expect(result).toEqual(expectedResult);
      expect(mockPrismaService.aluno.delete).toHaveBeenCalledWith({
        where: { mat },
      });
    });
  });
});
