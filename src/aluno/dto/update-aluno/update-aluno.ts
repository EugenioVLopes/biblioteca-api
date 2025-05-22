import { ApiProperty, PartialType } from '@nestjs/swagger';
import { CreateAlunoDto } from '../create-aluno/create-aluno';

export class UpdateAlunoDto extends PartialType(CreateAlunoDto) {
  @ApiProperty({
    required: false,
    example: 2022001234,
    description: 'Matrícula única do aluno (não pode ser alterada)',
    readOnly: true,
  })
  mat?: number;

  @ApiProperty({
    required: false,
    example: 'Maria Silva',
    description: 'Nome completo do aluno',
    minLength: 3,
    maxLength: 100,
  })
  nome?: string;

  @ApiProperty({
    required: false,
    example: 'maria@email.com',
    description: 'E-mail institucional do aluno',
    format: 'email',
  })
  email?: string;

  @ApiProperty({
    required: false,
    example: 'Sistemas de Informação',
    description: 'Curso no qual o aluno está matriculado',
    minLength: 3,
    maxLength: 100,
  })
  curso?: string;
}
