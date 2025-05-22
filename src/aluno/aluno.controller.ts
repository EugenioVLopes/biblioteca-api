import {
  Body,
  Controller,
  Delete,
  Get,
  HttpStatus,
  Param,
  ParseIntPipe,
  Patch,
  Post,
} from '@nestjs/common';
import {
  ApiBadRequestResponse,
  ApiBody,
  ApiConflictResponse,
  ApiNotFoundResponse,
  ApiOperation,
  ApiParam,
  ApiResponse,
  ApiTags,
} from '@nestjs/swagger';
import { AlunoService } from './aluno.service';
import { CreateAlunoDto } from './dto/create-aluno/create-aluno';
import { UpdateAlunoDto } from './dto/update-aluno/update-aluno';

@ApiTags('Gestão de Alunos')
@Controller('aluno')
export class AlunoController {
  constructor(private readonly alunoService: AlunoService) {}

  @Post()
  @ApiOperation({
    summary: 'Criar um novo aluno',
    description: 'Endpoint para cadastrar um novo aluno no sistema. Todos os campos são obrigatórios.'
  })
  @ApiBody({ type: CreateAlunoDto })
  @ApiResponse({
    status: HttpStatus.CREATED,
    description: 'Aluno criado com sucesso.',
    type: CreateAlunoDto,
  })
  @ApiBadRequestResponse({
    description: 'Dados inválidos fornecidos. Verifique o formato dos campos.',
  })
  @ApiConflictResponse({
    description: 'Já existe um aluno cadastrado com esta matrícula.',
  })
  create(@Body() createAlunoDto: CreateAlunoDto) {
    return this.alunoService.create(createAlunoDto);
  }

  @Get()
  @ApiOperation({
    summary: 'Listar todos os alunos',
    description: 'Retorna uma lista com todos os alunos cadastrados no sistema, ordenados por nome.'
  })
  @ApiResponse({
    status: HttpStatus.OK,
    description: 'Lista de alunos retornada com sucesso.',
    type: [CreateAlunoDto],
  })
  findAll() {
    return this.alunoService.findAll();
  }

  @Get(':mat')
  @ApiOperation({
    summary: 'Buscar aluno pelo número de matrícula',
    description: 'Retorna os dados de um aluno específico baseado no número de matrícula.'
  })
  @ApiParam({
    name: 'mat',
    description: 'Número de matrícula do aluno',
    example: 2022001234,
    type: Number,
  })
  @ApiResponse({
    status: HttpStatus.OK,
    description: 'Aluno encontrado com sucesso.',
    type: CreateAlunoDto,
  })
  @ApiNotFoundResponse({
    description: 'Aluno não encontrado com a matrícula informada.',
  })
  @ApiBadRequestResponse({
    description: 'Número de matrícula inválido.',
  })
  findOne(@Param('mat', ParseIntPipe) mat: number) {
    return this.alunoService.findOne(mat);
  }

  @Patch(':mat')
  @ApiOperation({
    summary: 'Atualizar dados de um aluno',
    description: 'Atualiza os dados de um aluno existente. Apenas os campos fornecidos serão atualizados.'
  })
  @ApiParam({
    name: 'mat',
    description: 'Número de matrícula do aluno',
    example: 2022001234,
    type: Number,
  })
  @ApiBody({ type: UpdateAlunoDto })
  @ApiResponse({
    status: HttpStatus.OK,
    description: 'Aluno atualizado com sucesso.',
    type: CreateAlunoDto,
  })
  @ApiNotFoundResponse({
    description: 'Aluno não encontrado com a matrícula informada.',
  })
  @ApiBadRequestResponse({
    description: 'Dados inválidos fornecidos. Verifique o formato dos campos.',
  })
  update(
    @Param('mat', ParseIntPipe) mat: number,
    @Body() updateAlunoDto: UpdateAlunoDto,
  ) {
    return this.alunoService.update(mat, updateAlunoDto);
  }

  @Delete(':mat')
  @ApiOperation({
    summary: 'Remover um aluno',
    description: 'Remove permanentemente um aluno do sistema.'
  })
  @ApiParam({
    name: 'mat',
    description: 'Número de matrícula do aluno',
    example: 2022001234,
    type: Number,
  })
  @ApiResponse({
    status: HttpStatus.OK,
    description: 'Aluno removido com sucesso.',
    schema: {
      type: 'object',
      properties: {
        message: {
          type: 'string',
          example: 'Aluno removido com sucesso',
        },
        mat: {
          type: 'number',
          example: 2022001234,
        },
      },
    },
  })
  @ApiNotFoundResponse({
    description: 'Aluno não encontrado com a matrícula informada.',
  })
  @ApiBadRequestResponse({
    description: 'Número de matrícula inválido.',
  })
  remove(@Param('mat', ParseIntPipe) mat: number) {
    return this.alunoService.remove(mat);
  }
}
