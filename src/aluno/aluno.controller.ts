import {
  Body,
  Controller,
  Delete,
  Get,
  Param,
  Patch,
  Post,
} from '@nestjs/common';
import {
  ApiOperation,
  ApiParam,
  ApiResponse,
  ApiTags,
} from '@nestjs/swagger';
import { AlunoService } from './aluno.service';
import { CreateAlunoDto } from './dto/create-aluno/create-aluno';
import { UpdateAlunoDto } from './dto/update-aluno/update-aluno';

@ApiTags('Alunos')
@Controller('aluno')
export class AlunoController {
  constructor(private readonly alunoService: AlunoService) {}

  @Post()
  @ApiOperation({ summary: 'Criar um aluno' })
  @ApiResponse({
    status: 201,
    description: 'Aluno criado com sucesso.',
    type: Object,
    schema: {
      example: {
        mat: 2022001234,
        nome: 'Maria Silva',
        email: 'maria@email.com',
        curso: 'Sistemas de Informação',
      },
    },
  })
  create(@Body() createAlunoDto: CreateAlunoDto) {
    return this.alunoService.create(createAlunoDto);
  }

  @Get()
  @ApiOperation({ summary: 'Listar todos os alunos' })
  @ApiResponse({
    status: 200,
    description: 'Lista de alunos retornada com sucesso.',
    type: Array,
    schema: {
      example: [
        {
          mat: 2022001234,
          nome: 'Maria Silva',
          email: 'maria@email.com',
          curso: 'Sistemas de Informação',
        },
        {
          mat: 2022005678,
          nome: 'João Souza',
          email: 'joao@email.com',
          curso: 'Engenharia da Computação',
        },
      ],
    },
  })
  findAll() {
    return this.alunoService.findAll();
  }

  @Get(':mat')
  @ApiOperation({ summary: 'Buscar aluno pelo número de matrícula' })
  @ApiParam({
    name: 'mat',
    description: 'Número de matrícula do aluno',
    example: 2022001234,
  })
  @ApiResponse({
    status: 200,
    description: 'Aluno encontrado com sucesso.',
    type: Object,
    schema: {
      example: {
        mat: 2022001234,
        nome: 'Maria Silva',
        email: 'maria@email.com',
        curso: 'Sistemas de Informação',
      },
    },
  })
  @ApiResponse({
    status: 404,
    description: 'Aluno não encontrado.',
  })
  findOne(@Param('mat') mat: string) {
    return this.alunoService.findOne(Number(mat));
  }

  @Patch(':mat')
  @ApiOperation({ summary: 'Atualizar dados de um aluno' })
  @ApiParam({
    name: 'mat',
    description: 'Número de matrícula do aluno',
    example: 2022001234,
  })
  @ApiResponse({
    status: 200,
    description: 'Aluno atualizado com sucesso.',
    type: Object,
    schema: {
      example: {
        mat: 2022001234,
        nome: 'Maria Silva Atualizada',
        email: 'maria_atualizada@email.com',
        curso: 'Análise de Dados',
      },
    },
  })
  @ApiResponse({
    status: 404,
    description: 'Aluno não encontrado.',
  })
  update(
    @Param('mat') mat: string,
    @Body() updateAlunoDto: UpdateAlunoDto,
  ) {
    return this.alunoService.update(Number(mat), updateAlunoDto);
  }

  @Delete(':mat')
  @ApiOperation({ summary: 'Remover um aluno' })
  @ApiParam({
    name: 'mat',
    description: 'Número de matrícula do aluno',
    example: 2022001234,
  })
  @ApiResponse({
    status: 200,
    description: 'Aluno removido com sucesso.',
    schema: {
      example: {
        message: 'Aluno removido com sucesso',
        mat: 2022001234,
      },
    },
  })
  @ApiResponse({
    status: 404,
    description: 'Aluno não encontrado.',
  })
  remove(@Param('mat') mat: string) {
    return this.alunoService.remove(Number(mat));
  }
}
